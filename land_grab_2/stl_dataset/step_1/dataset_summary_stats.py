import itertools
import os
import traceback
from collections import defaultdict
from pathlib import Path

import geopandas as gpd
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import UNIVERSITY, GIS_ACRES, STATE, DATA_DIRECTORY, UNIVERSITY_SUMMARY, \
    TRIBE_SUMMARY, RIGHTS_TYPE
from land_grab_2.utilities.utils import prettyify_list_of_strings

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'

TRIBE_COMBINE_DETAILS = {
    'Bridgeport Indian Colony, California': 'Bridgeport Paiute Indian Colony of California',
    'Burns Paiute Tribe, Oregon': 'Burns Paiute Tribe of the Burns Paiute Indian Colony of Oregon',
    'Confederated Tribes and Bands of the Yakama Nation': 'Confederated Tribes and Bands of the Yakama Nation, Washington',
    'Nez Perce Tribe, Idaho': 'Nez Perce Tribe of Idaho',
    'Quinault Indian Nation, Washington': 'Quinault Tribe of the Quinault Reservation, Washington',
}


def dedup_tribe_names(tribe_list):
    tribe_list_deduped = list(sorted(set([t
                                          if t not in TRIBE_COMBINE_DETAILS else TRIBE_COMBINE_DETAILS[t]
                                          for t in tribe_list])))

    return tribe_list_deduped


def extract_tribe_list(group, should_join=True):
    if group is None:
        return '' if should_join else []

    raw_tribes = [x for x in list(itertools.chain.from_iterable([i.split(';') for i in group])) if x]
    tribe_list = list(sorted(set([i.strip() for i in raw_tribes])))
    tribe_list = dedup_tribe_names(tribe_list)
    if should_join:
        tribe_list = ';'.join(tribe_list)
    return tribe_list


def count_tribe_list(group):
    return len(extract_tribe_list(group, should_join=False))


def tribe_summary_for_univ_summary(df, col_filter_func, out_column_name):
    # build simpler tribe-listing structure
    tmp_uni_summary = pd.DataFrame()
    for c in [c for c in df.columns.tolist() if col_filter_func(c)]:
        tmp_uni_summary[c] = df.groupby([UNIVERSITY])[c].apply(extract_tribe_list)
    tmp_uni_summary.reset_index(inplace=True)

    # collect tribe-name lists
    out_data = []
    tribes = defaultdict(lambda: defaultdict(list))
    for row in tmp_uni_summary.to_dict(orient='records'):
        univ = row[UNIVERSITY]
        for c in [c for c in tmp_uni_summary.columns.tolist() if col_filter_func(c)]:
            if len(row[c]) > 0:
                tribes[univ]['names'].append(row[c])
        tribe_list = extract_tribe_list(tribes[univ]['names'])
        tribe_count = count_tribe_list(tribes[univ]['names'])
        out_data.append({UNIVERSITY: univ, out_column_name: tribe_list, f'{out_column_name}_count': tribe_count})

    university_summary = pd.DataFrame(out_data, index=None)

    return university_summary


def combine_cession_ids(v):
    raw_nums = set(itertools.chain.from_iterable([c.split(',') if ',' in c else c.split(' ') for c in v.tolist() if c]))
    raw_nums = [n for n in raw_nums if n]
    clean_nums = ','.join(raw_nums)
    return clean_nums


def gather_univ_cessions_nums(df):
    tmp_summary = pd.DataFrame()
    tmp_summary['all_cessions'] = df.groupby([UNIVERSITY])['all_cession_numbers'].apply(combine_cession_ids)
    tmp_summary.reset_index(inplace=True)
    tmp_summary['cession_count'] = tmp_summary['all_cessions'].map(lambda c: len(c.split(',')))
    return tmp_summary


def gis_acres_sum_by_rights_type_for_uni_summary(df):
    records = []
    for univ in set(df.university.tolist()):
        record = {}
        for rt in set(df.loc[df[UNIVERSITY] == univ]['rights_type'].tolist()):
            if len(rt) == 0:
                col_name = f'unknown_rights_type_acres'
            elif '+' in rt:
                col_name = rt.replace('+', '_and_') + '_acres'
            else:
                col_name = f'{rt}_acres'

            relevant_rows = df.loc[(df[UNIVERSITY] == univ) & (df.rights_type == rt)]
            record[col_name] = relevant_rows[GIS_ACRES].sum()
            record[UNIVERSITY] = univ
        records.append(record)

    tmp_summary = pd.DataFrame(records)
    # tmp_summary['surface_acres'] = tmp_summary['surface_acres'] + tmp_summary['subsurface_and_surface_acres']
    # tmp_summary['subsurface_acres'] = tmp_summary['subsurface_acres'] + tmp_summary['subsurface_and_surface_acres']

    return tmp_summary


