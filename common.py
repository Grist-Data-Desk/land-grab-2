import os

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'

import geopandas as gpd
import pandas as pd
import restapi
import typer

from constants import (
    ATTRIBUTE_LABEL_TO_FILTER_BY, ATTRIBUTE_CODE_TO_ALIAS_MAP, RIGHTS_TYPE,
    TRUST_NAME, COLUMNS, DOWNLOAD_TYPE, SHAPEFILE_DOWNLOAD_TYPE, OBJECT_ID,
    API_QUERY_DOWNLOAD_TYPE, LAYER, OK_HOLDING_DETAIL_ID, OK_TRUST_FUND_ID,
    OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE, EXISTING_COLUMN_TO_FINAL_COLUMN_MAP,
    TOWNSHIP, SECTION, RANGE, MERIDIAN, COUNTY, ALIQUOT, LOCAL_DATA_SOURCE,
    GIS_ACRES, ACRES_TO_SQUARE_METERS, ALBERS_EQUAL_AREA, ACRES, ACTIVITY)

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
    return state.lower() + '-merged' + file_extension
  else:
    return 'all-states' + file_extension


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

  # to get feature set as GeoJson, must set outSR to 4326 for geojson
  # first get the state's metadata by submitting an incorrect query
  features = layer.query(where='OBJECTID=20',
                         outSR=4326,
                         f='geojson',
                         exceed_limit=True)
  features.dump(directory + f'{_to_kebab_case(source)}-metadata.geojson',
                indent=2)  # indent allows for pretty view

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
  # features = layer.query(where="bene_abrev = 'USU'", outSR=4326, f='geojson', exceed_limit=True)

  # count the number of features
  print(f'Found {len(features)} features with {attribute_filter}')

  # save geojson file, may save as json depending on the esri api version, needs 10.3 to saave as geojson
  features.dump(directory + filename, indent=2)  # indent allows for pretty view
  # features.dump('test.json', indent=2) # indent allows for pretty view

  # OR, you can save it directly to a shapefile (does not require arcpy)
  # layer.export_layer('test.shp', where=attribute_filter)


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

  filename = _get_filename(source, label, alias, '.geojson')
  gdf.to_file(cleaned_data_directory + filename, driver='GeoJSON')

  return gdf


def _filter_and_clean_shapefile(gdf, config, source, label, code, alias,
                                cleaned_data_directory):
  # adding projection info for wisconsin
  if source == 'WI':
    gdf = gdf.to_crs(ALBERS_EQUAL_AREA)

  if label != '*':
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


def _filter_queried_oklahoma_data(gdf):
  filter_df = _create_oklahoma_trust_fund_filter()
  # change id from from dictionary to string
  gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].str.replace('}', '')
  gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].str.replace('{', '')
  gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].astype(str)

  # filter dataframe by specific ids
  gdf = gdf[gdf[OK_HOLDING_DETAIL_ID].isin(filter_df[OK_HOLDING_DETAIL_ID])]

  # merge on ids
  gdf = gdf.merge(filter_df, on=OK_HOLDING_DETAIL_ID, how='left')
  return gdf


def _create_oklahoma_trust_fund_filter():
  # get the custom excel file
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
    for root, dirs, files in os.walk(directory_path):
      for file in files:
        file_path = os.path.join(root, file)
        os.remove(file_path)
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

  # get intersection of all columns
  # columns_to_join_on = set.intersection(
  #     *map(set, [df.columns for df in df_list]))
  # for df in df_list:
  #   for column in df.columns:
  #     if df[column].dtype == int:
  #       df[column] = df[column].astype(object)

  # # convert to lists
  # columns_to_join_on = [
  #     column for column in columns_to_join_on if column not in [RIGHTS_TYPE]
  # ]

  # columns_to_join_on = [STATE, UNIVERSITY, GEOMETRY]

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

  # if there are any rights type columns in the merged dataset,
  # correctly merge those columns to cintain a readable rights type
  # if merged.columns.str.contains(RIGHTS_TYPE).any():
  #   merged[RIGHTS_TYPE] = merged.apply(_merge_rights_type, axis=1)

  # remove remaining columns
  # columns_to_drop = [
  #     column for column in merged.columns if column not in COLUMNS
  # ]

  # return the final merged dataset
  merged = df_list.pop()
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