"""
University	Reverse_Search_Name	Reverse_Search_Mail_Address	Status	Check_Method
"""
import copy
import itertools
import logging
import os
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Tuple

import geopandas
import numpy as np
import pandas as pd
import typer
from numpy import percentile

from land_grab_2.init_database.db.gristdb import GristDB, GristDbResults
from land_grab_2.utilities.overlap import dictlist_to_geodataframe
from land_grab_2.utilities.utils import batch_iterable, in_parallel, in_parallel_fake

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = typer.Typer()
OUT_DIR = Path('').resolve()

UNIV_NAME_TO_STATE = {'Iowa State University': 'IA',
                      'University of Wisconsin': 'WI',
                      'Washington State University': 'WA',
                      'University of Minnesota': 'MN',
                      'North Carolina State University': 'NC',
                      'University of Vermont': 'VT',
                      'West Virginia University': 'WV',
                      'Utah State University': 'UT',
                      'University of Idaho': 'ID',
                      'Oregon State University': 'OR',
                      'New Mexico State University': 'NM',
                      'University of Florida': 'FL',
                      'University of California System': 'CA',
                      'University of Arizona': 'AZ',
                      'Purdue University': 'IN',
                      'University of Missouri': 'MO',
                      'Ohio State University': 'OH',
                      'University of Tennessee': 'TN'}

STATE_TO_UNIV = {v: k for k, v in UNIV_NAME_TO_STATE.items()}


def write_search_results(output_dir: Path, name: str, univ: str, queries: List[str], results: List[Dict[str, Any]]):
    univ_out_dir = output_dir / univ
    if not univ_out_dir.exists():
        univ_out_dir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame({'query_components': queries}).to_csv(univ_out_dir / f'{name}_query.csv', index=False)

    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(univ_out_dir / f'{name}_search_results.csv', index=False)

        gdf = dictlist_to_geodataframe(results)
        gdf.to_file(str(univ_out_dir / f'{name}_search_results.geojson'), driver='GeoJSON')
    else:
        results_file = univ_out_dir / f'{name}_empty_results.txt'
        with results_file.open('w') as fh:
            fh.write('')


@dataclass
class Bound:
    name: str
    left: int
    right: int
    values: List[str] = field(default_factory=list)


@dataclass
class StrSizeBucketBounds:
    small: Bound
    medium: Bound
    large: Bound
    extra_large: Bound


def db_state_by_min_col_length(state: str, column: str, min_len: int) -> List[Dict[str, Any]]:
    search_sql = f"""
    select * from regrid where state2 = '{state}' AND length({column}) >= {min_len};
    """
    return GristDB().execute(search_sql, results_type=GristDbResults.ALL)


def gather_size_bounds(q):
    data = np.array([len(s) for s in q])
    quartiles = percentile(data, [25, 50, 75])

    data_min = data.min()
    q1 = int(quartiles[0])
    median = int(quartiles[1])
    q3 = int(quartiles[2])
    data_max = data.max()

    bounds = StrSizeBucketBounds(small=Bound('small', data_min, median),
                                 medium=Bound('medium', q1, q3),
                                 large=Bound('large', median, data_max),
                                 extra_large=Bound('extra_large', data_max, 2 * data_max))

    return bounds


def bucket_queries(bounds, queries):
    for q in queries:
        if bounds.extra_large.left <= len(q):
            bounds.extra_large.values.append(q)
        elif bounds.large.left <= len(q) <= bounds.large.right:
            bounds.large.values.append(q)
        elif bounds.medium.left <= len(q) <= bounds.medium.right:
            bounds.medium.values.append(q)
        else:
            bounds.small.values.append(q)
    return bounds


def _search(state: str, column: str, bound: Bound):
    results = GristDB().state_by_min_col_length(state=state, column=column, min_len=bound.left, max_len=bound.right)

    keepers = []
    for result in results:
        if any(v in result[column] for v in bound.values):
            keepers.append(result)

    return keepers


def search_bucket_method(university: str, queries: List[str], column: str) -> List[Dict[str, Any]]:
    state = UNIV_NAME_TO_STATE.get(university)
    if not state:
        return

    # find bucket sizes based on query lengths by summarization
    bounds = gather_size_bounds(queries)

    queries_by_size = bucket_queries(bounds, queries)
    queries_by_size_xl_first = [
        # queries_by_size.extra_large,
        queries_by_size.large,
        queries_by_size.medium,
        queries_by_size.small
    ]

    keepers = list(itertools.chain.from_iterable([_search(state, column, bound) for bound in queries_by_size_xl_first]))

    return keepers