def university_summary(df, summary_statistics_data_directory=None):
    present_day_tribe_summary = tribe_summary_for_univ_summary(df,
                                                               lambda c: c.endswith('present_day_tribe'),
                                                               'present_day_tribe')
    tribe_named_in_cessions_summary = tribe_summary_for_univ_summary(df,
                                                                     lambda c: 'tribe_named_in_land_cessions' in c,
                                                                     'tribes_named_in_cession')

    uni_summary = present_day_tribe_summary.join(tribe_named_in_cessions_summary.set_index('university'),
                                                 on='university')

    cession_summary = gather_univ_cessions_nums(df)
    uni_summary = uni_summary.join(cession_summary.set_index('university'), on='university')

    rights_type_summary = gis_acres_sum_by_rights_type_for_uni_summary(df)
    uni_summary = uni_summary.join(rights_type_summary.set_index('university'), on='university')

    uni_summary['surface_acres'] = uni_summary['surface_acres'].map(lambda v: round(v, 2))
    uni_summary['subsurface_acres'] = uni_summary['subsurface_acres'].map(lambda v: round(v, 2))
    # uni_summary['subsurface_and_surface_acres'] = uni_summary['subsurface_and_surface_acres'].map(lambda v: round(v, 2))

    # sequence columns
    uni_summary = uni_summary[[
        'university',
        *list(sorted(c for c in uni_summary.columns if c.endswith('_acres'))),
        'present_day_tribe_count',
        'present_day_tribe',
        'tribes_named_in_cession_count',
        'tribes_named_in_cession',
        'cession_count',
        'all_cessions',
    ]]

    uni_summary.to_csv(summary_statistics_data_directory + UNIVERSITY_SUMMARY)
    return uni_summary


def cleanup_gis_acres(row):
    gis_acres = GIS_ACRES if GIS_ACRES in row.keys() else 'acres'
    original_val = row[gis_acres]
    if isinstance(original_val, str) and len(original_val) == 0:
        return None

    if isinstance(original_val, str) and len(original_val) > 0:
        return float(original_val)

    return original_val


def gather_single_tribe_details(row, current_tribe, cession_number_col):
    try:
        gis_acres_val = cleanup_gis_acres(row)
        current_tribe = (current_tribe
                         if current_tribe not in TRIBE_COMBINE_DETAILS
                         else TRIBE_COMBINE_DETAILS[current_tribe])
        return {
            GIS_ACRES: gis_acres_val,
            'present_day_tribe': current_tribe,
            UNIVERSITY: row[UNIVERSITY],
            STATE: row[STATE],
            'cession_number': row[cession_number_col]
        }
    except Exception as err:
        print(traceback.format_exc())
        print(err)


def construct_single_tribe_info(row):
    try:
        present_day_tribe_cols = [c for c in row.keys() if 'present_day_tribe' in c]
        tribe_cession_number_cols = [c for c in row.keys() if 'cession_num' in c and 'all' not in c]

        tribe_records = []
        for present_day_tribe_col, cession_number_col in zip(present_day_tribe_cols, tribe_cession_number_cols):
            current_tribe = row[present_day_tribe_col]
            if not isinstance(current_tribe, str) or (isinstance(current_tribe, str) and len(current_tribe) == 0):
                continue

            if ';' in current_tribe:
                records = [
                    gather_single_tribe_details(row, t.strip(), cession_number_col)
                    for t in current_tribe.split(';')
                ]
                tribe_records += [r for r in records if r is not None]
            else:
                res = gather_single_tribe_details(row, current_tribe, cession_number_col)
                if res is not None:
                    tribe_records.append(res)

        return tribe_records
    except Exception as err:
        print(err)


