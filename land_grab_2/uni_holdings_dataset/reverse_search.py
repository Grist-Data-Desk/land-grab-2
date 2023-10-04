"""
University	Reverse_Search_Name	Reverse_Search_Mail_Address	Status	Check_Method
"""
import logging
import os
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import geopandas
import pandas as pd
import typer

from land_grab_2.init_database.db.gristdb import GristDB

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = typer.Typer()
OUT_DIR = Path('').resolve()


def write_search_results(output_dir: Path, name: str, univ: str, queries: List[str], results: List[Dict[str, Any]]):
    univ_out_dir = output_dir / univ
    if not univ_out_dir.exists():
        univ_out_dir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame({'query_components': queries}).to_csv(univ_out_dir / f'{name}_query.csv', index=False)

    if results:
        pd.DataFrame(results).to_csv(univ_out_dir / f'{name}_search_results.csv', index=False)
    else:
        results_file = univ_out_dir / f'{name}_empty_results.txt'
        with results_file.open('w') as fh:
            fh.write('')


def process_university(row):
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
            owners = [o.strip() for o in owner.split(';')]
            owner_records = db.search_text_column_has_query('regrid', 'owner', owners)
            write_search_results(out_dir, 'owner', univ, owners, owner_records)

        if isinstance(mailadd, str) and len(mailadd) > 0:
            addresses = [a.strip() for a in mailadd.split(';')]
            address_records = db.search_text_column_has_query('regrid', 'mailadd', addresses)
            write_search_results(out_dir, 'address', univ, addresses, address_records)

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
            owner_addresses_for_search = set([a.strip() for a in owner_addresses if a not in existing_address_queries])

            # for returning only rows whose ids are not in the set of ids we already have
            all_ids = []
            if owner_records:
                all_ids += [r['id'] for r in owner_records]
            if address_records:
                all_ids += [r['id'] for r in address_records]

            # to perform an address search,
            # addresses = [a.strip() for a in mailadd.split(';')]
            print(f'[univ: {univ}] owner-address searching {len(owner_addresses_for_search)}: queries')
            address_results_from_owner_search = db.search_text_column_has_query('regrid',
                                                                                'mailadd',
                                                                                list(owner_addresses_for_search))

            # uniq_results = [
            # r for r in address_results_from_owner_search if r.get('id') and r.get('id') not in all_ids
            # ]

            write_search_results(out_dir,
                                 'address_results_from_owner_search',
                                 univ,
                                 list(owner_addresses_for_search),
                                 address_results_from_owner_search)
    except Exception as err:
        log.error(err)


@app.command()
def main():
    data_tld = os.environ.get('DATA')
    data_directory = Path(f'{data_tld}/uni_holdings/reverse_search')

    try:
        global OUT_DIR
        OUT_DIR = data_directory / 'output'

        grist_data_path = str(data_directory / 'input/UL-provided-names.geojson')
        grist_data = geopandas.read_file(grist_data_path)

        csv_path = data_directory / 'input/2308_LGU UNIS HACKATHON - UNI Priority Intake Status.csv'
        df = pd.read_csv(csv_path, index_col=False, dtype=str)

        st = datetime.now()
        for univ in set(df.Uni.tolist()):
            df.apply(process_university, axis=1)
        print(f'processing took {datetime.now() - st}')
    except Exception as err:
        print(traceback.format_exc())
        log.error(err)


if __name__ == '__main__':
    main()
