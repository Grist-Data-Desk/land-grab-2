import json
import logging
import os
from collections import defaultdict
from pathlib import Path

import geopandas
import numpy as np
from tqdm import tqdm

from land_grab_2.stl_dataset.step_2.land_activity_search.state_data_sources import STATE_ACTIVITIES, rewrite_rules
from land_grab_2.utilities.utils import GristCache
from land_grab_2.utilities.overlap import eval_overlap_keep_left

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

STL_COMPARISON_BASE_DIR = Path('')
CACHE_DIR = Path('')
STATE_OUT_COLS = ['object_id', 'state', 'university', 'Activity', 'Sub-activity', 'Use Purpose',
                  'Lessee or Owner or Manager', 'Lessee Name 2', 'Owner Address or Location', 'Lessor',
                  'Transaction Type', 'Lease Status', 'Lease Start Date', 'Lease End Date', 'Lease Extension Date',
                  'Commodity', 'Source', 'LandClass', 'Rights-Type']
DONT_USE_COLS = ['TypeGroup', 'Type', 'Status', 'DteGranted', 'DteExpires', 'Name', 'ALL_LESSEE']

GRIST_DATA_UPDATE = defaultdict(set)
COLUMN_RENAME_RULES = {}
AZ_KEY = {
    '0': 'Unleased Parcels',
    '1': 'Agriculture',
    '3': 'Commercial Lease',
    '5': 'Grazing Lease',
    '8': 'Prospecting Permit',
    '66': 'US Govt Exclusive Use',
    '89': 'Institutional Use',
    '0.0': 'Unleased Parcels',
    '1.0': 'Agriculture',
    '3.0': 'Commercial Lease',
    '5.0': 'Grazing Lease',
    '8.0': 'Prospecting Permit',
    '66.0': 'US Govt Exclusive Use',
    '89.0': 'Institutional Use',
}


# def capture_state_data(activity_state: str,
#                        activity: StateActivityDataSource,
#                        # matches: List[GristOverlapMatch],
#                        column_rename_rules: Dict[str, Any]):
#     missing_cols = set([])
#     expected_cols = set([])
#     activity_records = []
#     for m in matches:
#         if m is None:
#             continue
#
#         activity_col_names = [c for c in m.activity_row.keys().tolist()]
#         for grist_match in m.grist_rows.iterrows():
#             grist_match = grist_match[1]
#
#             activity_record = {}
#             if activity.use_name_as_activity:
#                 activity_record['Activity'] = activity.name
#
#             activity_record['object_id'] = grist_match['object_id']
#             activity_record['state'] = grist_match['state']
#             activity_record['university'] = grist_match['university']
#             # TODO where is county?
#
#             for col in activity.keep_cols:
#                 if col in activity_col_names:
#                     renamed_col = maybe_rename_column(col, activity_state, column_rename_rules, activity)
#                     activity_record[renamed_col] = m.activity_row[col].tolist()[0]
#                 else:
#                     missing_cols.add(col)
#                     expected_cols.update(list(m.activity_row.keys()))
#
#             activity_records.append(activity_record)
#
#     if missing_cols:
#         log.error(f'missing col in state-data. expected {missing_cols}'
#                   f' for state: {activity_state} activity: {activity.name} '
#                   f'which had cols: {expected_cols}')
#
#     return activity_records


def find_missing_cols(rewrite_rules, current_cols, the_out_dir):
    missing_cols = set(STATE_OUT_COLS) - set(current_cols)

    locs = []
    for state, acts in rewrite_rules.items():
        state_dict = defaultdict(list)
        for act, cols in acts.items():
            for in_col, out_col in cols.items():
                if out_col in missing_cols:
                    state_dict[out_col].append([state, act, in_col])
        if len(state_dict.keys()) > 0:
            locs.append(state_dict)

    with (the_out_dir / 'missing_col_info.json').open('w') as fh:
        json.dump(locs, fh)


def maybe_rename_column(col, activity_state=None, column_rename_rules=None, activity=None):
    state = activity_state.lower()
    name = activity.name.lower()
    if state in column_rename_rules and name in column_rename_rules[state] and col in column_rename_rules[state][name]:
        return column_rename_rules[state][name][col]
    return col


def simple_activity_rename(row):
    rename_rules = {'OilAndGas': 'Oil and gas',
                    'OtherMin': 'Other Minerals',
                    'OtherMinerals': 'Other Minerals',
                    'Oil & Gas': 'Oil and gas'}

    incumbent_activity_val = row['activity']
    if isinstance(incumbent_activity_val, str) and len(incumbent_activity_val) > 0:
        for rename_trigger, new_name in rename_rules.items():
            if rename_trigger in incumbent_activity_val:
                row['activity'] = new_name

    return row


def get_activity_column(activity, state):
    # which col in the rewrite rules is the one that becomes activity
    activity_rewrite_rules = COLUMN_RENAME_RULES.get(state.lower()).get(activity.name.lower())
    if not activity_rewrite_rules:
        activity_rewrite_rules = COLUMN_RENAME_RULES.get(state.lower()).get(activity.name)
        if not activity_rewrite_rules:
            return

    for original_col, output_column, in activity_rewrite_rules.items():
        if output_column.lower() == 'activity':
            return original_col


