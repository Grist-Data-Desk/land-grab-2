import os

import geopandas
import geopandas as gpd
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import ALL_STATES, RIGHTS_TYPE, ACTIVITY, COLUMNS, GIS_ACRES, \
    ALBERS_EQUAL_AREA, ACRES_TO_SQUARE_METERS, ACRES, OBJECT_ID
from land_grab_2.utilities.utils import prettyify_list_of_strings, state_specific_directory

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'


def _get_merged_dataset_filename(state=None, file_extension='.geojson'):
    if state:
        return state.lower() + file_extension
    else:
        return ALL_STATES + file_extension


def take_first_val(row):
    for col in row.keys():
        if 'activity' not in col:
            if isinstance(row[col], list):
                if len(row[col]) == 0:
                    # row[col] = None
                    pass
                else:
                    row[col] = row[col][0]

    return row


def condense_activity(merged):
    if 'activity' not in merged.columns:
        return merged

    # chlk = ['parcel', 'parcelid', 'globalid', 'objectid']
    # groupby_col = next((c for c in merged.columns for l in chlk if l.lower() in c.lower()), None)
    # if not groupby_col:
    #     return merged

    # m2 = merged.dissolve(by=groupby_col, aggfunc=list).reset_index()
    # m2 = merged.groupby([groupby_col, 'geometry'], as_index=False).agg(list).reset_index()
    m2 = merged.groupby(['geometry'], as_index=False).agg(list).reset_index()
    m2 = m2.apply(take_first_val, axis=1)
    m2[ACTIVITY] = m2.activity.map(lambda v: prettyify_list_of_strings({'activity': v})['activity'])
    # m2['rights_type'] = m2.rights_type.map(lambda v: prettyify_list_of_strings({'activity': v})['activity'])
    m2 = gpd.GeoDataFrame(m2, geometry=m2['geometry'], crs=merged.crs)
    return m2


def _merge_dataframes(df_list):
    '''
    Merge multiple dataframes for a state, correctly merging the different
    rights type column values (surface, mineral, etc)
    '''

    # merge dataframes one by one until only 1 exists
    while len(df_list) > 1:
        # get the first two datasets
        df1 = df_list.pop()
        df2 = df_list.pop()

        # get intersection of all columns between these two datasets
        columns_to_join_on = set.intersection(
            *map(set, [df.columns for df in [df1, df2]]))
        for df in [df1, df2]:
            for column in df.columns:
                if df[column].dtype == int:
                    df[column] = df[column].astype(object)

        # convert to lists
        columns_to_join_on = [
            column for column in columns_to_join_on
            if column not in [RIGHTS_TYPE, ACTIVITY]
        ]

        # merge on these columns
        merged = pd.merge(df1, df2, on=columns_to_join_on, how='outer')

        # if there are any rights type columns in the merged dataset,
        # correctly merge those columns to contain a readable rights type
        if merged.columns.str.contains(RIGHTS_TYPE).any():
            merged[RIGHTS_TYPE] = merged.apply(_merge_rights_type, axis=1)

        # if there are any activity columns in the merged dataset,
        # correctly merge those columns to contain a readable activity
        if merged.columns.str.contains(ACTIVITY).any():
            merged[ACTIVITY] = merged.apply(_merge_activity, axis=1)

        # remove remaining columns
        columns_to_drop = [
            column for column in merged.columns if column not in COLUMNS
        ]
        merged = merged.drop(columns_to_drop, axis=1)

        df_list.append(merged)

    # return the final merged dataset
    merged = df_list.pop()
    merged = merged.drop_duplicates()
    merged = geopandas.GeoDataFrame(merged)
    return merged


def _merge_rights_type(row):
    '''
    Correctly merge the rights type column, aggregating values and removing duplicated values
    '''
    return _merge_row_helper(row, column=RIGHTS_TYPE)


def _merge_activity(row):
    '''
    Correctly merge the activity column, aggregating values and removing duplicated values
    '''
    return _merge_row_helper(row, column=ACTIVITY)


def _merge_row_helper(row, column):
    '''
    Correctly merge a column, aggregating values and removing duplicated values
    '''
    # get all rights type values from datasets
    values = row.filter(like=column).dropna()
    if values.any():
        values = pd.unique(values)
        return '+'.join(values)
    else:
        return None


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
            print(len(gdf))
            if not gdf.empty:
                gdfs.append(gdf)

    # merge into a single dataframe, finding and merging any duplicates
    gdf = _merge_dataframes(gdfs)
    print(len(gdf))

    # compute gis calculated areas, rounded to 2 decimals
    gdf[GIS_ACRES] = (gdf.to_crs(ALBERS_EQUAL_AREA).area /
                      ACRES_TO_SQUARE_METERS).round(2)
    # round acres to 2 decimals
    if ACRES in gdf.columns:
        gdf[ACRES] = gdf[ACRES].round(2)

    # reorder columns to desired order
    final_column_order = [column for column in COLUMNS if column in gdf.columns]
    gdf = gdf[final_column_order]

    # save to geojson and csv
    gdf.to_file(merged_data_directory + _get_merged_dataset_filename(state),
                driver='GeoJSON')
    gdf.to_csv(merged_data_directory +
               _get_merged_dataset_filename(state, '.csv'))

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
        state_cleaned_data_directory = state_specific_directory(
            cleaned_data_directory, state)

        state_datasets_to_merge.append(
            merge_single_state_helper(
                state, state_cleaned_data_directory,
                merged_data_directory).to_crs(ALBERS_EQUAL_AREA))

    # merge all states to single geodataframe
    merged = pd.concat(state_datasets_to_merge, ignore_index=True)
    # merged = condense_activity(merged)
    m2 = merged.groupby(['geometry'], as_index=False).agg(list).reset_index()
    m2 = m2.apply(uniq, axis=1)
    merged = gpd.GeoDataFrame(m2, geometry=m2['geometry'], crs=merged.crs)

    # add a unique object id identifier columns
    merged[OBJECT_ID] = merged.index + 1

    # reorder columns to desired order
    final_column_order = [
        column for column in COLUMNS if column in merged.columns
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
    # # save json file, may save as json depending on the esri api version, needs 10.3 to saave as geojson
    # features.dump(cessions_directory + 'data.json',
    #               indent=2)  # indent allows for pretty view
    gdf = gpd.read_file(cessions_directory + 'data.json')
    breakpoint()