def search(university: str, queries: List[str], column: str, batch_size=100) -> List[Dict[str, Any]]:
    # gather all ids for a state
    state = UNIV_NAME_TO_STATE.get(university)
    state_ids = GristDB().ids_where('state2', state) # TODO paged impl.

    # batch ids into batches of $X
    state_id_batches = batch_iterable(state_ids, batch_size=batch_size)

    # DISTINCT query db for field match where id IN $ids_list
    batched_results = in_parallel(state_id_batches,
                                  partial(GristDB().db_query_field_in_value_by_ids, queries, column),
                                  scheduler='processes',
                                  show_progress=True,
                                  batched=False)

    # maybe quality-filter - post-process result
    # quality_filter(batched_results) # possibly also in parallel

    # flatten results
    keepers = list(itertools.chain.from_iterable(batched_results))

    return keepers


def process_university(row, secondary_search=False):
    global OUT_DIR
    out_dir = OUT_DIR / 'reverse_search_results'
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)

    try:
        db = GristDB()
        univ = row['University']
        owner = row['Reverse_Search_Name']
        mailadd = row['Reverse_Search_Mail_Address']

        owner_records = None
        address_records = None
        if isinstance(owner, str) and len(owner) > 0:
            owners = [o.strip() for o in owner.split('\n')]
            owner_records = search(univ, owners, 'owner')
            # owner_records = db.search_text_column_has_query('regrid', 'owner', owners)
            write_search_results(out_dir, 'owner', univ, owners, owner_records)

        if isinstance(mailadd, str) and len(mailadd) > 0:
            addresses = [a.strip() for a in mailadd.split('\n')]
            address_records = search(univ, addresses, 'mailadd')
            # address_records = db.search_text_column_has_query('regrid', 'mailadd', addresses)
            write_search_results(out_dir, 'address', univ, addresses, address_records)

        if secondary_search:
            if owner and mailadd and owner_records and address_records:
                owner_ids = set([r['id'] for r in owner_records])
                address_ids = set([r['id'] for r in address_records])
                owner_no_address = owner_ids - address_ids
                address_no_owner = address_ids - owner_ids
                shared_ids = set.intersection(owner_ids, address_ids)
                print(f'[univ: {univ}] address had: {len(address_ids)} unique ids, '
                      f'owner had: {len(owner_ids)} unique ids, shared: {len(shared_ids)}')
                print(f'[univ: {univ}] address had: {len(address_no_owner)} ids not in owner, '
                      f'owner had: {len(owner_no_address)} ids not in address')

            # for rows that match owner queries,
            if owner_records:
                # we want to extract their address field
                owner_addresses = [r.get('mailadd') for r in owner_records if r.get('mailadd')]
                if not owner_addresses:
                    return

                # and use the ones not already accounted for in original address queries list,
                existing_address_queries = mailadd if mailadd else []
                owner_addresses_for_search = set(
                    [a.strip() for a in owner_addresses if a not in existing_address_queries])

                # for returning only rows whose ids are not in the set of ids we already have
                all_ids = []
                if owner_records:
                    all_ids += [r['id'] for r in owner_records]
                if address_records:
                    all_ids += [r['id'] for r in address_records]

                # to perform an address search,
                # addresses = [a.strip() for a in mailadd.split(';')]
                print(f'[univ: {univ}] owner-address searching {len(owner_addresses_for_search)}: queries')
                address_results_from_owner_search = search(univ, list(owner_addresses_for_search), 'mailadd')
                # address_results_from_owner_search = db.search_text_column_has_query('regrid',
                #                                                                     'mailadd',
                #                                                                     list(owner_addresses_for_search))
                #
                # uniq_results = [
                # r for r in address_results_from_owner_search if r.get('id') and r.get('id') not in all_ids
                # ]

                write_search_results(out_dir,
                                     'address_results_from_owner_search',
                                     univ,
                                     list(owner_addresses_for_search),
                                     address_results_from_owner_search)
    except Exception as err:
        print(traceback.format_exc())
        log.error(err)


@app.command()
def run():
    print('running private_holdings_by_reverse_search')
    data_tld = os.environ.get('DATA')
    data_directory = Path(f'{data_tld}/uni_holdings/reverse_search')

    try:
        global OUT_DIR
        OUT_DIR = data_directory / 'output'

        csv_path = data_directory / 'input/2308_LGU UNIS HACKATHON - Sheet5.csv'
        df = pd.read_csv(csv_path, index_col=False, dtype=str)

        st = datetime.now()
        df.apply(process_university, axis=1)
        print(f'processing took {datetime.now() - st}')
    except Exception as err:
        print(traceback.format_exc())
        log.error(err)


if __name__ == '__main__':
    run()