def get_activity_name(state, activity, activity_row):
    if activity.use_name_as_activity:
        return activity.name

    activity_col = get_activity_column(activity, state)
    if activity_col and activity_col in activity_row.keys():
        activity_name_row = activity_row[activity_col].tolist()
        if activity_name_row is not None and isinstance(activity_name_row, list):
            activity_name = activity_name_row[0]
            if activity_name and activity_name is not np.nan:
                activity_name = str(activity_name)
                if activity_name in AZ_KEY:
                    return AZ_KEY[activity_name]
                return activity_name


def extract_matches(state, activity, activity_data, grist_data, overlap_report):
    for name, group in overlap_report.groupby("joinidx_0")[["joinidx_1"]]:
        activity_row = activity_data[activity_data['joinidx_0'] == name]
        activity_name = get_activity_name(state, activity, activity_row)

        grist_row_idxs = group['joinidx_1'].tolist()
        grist_rows = grist_data[grist_data['joinidx_1'].isin(grist_row_idxs)].index.tolist()
        for g_row_idx in grist_rows:
            if activity_name:
                try:
                    existing_activity = grist_data.at[g_row_idx, 'activity']
                    if existing_activity is not None:
                        assert 1
                except Exception as err:
                    assert 1
                GRIST_DATA_UPDATE[g_row_idx].add(activity_name)


def find_overlaps(state, activity, activity_data, grist_data):
    try:
        overlapping_regions, left, right = eval_overlap_keep_left(activity_data, grist_data, return_inputs=True)
        activity_data, grist_data = left, right

        return (extract_matches(state, activity, activity_data, grist_data, overlapping_regions)
                if overlapping_regions.shape[0] > 0
                else [])
    except Exception as err:
        print(f'failing on mysterious except in find_overlaps(): {err}')


def match_all_activities(states_data=None, grist_data=None):
    log.info(f'processing states {states_data.keys()}')

    for activity_state, activity_info in states_data.items():
        if not activity_info:
            log.error(f'NO ACTIVITY CONFIG FOR {activity_state}')
            continue

        for activity in tqdm(activity_info.activities):
            if activity_info.scheduler:
                activity.scheduler = activity_info.scheduler

            if not activity_info.use_cache:
                activity.use_cache = activity_info.use_cache

            try:
                activity_data = activity.query_data(STL_COMPARISON_BASE_DIR)
                if activity_data is None or len(activity_data) == 0:
                    log.error(f'NO ACTIVITY DATA FOR {activity_state} {activity.name}')
                    continue

                find_overlaps(activity_state, activity, activity_data, grist_data)
            except Exception as err:
                print(f'random err: {err}')
                assert 1


def main(stl_path: Path, the_out_dir: Path):
    if not the_out_dir.exists():
        the_out_dir.mkdir(parents=True, exist_ok=True)

    global COLUMN_RENAME_RULES
    COLUMN_RENAME_RULES = rewrite_rules

    log.info(f'reading {stl_path}')
    gdf = GristCache(f'{stl_path}').cache_read('stl_file', '.feather')
    if gdf is None:
        gdf = geopandas.read_file(str(stl_path))
        GristCache(f'{stl_path}').cache_write(gdf, 'stl_file', '.feather')

    match_all_activities(STATE_ACTIVITIES, gdf)
    for row_idx, activity_list in GRIST_DATA_UPDATE.items():
        # gdf.at[row_idx, 'activity'] = ','.join(activity_list)
        gdf.loc[row_idx, 'activity'] = ','.join(activity_list)

    if 'joinidx_1' in gdf.columns:
        gdf.drop('joinidx_1', inplace=True, axis=1)
    if 'joinidx_0' in gdf.columns:
        gdf.drop('joinidx_0', inplace=True, axis=1)

    log.info(f'final grist_data row_count: {gdf.shape[0]}')
    gdf.to_csv(str(the_out_dir / 'updated_grist_stl.csv'), index=False)
    gdf.to_file(str(the_out_dir / 'updated_grist_stl.geojson'), driver='GeoJSON')

    log.info(f'original grist_data row_count: {gdf.shape[0]}')


def run():
    print('running stl_activity_match')
    required_envs = ['DATA', 'PYTHONHASHSEED']
    missing_envs = [env for env in required_envs if os.environ.get(env) is None]
    if any(missing_envs):
        raise Exception(f'RequiredEnvVar: The following ENV vars must be set. {missing_envs}')

    data_tld = os.environ.get('DATA')
    data_directory = f'{data_tld}/stl_dataset/step_2'
    base_data_dir = Path(data_directory).resolve()

    global STL_COMPARISON_BASE_DIR, CACHE_DIR
    CACHE_DIR = base_data_dir / 'input/cache'
    STL_COMPARISON_BASE_DIR = base_data_dir / 'input/stl_activity_layers'

    # set cache dir
    GristCache('', CACHE_DIR)

    # stl = base_data_dir / 'input/230815_nationals_STLs/0815_national_stls_deduplicated.geojson'
    stl = base_data_dir / 'input/all-states.geojson'

    out_dir = base_data_dir / 'output'

    main(stl, out_dir)


if __name__ == '__main__':
    run()
