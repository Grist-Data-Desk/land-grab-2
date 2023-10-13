import itertools
import json
import os
import traceback
from pathlib import Path

import geopandas as gpd
import pandas as pd
from compose import compose

from land_grab_2.stl_dataset.step_1.constants import UNIVERSITY, GIS_ACRES, STATE, DATA_DIRECTORY, UNIVERSITY_SUMMARY, \
    TRIBE_SUMMARY
from land_grab_2.utilities.utils import prettyify_list_of_strings

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'


def extract_tribe_list(group, should_join=True):
    if group is None:
        return '' if should_join else []

    raw_tribes = [x for x in list(itertools.chain.from_iterable([i.split(';') for i in group])) if x]
    tribe_list = set([i.strip() for i in raw_tribes])
    if should_join:
        tribe_list = ';'.join(tribe_list)
    return tribe_list


def count_tribe_list(group):
    return len(extract_tribe_list(group, should_join=False))


def present_day_tribe(df, university_summary):
    for c in [c for c in df.columns.tolist() if 'present_day_tribe' in c]:
        university_summary[c] = df.groupby([UNIVERSITY])[c].apply(extract_tribe_list)
        university_summary[f'{c}_count'] = df.groupby([UNIVERSITY])[c].apply(count_tribe_list)
    return university_summary


def tribe_named_in_land_cession(df, university_summary):
    for c in [c for c in df.columns.tolist() if 'tribe_named_in_land_cessions' in c]:
        university_summary[c] = df.groupby([UNIVERSITY])[c].apply(extract_tribe_list)
        university_summary[f'{c}_count'] =  df.groupby([UNIVERSITY])[c].apply(count_tribe_list)
    return university_summary


def combine_cession_ids(v):
    return ','.join(set(itertools.chain.from_iterable([c.split(',') for c in v.tolist() if c])))


def gather_univ_cessions_nums(df, university_summary):
    university_summary['all_univ_cession_nums'] = df.groupby([UNIVERSITY])['all_cession_numbers'].apply(
        combine_cession_ids
    )
    return university_summary


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


def pivot_on_tribe(df):
    results = list(itertools.chain.from_iterable([
        construct_single_tribe_info(row.to_dict())
        for _, row in df.iterrows()
    ]))
    tribe_summary_tmp = pd.DataFrame(results)
    group_cols = [c for c in list(tribe_summary_tmp.columns) if GIS_ACRES not in c and 'cession_number' not in c]
    tribe_summary_semi_aggd = tribe_summary_tmp.groupby(group_cols)[GIS_ACRES].sum().reset_index()
    # tribe_summary['cession_number'] = tribe_summary.groupby(group_cols)['cession_number'].agg(lambda g: g)

    tribe_summary_full_agg = tribe_summary_tmp.groupby(['present_day_tribe']).agg(list).reset_index()
    tribe_summary_full_agg[GIS_ACRES] = tribe_summary_full_agg[GIS_ACRES].map(sum)
    tribe_summary_full_agg = tribe_summary_full_agg.apply(prettyify_list_of_strings, axis=1)

    return tribe_summary_semi_aggd, tribe_summary_full_agg


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

    # create first csv: university summary
    university_summary = pd.DataFrame()
    university_summary = present_day_tribe(df, university_summary)
    university_summary = tribe_named_in_land_cession(df, university_summary)
    university_summary = gather_univ_cessions_nums(df, university_summary)
    university_summary[GIS_ACRES] = df.groupby([UNIVERSITY])[GIS_ACRES].sum()
    university_summary.to_csv(summary_statistics_data_directory + UNIVERSITY_SUMMARY)

    # second csv: tribal summary
    tribe_summary_semi_aggd, tribe_summary_full_agg = pivot_on_tribe(df_1)
    tribe_summary_semi_aggd.to_csv(summary_statistics_data_directory + TRIBE_SUMMARY)
    tribe_summary_full_agg.to_csv(summary_statistics_data_directory + 'tribe-summary-condensed.csv')
