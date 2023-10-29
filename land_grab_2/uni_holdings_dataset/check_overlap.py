import itertools
import logging
import os
import traceback
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Optional

import geopandas
import pandas as pd

from land_grab_2.init_database.db.gristdb import GristDB
from land_grab_2.utilities.utils import in_parallel, batch_iterable, get_uuid, send_email, in_parallel_prod
from land_grab_2.utilities.overlap import eval_overlap_keep_left, dictlist_to_geodataframe, STATE_LONG_NAME, \
    tree_based_proximity

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

SCALE_SCHEDULER = os.environ.get('SCALE_SCHEDULER', 'synchronous')

UNIV_NAME_TO_STATE = {
    'Iowa State University': 'IA',
    'University of Idaho': 'ID',
    'University of Minnesota': 'MN',
    'North Carolina State University': 'NC',
    'New Mexico State University': 'NM',
    'Portland State University': 'OR',
    'Oregon State University': 'OR',
    'Utah State University': 'UT',
    'University of Vermont': 'VT',
    'Washington State University': 'WA',
    'University of Wisconsin': 'WI',
    'West Virginia University': 'WV',
}

STATE_TO_UNIV = {v: k for k, v in UNIV_NAME_TO_STATE.items()}


def db_list_counties(state_code):
    return GristDB().fetch_from_col_where_val('county', 'state2', state_code, distinct=True)


def db_list_states():
    return GristDB().fetch_all_unique('state2')


def db_get_county_all(county, pagination_row_id=None, batch_size=1000):
    return GristDB().fetch_from_col_where_val('*',
                                              'county',
                                              county,
                                              pagination_row_id=pagination_row_id,
                                              limit=batch_size)


def db_county_parcel_ids(county, batch_size):
    return GristDB().ids_where('county', county, batch_size=batch_size)


def extract_matches(grist_data, county_parcels_gdf, overlap_report):
    grist_data_update = []
    try:
        for name, group in overlap_report.groupby("joinidx_1")[["joinidx_0"]]:
            county_parcel = county_parcels_gdf[county_parcels_gdf['joinidx_1'] == name]

            grist_rows = grist_data[grist_data['joinidx_0'].isin(group['joinidx_0'].tolist())].index.tolist()
            for g_row_idx in grist_rows:
                rownum = grist_data.at[g_row_idx, 'rownum']
                if rownum is not None:
                    record = (int(rownum), county_parcel['id'].tolist()[0])
                    grist_data_update.append(record)
    except Exception as err:
        print(traceback.format_exc())
        print(f'just swallowed err from extract_matches(), err: {err}')

    return grist_data_update


def find_overlaps(grist_data, county_parcels_gdf, crs_list):
    try:
        overlapping_regions, grist_data, county_parcels_gdf = eval_overlap_keep_left(grist_data,
                                                                                     county_parcels_gdf,
                                                                                     crs_list=crs_list,
                                                                                     return_inputs=True)

        return (extract_matches(grist_data, county_parcels_gdf, overlapping_regions)
                if overlapping_regions.shape[0] > 0
                else [])
    except Exception as err:
        print(f'failing on mysterious except in find_overlaps(): {err}')


def write_county_batch(grist_data_path: str, state_code: str, county: str, batch_results: Optional[list]):
    if batch_results is None or isinstance(batch_results, list) and len(batch_results) == 0:
        return
    output_dir = Path(grist_data_path).parent.parent / 'output'
    state_dir = output_dir / state_code
    county_dir = state_dir / county
    bid = get_uuid()
    batch_name = f'{state_code}_{county}_{bid}.csv'
    if not county_dir.exists():
        county_dir.mkdir(parents=True, exist_ok=True)

    results_hydrated = GristDB().hydrate_ids([pid for _, pid in batch_results])
    results = [
        {'rownum': grist_rownum, **{k: v for k, v in regrid_row.items() if k != 'id'}}
        for (grist_rownum, _), regrid_row in zip(batch_results, results_hydrated)
    ]
    df = pd.DataFrame(results)
    df.to_csv(str(county_dir / batch_name), index=False)


def process_parcels_batch_prod(grist_data_path, county, state_code, parcels_batch):
    try:
        grist_data = geopandas.read_file(grist_data_path)
        grist_data = grist_data[grist_data.university == STATE_TO_UNIV[state_code]]
        county_parcels = GristDB().hydrate_ids(parcels_batch)

        county_parcels_gdf = dictlist_to_geodataframe(county_parcels, crs=grist_data.crs)
        crs_list = GristDB().crs_search_by_state(STATE_LONG_NAME[state_code])
        crs_list = [f"{r['data_source']}:{r['coord_ref_sys_code']}" for r in crs_list]
        crs_list = [grist_data.crs] + crs_list

        overlapping_county_parcels = find_overlaps(grist_data, county_parcels_gdf, crs_list)
        if overlapping_county_parcels:
            print(f' found {len(overlapping_county_parcels)} parcels with overlap for {county} in {state_code}')
            write_county_batch(grist_data_path, state_code, county, overlapping_county_parcels)

        return overlapping_county_parcels
    except Exception as err:
        print(traceback.format_exc())
        print(err)


