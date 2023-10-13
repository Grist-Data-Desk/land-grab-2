import itertools
import os

import geopandas
import geopandas as gpd
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import ALL_STATES, RIGHTS_TYPE, ACTIVITY, FINAL_DATASET_COLUMNS, \
    GIS_ACRES, \
    ALBERS_EQUAL_AREA, ACRES_TO_SQUARE_METERS, ACRES, OBJECT_ID
from land_grab_2.utilities.overlap import combine_dfs
from land_grab_2.utilities.utils import state_specific_directory

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'


def _get_merged_dataset_filename(state=None, file_extension='.geojson'):
    if state:
        return state.lower() + file_extension
    else:
        return ALL_STATES + file_extension


def take_first_val(column, row):
    """
    Correctly merge a column, aggregating values and removing duplicated values
    """
    # get all rights type values from datasets
    group = row.filter(like=column).dropna()
    if group.any():
        single_val = next((g for g in group if g is not None), None)
        return single_val
    else:
        return None


def _merge_dataframes(df_list):
    """
    Merge multiple dataframes for a state, correctly merging the different
    rights type column values (surface, mineral, etc.)
    """
    if not df_list:
        return geopandas.GeoDataFrame()

    # return the final merged dataset
    merged = df_list[0] if len(df_list) == 1 else combine_dfs(df_list)
    merged = geopandas.GeoDataFrame(merged, geometry=merged.geometry, crs=merged.crs)
    return merged


def _merge_rights_type(row):
    """
    Correctly merge the rights type column, aggregating values and removing duplicated values
    """
    return _merge_rights_row_helper(row, column=RIGHTS_TYPE)


def _merge_activity(row):
    """
    Correctly merge the activity column, aggregating values and removing duplicated values
    """
    return _merge_row_helper(row, column=ACTIVITY)


def _merge_row_helper(row, column):
    """
    Correctly merge a column, aggregating values and removing duplicated values
    """
    # get all rights type values from datasets
    values = row.filter(like=column).dropna()
    if values.any():
        uniq_vals = list(itertools.chain.from_iterable([v.split('+') for v in list(set(values.tolist()))]))
        uniq_vals = sorted([v.strip() for v in uniq_vals])
        values = pd.unique(uniq_vals)
        return '+'.join(values)
    else:
        return None


def _merge_rights_row_helper(row, column):
    """
    Correctly merge a column, aggregating values and removing duplicated values
    """
    # get all rights type values from datasets
    return _merge_row_helper(row, column)


def merge_single_state_helper(state: str, cleaned_data_directory,
                              merged_data_directory):
    if not os.path.exists(merged_data_directory):
        os.makedirs(merged_data_directory)

    gdfs = []

    # find all cleaned datasets for the state
    for file in os.listdir(cleaned_data_directory):
        if file.endswith('.geojson'):
            print(cleaned_data_directory + file)
            gdf = gpd.read_file(cleaned_data_directory + file)
            gdf[GIS_ACRES] = (gdf.to_crs(ALBERS_EQUAL_AREA).area / ACRES_TO_SQUARE_METERS).round(2)

            if not gdf.empty:
                gdfs.append(gdf)

    # merge into a single dataframe, finding and merging any duplicates
    gdf = _merge_dataframes(gdfs)
    print(len(gdf))

    # round acres to 2 decimals
    if ACRES in gdf.columns:
        gdf[ACRES] = gdf[ACRES].round(2)

    # reorder columns to desired order
    final_column_order = [column for column in FINAL_DATASET_COLUMNS if column in gdf.columns]
    gdf = gdf[final_column_order]

    # save to geojson and csv
    gdf.to_file(merged_data_directory + _get_merged_dataset_filename(state), driver='GeoJSON')
    gdf.to_csv(merged_data_directory + _get_merged_dataset_filename(state, '.csv'))

    return gdf


def uniq(row):
    for col in row.keys():
        if isinstance(row[col], list):
            if len(row[col]) == 0:
                # row[col] = None
                pass
            else:
                row[col] = row[col][0]
    return row


def merge_all_states_helper(cleaned_data_directory, merged_data_directory):
    state_datasets_to_merge = []

    # grab data from each state directory
    for state in os.listdir(cleaned_data_directory):
        print(state)
        state_cleaned_data_directory = state_specific_directory(cleaned_data_directory, state)

        merged_state = merge_single_state_helper(state, state_cleaned_data_directory, merged_data_directory)
        merged_state = merged_state.to_crs(ALBERS_EQUAL_AREA)
        state_datasets_to_merge.append(merged_state)

    # merge all states to single geodataframe
    merged = pd.concat(state_datasets_to_merge, ignore_index=True)
    m2 = merged.groupby(['geometry'], as_index=False).agg(list).reset_index()
    m2 = m2.apply(uniq, axis=1)
    merged = gpd.GeoDataFrame(m2, geometry=m2['geometry'], crs=ALBERS_EQUAL_AREA)

    # add a unique object id identifier columns
    merged[OBJECT_ID] = merged.index + 1

    # reorder columns to desired order
    final_column_order = [
        column for column in FINAL_DATASET_COLUMNS if column in merged.columns
    ]
    merged = merged[final_column_order]

    # save to geojson and csv
    merged.to_file(merged_data_directory + _get_merged_dataset_filename(),
                   driver='GeoJSON')
    merged.to_csv(merged_data_directory +
                  _get_merged_dataset_filename(file_extension='.csv'))

    return merged


def merge_cessions_data_helper(cessions_directory):
    # layer = restapi.MapServiceLayer(
    #     'https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TribalCessionLands_01/MapServer/0'
    # )

    # # then filter by specific attributes
    # features = layer.query(outSR=4326, f='geojson', exceed_limit=True)
    # print(f'Found {len(features)} features.')
    # # save json file, may save as json depending on the esri api version, needs 10.3 to save as geojson
    # features.dump(cessions_directory + 'data.json',
    #               indent=2)  # indent allows for pretty view
    gpd.read_file(cessions_directory + 'data.json')
    breakpoint()
