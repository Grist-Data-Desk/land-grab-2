import itertools
import os
from pathlib import Path

import geopandas
import geopandas as gpd
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import ALL_STATES, ACTIVITY, FINAL_DATASET_COLUMNS, \
    GIS_ACRES, \
    ALBERS_EQUAL_AREA, ACRES_TO_SQUARE_METERS, ACRES, OBJECT_ID, TRUST_NAME
from land_grab_2.utilities.overlap import combine_dfs, fix_geometries
from land_grab_2.utilities.utils import state_specific_directory, combine_delim_list

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'


def _get_merged_dataset_filename(state=None, file_extension='.geojson'):
    if state:
        return state.lower() + file_extension
    else:
        return ALL_STATES + file_extension


def _merge_dataframes(df_list):
    """
    Merge multiple dataframes for a state, correctly merging the different
    rights type column values (surface, mineral, etc.)
    """
    if not df_list:
        return geopandas.GeoDataFrame()

    if len(df_list) == 1:
        return df_list[0]

    # return the final merged dataset
    merged = df_list[0] if len(df_list) == 1 else combine_dfs(df_list)
    merged = geopandas.GeoDataFrame(merged, geometry=merged.geometry, crs=merged.crs)
    return merged


def capture_matches(gdf, matches):
    contained_dups = False
    rows_to_be_deleted = set()
    for match_score, grist_idx, grist_row, cmp_row, contains, cmp_idx in matches:
        if contains and grist_row[TRUST_NAME] == cmp_row[TRUST_NAME] and grist_idx != cmp_idx:
            contained_dups = True
            rows_to_be_deleted.add(cmp_idx)
            if ACTIVITY in cmp_row:
                new_activity = cmp_row[ACTIVITY] or ''
                existing = gdf.loc[grist_idx, ACTIVITY] or ''
                gdf.loc[grist_idx, ACTIVITY] = combine_delim_list(existing, new_activity, sep=',')

    gdf_rows = [r for i, r in enumerate(gdf.to_dict(orient='records')) if i not in rows_to_be_deleted]
    df = pd.DataFrame(gdf_rows)
    gdf = geopandas.GeoDataFrame(df, geometry=df.geometry, crs=gdf.crs)

    return gdf, contained_dups


def condense_activities(row):
    for col in row.keys().tolist():
        if ACTIVITY in col:
            row[ACTIVITY] = combine_delim_list('', ','.join(row[ACTIVITY]), sep=',')
        elif 'index' in col:
            continue
        else:
            if isinstance(row[col], list):
                row[col] = None if not row[col] else row[col][0]
    return row


def dedup_single(gdf):
    all_trusts = set(gdf[TRUST_NAME].tolist())
    deduped_groups = []
    for trust in all_trusts:
        gdf_group = gdf[gdf[TRUST_NAME] == trust].reset_index()
        gdf_group = (gdf_group.groupby(['geometry'], as_index=False)
                     .agg(list)
                     .apply(condense_activities, axis=1))
        gdf_group = gpd.GeoDataFrame(gdf_group, geometry=gdf_group['geometry'], crs=gdf.crs)
        deduped_groups.append(gdf_group)

    gdf = _merge_dataframes(deduped_groups).reset_index()

    return gdf


def dedup_group(group):
    if not group:
        return []

    gdf = _merge_dataframes(group)
    gdf = dedup_single(gdf)

    return [gdf]


def merge_single_state_helper(state: str, cleaned_data_directory,
                              merged_data_directory):
    if not os.path.exists(merged_data_directory):
        os.makedirs(merged_data_directory)

    # gdfs = []
    combined_rights_type_gdfs = {'surface': [], 'subsurface': [], 'other': []}

    # find all cleaned datasets for the state
    for file in os.listdir(cleaned_data_directory):
        if file.endswith('.geojson'):
            print(cleaned_data_directory + file)
            gdf = gpd.read_file(cleaned_data_directory + file)
            gdf[GIS_ACRES] = (gdf.to_crs(ALBERS_EQUAL_AREA).area / ACRES_TO_SQUARE_METERS).round(2)

            if not gdf.empty:
                gdf = fix_geometries(gdf)
                file_p = Path(file).resolve()
                if 'subsurface' in file_p.name:
                    combined_rights_type_gdfs['subsurface'].append(gdf)
                elif 'surface' not in file_p.name:
                    combined_rights_type_gdfs['other'].append(gdf)
                else:
                    combined_rights_type_gdfs['surface'].append(gdf)

                # gdfs.append(gdf)

    gdfs = list(itertools.chain.from_iterable([dedup_group(g) for g in combined_rights_type_gdfs.values()]))
    if not gdfs:
        return None

    # merge into a single dataframe, finding and merging any duplicates
    gdf = _merge_dataframes(gdfs)
    print(len(gdf))

    # round acres to 2 decimals
    if ACRES in gdf.columns:
        gdf[ACRES] = gdf[ACRES].map(lambda a: a or 0.0).round(2)

    final_column_order = [column for column in FINAL_DATASET_COLUMNS if column in gdf.columns]
    gdf = fix_geometries(gdf)
    gdf = gdf[final_column_order]

    # save to geojson and csv
    gdf.to_file(merged_data_directory + _get_merged_dataset_filename(state), driver='GeoJSON')
    gdf.to_csv(merged_data_directory + _get_merged_dataset_filename(state, '.csv'))

    return gdf


def merge_all_states_helper(cleaned_data_directory, merged_data_directory):
    state_datasets_to_merge = []

    # grab data from each state directory
    for state in os.listdir(cleaned_data_directory):
        print(state)
        state_cleaned_data_directory = state_specific_directory(cleaned_data_directory, state)
        if not Path(state_cleaned_data_directory).is_dir():
            continue
        merged_state = merge_single_state_helper(state, state_cleaned_data_directory, merged_data_directory)
        if merged_state is None:
            continue
        merged_state = merged_state.to_crs(ALBERS_EQUAL_AREA)
        state_datasets_to_merge.append(merged_state)

    # merge all states to single geodataframe
    merged = pd.concat(state_datasets_to_merge, ignore_index=True).reset_index()
    merged = gpd.GeoDataFrame(merged, geometry=merged['geometry'], crs=ALBERS_EQUAL_AREA)

    # add a unique object id identifier columns
    merged[OBJECT_ID] = merged.index + 1

    final_column_order = [column for column in FINAL_DATASET_COLUMNS if column in merged.columns]
    merged = merged[final_column_order]
    merged = fix_geometries(merged)

    # save to geojson and csv
    merged.to_file(merged_data_directory + _get_merged_dataset_filename(), driver='GeoJSON')
    merged.to_csv(merged_data_directory + _get_merged_dataset_filename(file_extension='.csv'))

    return merged
