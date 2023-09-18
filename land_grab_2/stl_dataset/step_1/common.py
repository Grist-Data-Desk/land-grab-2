import itertools
import json
import os
import shutil
import traceback

from pathlib import Path

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'

import geopandas as gpd
import pandas as pd
import restapi
from compose import compose
import typer

from land_grab_2.stl_dataset.step_1.constants import (
    ATTRIBUTE_LABEL_TO_FILTER_BY, ATTRIBUTE_CODE_TO_ALIAS_MAP, RIGHTS_TYPE,
    TRUST_NAME, COLUMNS, DOWNLOAD_TYPE, SHAPEFILE_DOWNLOAD_TYPE, OBJECT_ID,
    API_QUERY_DOWNLOAD_TYPE, LAYER, OK_HOLDING_DETAIL_ID, OK_TRUST_FUND_ID,
    OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE, EXISTING_COLUMN_TO_FINAL_COLUMN_MAP,
    TOWNSHIP, SECTION, RANGE, MERIDIAN, COUNTY, ALIQUOT, LOCAL_DATA_SOURCE,
    GIS_ACRES, ACRES_TO_SQUARE_METERS, ALBERS_EQUAL_AREA, ACRES, ACTIVITY,
    UNIVERSITY, STATE, ALL_STATES, UNIVERSITY_SUMMARY, TRIBE_SUMMARY, DATA_DIRECTORY)

app = typer.Typer()


######################################################
##### helper functions for returning filenames ######
######################################################


def _to_kebab_case(string):
    '''convert string to kebab case'''
    if '_' in string:
        return "-".join(string.lower().split('_'))
    else:
        return "-".join(string.lower().split())


def _get_filename(state, label, alias, filetype):
    '''return a filename in kebabcase'''
    if alias:
        return f'{_to_kebab_case(state)}-{_to_kebab_case(label)}-{_to_kebab_case(alias)}{filetype}'
    else:
        return f'{_to_kebab_case(state)}-{_to_kebab_case(label)}{filetype}'


def _get_merged_dataset_filename(state=None, file_extension='.geojson'):
    if state:
        return state.lower() + file_extension
    else:
        return ALL_STATES + file_extension


##############################################
##### function for returning directories #####
##############################################


def state_specific_directory(directory, state=None):
    if state:
        return directory + f'{state}/'
    else:
        return directory


######################################################
##### helper functions for querying rest servers #####
######################################################


def _query_arcgis_restapi(config, source, label, code, alias, directory):
    '''
    Query available arcgis restapi's with relevant filters
    '''
    # create a descriptive filename to store query info
    filename = _get_filename(source, label, alias, '.geojson')

    # data_source for specific Map Server
    data_source = config['data_source']
    layer = restapi.MapServiceLayer(data_source)

    # create desired attribute conditions to filter the query by
    attribute_filter = f'{label}={code}'

    # then filter by specific attributes
    if code == '*':
        features = layer.query(outSR=4326, f='geojson', exceed_limit=True)
    else:
        features = layer.query(where=attribute_filter,
                               outSR=4326,
                               f='geojson',
                               exceed_limit=True)

    # count the number of features
    print(f'Found {len(features)} features with {attribute_filter}')

    # save geojson file, may save as json depending on the esri api version, needs 10.3 to saave as geojson
    features.dump(directory + filename, indent=2)  # indent allows for pretty view


#############################################################
##### helper functions for cleaning and formatting data #####
#############################################################


def _clean_queried_data(source, config, label, alias, queried_data_directory,
                        cleaned_data_directory):
    '''
    Clean data queried from restapis
    '''

    filename = _get_filename(source, label, alias, '.json')
    gdf = gpd.read_file(queried_data_directory + filename)

    if gdf.empty:
        return gdf

    # custom cleaning
    if source == 'OK-surface':
        gdf = _filter_queried_oklahoma_data(gdf)
        gdf = _get_ok_surface_town_range(gdf)
    elif source == 'OK-unleased-mineral-lands':
        gdf = _filter_queried_oklahoma_data_unleased_min_lands(gdf)
        gdf = _get_ok_surface_town_range(gdf)
    elif source == 'OK-real-estate-subdivs':
        gdf = _filter_queried_oklahoma_data_unleased_min_lands(gdf)
        gdf = _get_ok_surface_town_range(gdf)
    elif source == 'OK-mineral-subdivs':
        gdf = _filter_queried_oklahoma_data_unleased_min_lands(gdf)
        gdf = _get_ok_surface_town_range(gdf)
    elif 'AZ' in source:
        gdf = _get_az_town_range_section(gdf)
    elif 'MT' in source:
        gdf = _get_mt_town_range_section(gdf)
    elif source == 'OK-subsurface':
        gdf = _get_ok_subsurface_town_range(gdf)
    elif 'OR' in source:
        gdf = _get_or_town_range_section(gdf)
    elif 'UT' in source:
        gdf = _get_ut_town_range_section_county(gdf)

    gdf = _format_columns(gdf, config, alias)

    if not gdf.empty:
        filename = _get_filename(source, label, alias, '.geojson')
        gdf.to_file(cleaned_data_directory + filename, driver='GeoJSON')

    return gdf


