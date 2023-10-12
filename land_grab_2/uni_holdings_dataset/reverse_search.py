"""
University	Reverse_Search_Name	Reverse_Search_Mail_Address	Status	Check_Method
"""
import itertools
import logging
import os
import traceback
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import typer

from land_grab_2.init_database.db.gristdb import GristDB
from land_grab_2.utilities.overlap import dictlist_to_geodataframe
from land_grab_2.utilities.utils import batch_iterable, in_parallel

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = typer.Typer()

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
        results_df.drop_duplicates([c for c in results_df.columns if c != 'id'], inplace=True)
        results_df.to_csv(univ_out_dir / f'{name}_search_results.csv', index=False)

        gdf = dictlist_to_geodataframe(results)
        gdf.to_file(str(univ_out_dir / f'{name}_search_results.geojson'), driver='GeoJSON')
    else:
        results_file = univ_out_dir / f'{name}_empty_results.txt'
        with results_file.open('w') as fh:
            fh.write('')


def secondary_search(univ, owner, mailadd, owner_records, address_records, out_dir):
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


def search(university: str, queries: List[str], column: str, batch_size=10000) -> List[Dict[str, Any]]:
    # gather all ids for a state
    state = UNIV_NAME_TO_STATE.get(university)
    # print(f'filtering db for state: {state}')
    st = datetime.now()
    state_ids = GristDB().ids_where('state2', state, batch_size=None)
    et = datetime.now()
    # print(f'took {et - st}s')

    # batch ids into batches of $X
    # print(f'batching {len(state_ids)} records into batches of {batch_size}')
    st = datetime.now()
    state_id_batches = batch_iterable(state_ids, batch_size=batch_size)
    et = datetime.now()
    # print(f'took {et - st}s')

    # DISTINCT query db for field match where id IN $ids_list
    # print('querying ids for batched matches')
    st = datetime.now()
    batched_results1 = in_parallel(state_id_batches,
                                   partial(GristDB().db_query_field_in_value_by_ids_1, queries, column),
                                   scheduler='threads',
                                   batched=False)
    et = datetime.now()
    # print(f'took {et - st}s')

    # print('hydrating ids for batched matched results')
    st = datetime.now()
    batched_results2 = in_parallel(batched_results1,
                                   GristDB().db_query_field_in_value_by_ids_2,
                                   scheduler='threads',
                                   batched=False)
    et = datetime.now()
    # print(f'took {et - st}s')

    # maybe quality-filter - post-process result
    # quality_filter(batched_results) # possibly also in parallel

    # flatten results
    # print('flattening results')
    st = datetime.now()
    keepers = list(itertools.chain.from_iterable(batched_results2))
    et = datetime.now()
    # print(f'took {et - st}s')

    # print(f'completed {column} search for {state}, found: {len(keepers)}')
    return keepers


def process_university(should_secondary_search=False, out_dir=None, row=None):
    try:
        univ = row['University']
        owner = row['Reverse_Search_Name']
        mailadd = row['Reverse_Search_Mail_Address']
        if not univ or not (univ and (owner or mailadd)):
            print(f'skipping univ: {univ}')
            return

        owner_records = None
        address_records = None
        if isinstance(owner, str) and len(owner) > 0:
            owners = [o.strip() for o in owner.split('\n')]
            owner_records = search(univ, owners, 'owner')
            write_search_results(out_dir, 'owner', univ, owners, owner_records)

        if isinstance(mailadd, str) and len(mailadd) > 0:
            addresses = [a.strip() for a in mailadd.split('\n')]
            address_records = search(univ, addresses, 'mailadd')
            write_search_results(out_dir, 'address', univ, addresses, address_records)

        if should_secondary_search:
            secondary_search(univ, owner, mailadd, owner_records, address_records, out_dir)
    except Exception as err:
        print(traceback.format_exc())
        log.error(err)


@app.command()
def run():
    print('running private_holdings_by_reverse_search')
    data_tld = os.environ.get('DATA')
    data_directory = Path(f'{data_tld}/uni_holdings/reverse_search')

    try:
        out_dir = data_directory / 'output'
        if not out_dir.exists():
            out_dir.mkdir(parents=True, exist_ok=True)

        csv_path = data_directory / 'input/2308_LGU UNIS HACKATHON - Sheet5.csv'
        df = pd.read_csv(csv_path, index_col=False, dtype=str)

        univs = df.to_dict(orient='records')
        should_secondary_search = False
        st = datetime.now()
        in_parallel(univs, partial(process_university, should_secondary_search, out_dir),
                    show_progress=True,
                    batched=False)
        print(f'processing took {datetime.now() - st}')
    except Exception as err:
        print(traceback.format_exc())
        log.error(err)


if __name__ == '__main__':
    run()
