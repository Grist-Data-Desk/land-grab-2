import concurrent.futures
import itertools
import json
import logging
import os
import traceback
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Optional

import geopandas
import pandas as pd
from shapely import MultiPolygon, Polygon

from land_grab_2.init_database.db.gristdb import GristDB
from land_grab_2.utilities.utils import in_parallel, batch_iterable, get_uuid, in_parallel_fake, send_email
from land_grab_2.utilities.overlap import eval_overlap_keep_left

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

SCALE_SCHEDULER = os.environ.get('SCALE_SCHEDULER', 'synchronous')

UNIV_NAME_TO_STATE = {'Iowa State University': 'IA',
                      'Portland State University': 'OR',
                      'University of Wisconsin': 'WI',
                      'Washington State University': 'WA',
                      'University of Minnesota': 'MN',
                      'North Carolina State University': 'NC',
                      'University of Vermont': 'VT',
                      'West Virginia University': 'WV',
                      'Utah State University': 'UT',
                      'University of Idaho': 'ID',
                      'Oregon State University': 'OR',
                      'New Mexico State University': 'NM'}

STATE_TO_UNIV = {v: k for k, v in UNIV_NAME_TO_STATE.items()}
STATE_LONG_NAME = {'IA': 'iowa',
                   'OR': 'oregon',
                   'WI': 'wisconsin',
                   'WA': 'washington',
                   'MN': 'minnesota',
                   'NC': 'north carolina',
                   'VT': 'vermont',
                   'WV': 'west virginia',
                   'UT': 'utah',
                   'ID': 'idaho',
                   'NM': 'new mexico'}


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


def db_county_parcel_ids(county):
    return GristDB().ids_where('county', county)


def is_polygon_def(arr, multi=True):
    if multi:
        return all(len(item) > 2 for item in arr)
    return all(len(item) == 2 and not (isinstance(item[0], list) or isinstance(item[0], list)) for item in arr)


def strs_to_floats(obj, hydrate_points=False):
    if isinstance(obj, str):
        return float(obj)

    if isinstance(obj, list):
        if len(obj) == 2:
            x, y = obj
            return strs_to_floats(x, hydrate_points), strs_to_floats(y, hydrate_points)

        if hydrate_points and is_polygon_def(obj, multi=False):
            polygon_shell = tuple([strs_to_floats(item, hydrate_points) for item in obj])
            polygon_holes = None
            return Polygon(polygon_shell, polygon_holes)

        return [strs_to_floats(item, hydrate_points) for item in obj]

    return obj


def dict_to_geodataframe(crs, parcel) -> Optional[geopandas.GeoSeries]:
    geometry_json = parcel.get('geometry')
    if not geometry_json:
        return

    try:
        geojson_0 = strs_to_floats(json.loads(geometry_json), hydrate_points=True)
        geojson = ([MultiPolygon(geojson_0)]
                   if all(isinstance(obj, Polygon) for obj in geojson_0)
                   else [MultiPolygon(p) for p in geojson_0])

        gdfs = []
        df = pd.DataFrame([parcel], dtype=str, columns=parcel.keys())
        for poly in geojson:
            gdf = geopandas.GeoDataFrame(df, crs=crs, geometry=[poly])
            gdfs.append(gdf)
        return gdfs
    except Exception as err:
        print(traceback.format_exc())
        log.error(err)


def dictlist_to_geodataframe(count_parcels, crs=None):
    gdfs = itertools.chain.from_iterable(
        in_parallel(count_parcels, partial(dict_to_geodataframe, crs), batched=False)
    )
    # gdfs = itertools.chain.from_iterable([dict_to_geodataframe(crs, p) for p in count_parcels])
    gdf = geopandas.GeoDataFrame(
        pd.concat(gdfs, ignore_index=True),
        crs=crs
    )
    return gdf


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


def process_parcels_batch(grist_data_path, county, state_code, parcels_batch):
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


def process_county(grist_data_path, state_code, county):
    county_parcel_groups = batch_iterable([p['id'] for p in db_county_parcel_ids(county)], batch_size=500)

    parcel_matches_ids = in_parallel(county_parcel_groups,
                                     partial(process_parcels_batch,
                                             grist_data_path,
                                             county,
                                             state_code),
                                     batched=False)

    parcel_matches_ids = itertools.chain.from_iterable(parcel_matches_ids)

    return parcel_matches_ids


def process_state(grist_data_path, state_code):
    print(f'processing state: {state_code}')
    counties = [c['county'] for c in db_list_counties(state_code)]
    print(f'state: {state_code} total counties: {len(counties)}')
    overlapping_parcels_ids = in_parallel(counties,
                                          partial(process_county, grist_data_path, state_code),
                                          scheduler='processes',
                                          show_progress=True,
                                          batched=False)
    overlapping_parcels_ids = itertools.chain.from_iterable(overlapping_parcels_ids)

    return overlapping_parcels_ids


def find_overlapping_parcels(grist_data_path):
    all_states = [v for v in UNIV_NAME_TO_STATE.values()]
    all_matches_ids = in_parallel(all_states, partial(process_state, grist_data_path),
                                  scheduler='processes',
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


def run():
    print('Running: private_holdings_by_geo_overlap')
    # given a set of geometry entries from the regrid database and
    # a set of geometry entries from university primary source,
    # gather regrid database entries where there is intersection with university primary source data
    data_tld = os.environ.get('DATA')
    data_directory = Path(f'{data_tld}/uni_holdings/overlap_check')

    st = datetime.now()
    overlapping_parcels = find_overlapping_parcels(str(data_directory / 'input/UL-provided-names.geojson'))
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