def _filter_and_clean_shapefile(gdf, config, source, label, code, alias,
                                cleaned_data_directory):
    # adding projection info for wisconsin
    if source == 'WI':
        gdf = gdf.to_crs(ALBERS_EQUAL_AREA)

    if code != '*':
        filtered_gdf = gdf[gdf[label] == code].copy()
    else:
        filtered_gdf = gdf

    if filtered_gdf.empty:
        return filtered_gdf

    # custom cleaning
    if source == 'NE':
        filtered_gdf = _get_ne_town_range_section(filtered_gdf)
    elif source == 'WI':
        filtered_gdf = _get_wi_town_range_section_aliquot(filtered_gdf)
    elif 'MT' in source:
        filtered_gdf = _get_mt_town_range_section(filtered_gdf)
    elif 'SD' in source:
        filtered_gdf = _get_sd_town_range_meridian(filtered_gdf)
        filtered_gdf = _get_sd_rights_type(filtered_gdf)

    filtered_gdf = _format_columns(filtered_gdf, config, alias)

    # more custom cleaning
    if 'NM' in source:
        filtered_gdf = _clean_nm_town_range(filtered_gdf)

    filename = _get_filename(source, label, alias, '.geojson')
    filtered_gdf.to_file(cleaned_data_directory + filename, driver='GeoJSON')

    return filtered_gdf


def _format_columns(gdf, config, alias):
    '''
    Column formatting used in final dataset
    '''
    # if the initial dataset contains any columns that can be used in our final
    # dataset, rename them to the final dataset column name
    if config.get(EXISTING_COLUMN_TO_FINAL_COLUMN_MAP):
        gdf = gdf.rename(columns=config[EXISTING_COLUMN_TO_FINAL_COLUMN_MAP])

    # add any other data if it exists in the config
    for column in COLUMNS:
        if ((column not in gdf.columns) and config.get(column)):
            gdf[column] = config[column]

    # remove remaining columns
    columns_to_drop = [column for column in gdf.columns if column not in COLUMNS]

    # add trust name columns
    if alias:
        gdf[TRUST_NAME] = alias
    return gdf.drop(columns_to_drop, axis=1)


###########################################################
########### state specific cleaning functions ############
###########################################################


def _get_az_town_range_section(gdf):
    # arizona data has a 'trs' column which is composed of township, range, and section
    # split by ' - ' so we expand this into three columns
    split = gdf['trs'].str.split(' - ', expand=True)
    gdf[TOWNSHIP] = split[0]
    gdf[RANGE] = split[1]
    gdf[SECTION] = split[2]
    return gdf


def _get_mt_town_range_section(gdf):
    # mt data has a 'STRID' column which is composed of township, range, and section
    # split by ' ' so we expand this into three columns
    split = gdf['STRID'].str.split(' ', expand=True)
    gdf[TOWNSHIP] = split[0]
    gdf[RANGE] = split[1]
    gdf[SECTION] = split[2]
    return gdf


def _get_ne_town_range_section(gdf):
    # ne data has a 'STR' column which is composed of township, range, and section
    # split by ' ' so we expand this into three columns
    split = gdf['STR'].str.split('-', expand=True)
    gdf[SECTION] = split[0]
    gdf[TOWNSHIP] = split[1]
    gdf[RANGE] = split[2]
    return gdf


def _clean_nm_town_range(gdf):
    # nm section and range data has extra leading and trailing zeros in a funny way
    # # for example Range 11E is formatted 0110E. So we remove the extra zeros here.
    for column in [RANGE, TOWNSHIP]:
        gdf[column] = gdf[column].str.slice(start=1,
                                            stop=3) + gdf[column].str.slice(start=4)
    return gdf