def write_county_batch_exp(grist_data_path: str, state_code: str, county: str, batch_results: Optional[list]):
    if batch_results is None or isinstance(batch_results, list) and len(batch_results) == 0:
        return
    output_dir = Path(grist_data_path).parent.parent / 'output'
    state_dir = output_dir / state_code
    county_dir = state_dir / county
    bid = get_uuid()
    batch_name = f'{state_code}_{county}_{bid}.csv'
    if not county_dir.exists():
        county_dir.mkdir(parents=True, exist_ok=True)

    results = [
        {'rownum': grist_rownum, **{k: v for k, v in regrid_row.items() if k != 'id'}}
        for match_score, grist_rownum, grist_row, regrid_row, contains in batch_results
        if contains
    ]

    if results:
        df = pd.DataFrame(results)
        df.to_csv(str(county_dir / batch_name), index=False)


def process_parcels_batch(grist_data_path, county, state_code, parcels_batch):
    try:
        grist_data = geopandas.read_file(grist_data_path)
        grist_data = grist_data[grist_data.university == STATE_TO_UNIV[state_code]]
        county_parcels = GristDB().hydrate_ids(parcels_batch)

        county_parcels_gdf = dictlist_to_geodataframe(county_parcels, crs=grist_data.crs)
        # crs_list = GristDB().crs_search_by_state(STATE_LONG_NAME[state_code])
        # crs_list = [f"{r['data_source']}:{r['coord_ref_sys_code']}" for r in crs_list]
        # crs_list = [grist_data.crs] + crs_list

        # overlapping_county_parcels = find_overlaps(grist_data, county_parcels_gdf, crs_list)
        overlapping_county_parcels = tree_based_proximity(
            grist_data.to_dict(orient='records'), county_parcels_gdf, grist_data.crs
        )
        overlapping_county_parcels = list(overlapping_county_parcels)

        if overlapping_county_parcels:
            # print(f' found {len(overlapping_county_parcels)} parcels with overlap for {county} in {state_code}')
            write_county_batch_exp(grist_data_path, state_code, county, overlapping_county_parcels)

        return overlapping_county_parcels
    except Exception as err:
        print(traceback.format_exc())
        print(err)


def process_county(grist_data_path, state_code, county):
    county_parcel_groups = batch_iterable(
        [p['id'] for p in db_county_parcel_ids(county, 100000)],
        batch_size=5000
    )

    parcel_matches_ids = in_parallel(county_parcel_groups,
                                     partial(process_parcels_batch, grist_data_path, county, state_code),
                                     batched=False)

    parcel_matches_ids = itertools.chain.from_iterable(parcel_matches_ids)

    return parcel_matches_ids


def process_state(grist_data_path, state_code):
    print(f'processing state: {state_code}')
    counties = [c['county'] for c in db_list_counties(state_code)]
    print(f'state: {state_code} total counties: {len(counties)}')
    overlapping_parcels_ids = in_parallel_prod(counties,
                                          partial(process_county, grist_data_path, state_code),
                                          # scheduler='synchronous',
                                          show_progress=True,
                                          batched=False)
    overlapping_parcels_ids = itertools.chain.from_iterable(overlapping_parcels_ids)

    return overlapping_parcels_ids


def find_overlapping_parcels(grist_data_path, states=None):
    all_states = states or [v for v in UNIV_NAME_TO_STATE.values()]
    all_matches_ids = in_parallel_prod(all_states, partial(process_state, grist_data_path),
                                  scheduler='synchronous',
                                  batched=False)
    # all_matches_ids = list(itertools.chain.from_iterable(all_matches_ids))
    # if all_matches_ids:
    #     overlapping_county_parcels = GristDB().hydrate_ids([pid for _, pid in all_matches_ids])
    #     results = [
    #         {'rownum': grist_rownum, **{k: v for k, v in regrid_row.items() if k != 'id'}}
    #         for (grist_rownum, _), regrid_row in zip(all_matches_ids, overlapping_county_parcels)
    #     ]
    #     df = pd.DataFrame(results)
    #     return df


def run(states=None):
    print('Running: private_holdings_by_geo_overlap')
    # given a set of geometry entries from the regrid database and
    # a set of geometry entries from university primary source,
    # gather regrid database entries where there is intersection with university primary source data
    data_tld = os.environ.get('DATA')
    data_directory = Path(f'{data_tld}/uni_holdings/overlap_check')

    st = datetime.now()
    states = None if not states else [s.strip() for s in states.split(',')]
    overlapping_parcels = find_overlapping_parcels(str(data_directory / 'input/UL-provided-names.geojson'), states)
    print(f'processing took {datetime.now() - st}')
    try:
        send_email('laanak@gmail.com', 'check-overlap-status', f'processing took {datetime.now() - st}')
    except:
        pass
    # if overlapping_parcels is not None:
    #     overlapping_parcels.to_csv(str(data_directory / 'output/matches.csv'), index=False)
    # else:
    #     print('no report to write')


if __name__ == '__main__':
    run()