def gis_acres_sum_by_rights_type_tribe_summary(df):
    present_day_tibe_cols = [c for c in df.columns if c.endswith('present_day_tribe')]
    tribe_land_accounts = defaultdict(dict)
    for row in df.to_dict(orient='records'):
        tribe_list = extract_tribe_list([row[c] for c in present_day_tibe_cols], should_join=False)
        for tribe in tribe_list:
            rights_type = 'unknown_rights_type' if RIGHTS_TYPE not in row or not row[RIGHTS_TYPE] else row[RIGHTS_TYPE]
            if '+' in rights_type:
                rights_type = rights_type.replace('+', '_and_')

            out_col_name = f'{rights_type}_acres'
            if rights_type not in tribe_land_accounts[tribe]:
                tribe_land_accounts[tribe][out_col_name] = float(row[GIS_ACRES])
            else:
                tribe_land_accounts[tribe][out_col_name] += float(row[GIS_ACRES])

    records = [{'present_day_tribe': tribe, **land_info} for tribe, land_info in tribe_land_accounts.items()]

    tmp_summary = pd.DataFrame(records)
    tmp_summary['surface_acres'] = tmp_summary['surface_acres'] # + tmp_summary['subsurface_and_surface_acres']
    tmp_summary['subsurface_acres'] = tmp_summary['subsurface_acres'] # + tmp_summary['subsurface_and_surface_acres']

    tmp_summary['surface_acres'] = tmp_summary['surface_acres'].map(lambda v: round(v, 2))
    tmp_summary['subsurface_acres'] = tmp_summary['subsurface_acres'].map(lambda v: round(v, 2))
    # tmp_summary['subsurface_and_surface_acres'] = tmp_summary['subsurface_and_surface_acres'].map(lambda v: round(v, 2))

    return tmp_summary


def tribe_summary(df, summary_statistics_data_directory, univ_summary):
    results = list(itertools.chain.from_iterable([
        construct_single_tribe_info(row.to_dict())
        for _, row in df.iterrows()
    ]))
    tribe_summary_tmp = pd.DataFrame(results)
    group_cols = [c for c in list(tribe_summary_tmp.columns) if GIS_ACRES not in c and 'cession_number' not in c]
    tribe_summary_semi_aggd = tribe_summary_tmp.groupby(group_cols)[GIS_ACRES].sum().reset_index()
    tribe_summary_semi_aggd.to_csv(summary_statistics_data_directory + TRIBE_SUMMARY)

    tribe_summary_full_agg = tribe_summary_tmp.groupby(['present_day_tribe']).agg(list).reset_index()
    tribe_summary_full_agg[GIS_ACRES] = tribe_summary_full_agg[GIS_ACRES].map(sum)
    tribe_summary_full_agg = tribe_summary_full_agg.apply(prettyify_list_of_strings, axis=1)
    tribe_summary_full_agg['cession_count'] = tribe_summary_full_agg['cession_number'].map(lambda v: len(v.split(',')))
    rights = gis_acres_sum_by_rights_type_tribe_summary(df)
    tribe_summary_full_agg = tribe_summary_full_agg.join(rights.set_index('present_day_tribe'), on='present_day_tribe')

    # sequence columns
    tribe_summary_full_agg = tribe_summary_full_agg[[
        'present_day_tribe',
        'cession_count',
        'cession_number',
        *list(sorted(c for c in tribe_summary_full_agg.columns if c.endswith('_acres') and GIS_ACRES not in c)),
        'university',
        'state',
    ]]

    tribe_summary_full_agg.to_csv(summary_statistics_data_directory + 'tribe-summary-condensed.csv')


def calculate_summary_statistics_helper(summary_statistics_data_directory, merged_data_directory):
    '''
    Calculate summary statistics based on the full dataset. Create two csvs. In the first,
    for each university calculate total acreage of land held in trust, all present day tribes
    and tribes listed in treaties associated with the university land, and which cessions
    (represented by Royce IDs) overlap with land held in trust. In the second, for each present
    day tribe, get total acreage of state land trust parcels, all associated cessions, and all
    states and universities that have land taken from this tribe held in trust
    '''

    # df_0 = gpd.read_file(merged_data_directory + _get_merged_dataset_filename())
    df_0 = gpd.read_file(DATA_DIRECTORY + '/national_stls.csv')  # TODO: parameterize

    df = df_0.copy(deep=True)
    df_1 = df_0.copy(deep=True)

    stats_dir = Path(summary_statistics_data_directory).resolve()
    if not stats_dir.exists():
        stats_dir.mkdir(parents=True, exist_ok=True)

    gis_acres_col = GIS_ACRES if GIS_ACRES in df.columns else 'gis_calculated_acres'
    df[GIS_ACRES] = df[gis_acres_col].astype(float)

    univ_summary = university_summary(df, summary_statistics_data_directory)
    tribe_summary(df_1, summary_statistics_data_directory, univ_summary)