def _get_ok_surface_town_range(gdf):
    '''
    OK surface data has township and range divided into two parts, so merge those parts
    '''
    gdf[TOWNSHIP] = gdf['Township'].astype(str) + gdf['TownshipDirection']
    gdf[RANGE] = gdf['Range'].astype(str) + gdf['RangeDirection']
    return gdf


def _get_ok_subsurface_town_range(gdf):
    '''
    OK subsurface data has section, township, range and meridian together in a certain format
    ex: "STRM": "31-09N-25EIM"
    '''
    split = gdf['STRM'].str.split('-', expand=True)
    gdf[SECTION] = split[0]
    gdf[TOWNSHIP] = split[1]
    gdf[RANGE] = split[2].str.slice(stop=3)
    gdf[MERIDIAN] = split[2].str.slice(start=3, stop=4)
    return gdf


def _get_or_town_range_section(gdf):
    '''
    data has a 'TRS' column which is composed of township, range, and section
    but the format is wacky
    '''
    trs = pd.DataFrame(gdf['TRS'].apply(split_trs).tolist())
    gdf[TOWNSHIP] = trs[0]
    gdf[RANGE] = trs[1]
    gdf[SECTION] = trs[2]
    return gdf


def split_trs(trs):
    section, township, range = '', '', ''
    if len(trs) == 7:
        township = trs[:3]
        range = trs[3:5]
        section = trs[5:]
    else:
        township = trs[:3]
        range = trs[3:6]
        section = trs[6:]

    return township, range, section


def _get_ut_town_range_section_county(gdf):
    '''
    data has a 'TRS_LABEL' column which is composed of township, range, sectionm meridian
    '''
    # first clean county name
    gdf[COUNTY] = gdf['county_name'].str.strip()

    split = gdf['TRS_LABEL'].str.split(' ', expand=True)
    gdf[SECTION] = split[2].str.slice(start=3)

    township_split = split[0].str.split('.', expand=True)
    gdf[TOWNSHIP] = township_split[0].str.slice(
        start=1) + township_split[1].str.slice(start=-1)

    range_split = split[1].str.split('.', expand=True)
    gdf[RANGE] = range_split[0].str.slice(start=1) + range_split[1].str.slice(
        start=-1)
    gdf[MERIDIAN] = split[3]
    return gdf


def _get_wi_town_range_section_aliquot(gdf):
    '''
    WI subsurface data has section, township, range and maliquot together in a certain format
    under the 'PARCEL_DES' label
    '''
    split = gdf['PARCEL_DES'].str.split(' ', expand=True)

    gdf[SECTION] = split[6]
    gdf[TOWNSHIP] = split[0].str.slice(start=1)
    gdf[RANGE] = split[2].str.slice(start=1)
    gdf[ALIQUOT] = split[9]
    return gdf


def _get_sd_town_range_meridian(gdf):
    '''
    SD data has meridian, township, range together in a certain format in the PLSSID field
    ex: "SD051130N0810W0": where the meridian is 5, township is 113N, range is 81W
    '''
    gdf[MERIDIAN] = gdf['PLSSID'].str.slice(start=3, stop=4)
    gdf[TOWNSHIP] = gdf['PLSSID'].str.slice(
        start=4, stop=7).str.strip('0') + gdf['PLSSID'].str.slice(start=8, stop=9)
    gdf[RANGE] = gdf['PLSSID'].str.slice(
        start=9, stop=12).str.strip('0') + gdf['PLSSID'].str.slice(start=13,
                                                                   stop=14)

    return gdf


def _get_sd_rights_type(gdf):
    '''
    get and clean SD rights types to be consistent with the rest of the dataset
    '''
    gdf[RIGHTS_TYPE] = gdf['match_type'].str.replace('both', 'surface+subsurface')
    gdf[RIGHTS_TYPE] = gdf[RIGHTS_TYPE].str.lower()
    return gdf


def _filter_queried_oklahoma_data_unleased_min_lands(gdf):
    filter_df = pd.read_csv(OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE)

    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].str.replace('}', '')
    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].str.replace('{', '')
    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].astype(str)

    # filter dataframe by specific ids
    gdf = gdf[gdf[OK_HOLDING_DETAIL_ID].isin(filter_df[OK_HOLDING_DETAIL_ID])]

    # merge on ids
    gdf = gdf.merge(filter_df[[OK_HOLDING_DETAIL_ID, 'LeaseType']], how='left', on=OK_HOLDING_DETAIL_ID)
    gdf[ACTIVITY] = gdf['LeaseType']
    return gdf


def _filter_queried_oklahoma_data(gdf):
    filter_df = _create_oklahoma_trust_fund_filter()
    # change id from dictionary to string
    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].str.replace('}', '')
    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].str.replace('{', '')
    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].astype(str)

    # filter dataframe by specific ids
    gdf = gdf[gdf[OK_HOLDING_DETAIL_ID].isin(filter_df[OK_HOLDING_DETAIL_ID])]

    # merge on ids
    gdf = gdf.merge(filter_df, on=OK_HOLDING_DETAIL_ID, how='left')
    return gdf


def _create_oklahoma_trust_fund_filter():
    # get the custom Excel file
    df = pd.read_excel(OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE)

    # clean and filter by the trust funds we care about, 5 for OSU
    df = df[[OK_HOLDING_DETAIL_ID, OK_TRUST_FUND_ID]].copy()
    df = df[df[OK_TRUST_FUND_ID].isin([5])]
    df[OK_HOLDING_DETAIL_ID] = df[OK_HOLDING_DETAIL_ID].astype(str)
    return df


###################################################
##### helper functions for cleaning directory #####
###################################################


def delete_files_and_subdirectories_in_directory(directory_path):
    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_file():
                    os.unlink(entry.path)
                else:
                    shutil.rmtree(entry.path)
        print("All files and subdirectories deleted successfully.")
    except OSError:
        print("Error occurred while deleting files and subdirectories.")


#############################################
##### helper functions for merging data #####
#############################################


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


#################################################################
###### helper functions for final dataset creation commands #####
#################################################################


def extract_and_clean_single_source_helper(source: str, config: dict,
                                           queried_data_directory: str,
                                           cleaned_data_directory: str):
    # create the correct data directories
    if not os.path.exists(queried_data_directory):
        os.makedirs(queried_data_directory)

    if not os.path.exists(cleaned_data_directory):
        os.makedirs(cleaned_data_directory)

    # if downloading shapefile
    if config[DOWNLOAD_TYPE] == SHAPEFILE_DOWNLOAD_TYPE:
        gdf = gpd.read_file(config[LOCAL_DATA_SOURCE], layer=config.get(LAYER))

    for label in config[ATTRIBUTE_LABEL_TO_FILTER_BY]:
        for code, alias in config[ATTRIBUTE_CODE_TO_ALIAS_MAP].items():

            # if querying from rest api
            if config[DOWNLOAD_TYPE] == API_QUERY_DOWNLOAD_TYPE:

                _query_arcgis_restapi(config, source, label, code, alias,
                                      queried_data_directory)

                _clean_queried_data(source, config, label, alias,
                                    queried_data_directory, cleaned_data_directory)

            # if cleaning a shapefile
            elif config[DOWNLOAD_TYPE] == SHAPEFILE_DOWNLOAD_TYPE:

                _filter_and_clean_shapefile(gdf, config, source, label, code, alias,
                                            cleaned_data_directory)


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


def present_day_tribe(df, university_summary):
    uniq_no_blanks = compose(lambda s: ','.join([json.dumps(i) for i in s if i]), set)
    for c in [c for c in df.columns.tolist() if 'present_day_tribe' in c]:
        university_summary[c] = df.groupby([UNIVERSITY])[c].apply(uniq_no_blanks)
        university_summary[f'{c}_count'] = df.groupby([UNIVERSITY])[c].nunique()
    return university_summary


def tribe_named_in_land_cession(df, university_summary):
    uniq_no_blanks = compose(lambda s: ','.join([i for i in s if i]), set)
    for c in [c for c in df.columns.tolist() if 'tribe_named_in_land_cessions' in c]:
        university_summary[c] = df.groupby([UNIVERSITY])[c].apply(uniq_no_blanks)
        university_summary[f'{c}_count'] = df.groupby([UNIVERSITY])[c].nunique()
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


def prettyify_list_of_strings(row):
    for col in row.keys():
        if isinstance(row[col], list):
            row[col] = ', '.join(list(set(row[col])))
    return row


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
