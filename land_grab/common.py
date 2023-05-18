import os

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'

import geopandas as gpd
import pandas as pd
import restapi
import typer

from constants import (
    DATA_SOURCE, ATTRIBUTE_LABEL_TO_FILTER_BY, ATTRIBUTE_CODE_TO_ALIAS_MAP,
    STATE, UNIVERSITY, MANAGING_AGENCY, RIGHTS_TYPE, ATTRIBUTE_FILTER, COLUMNS,
    DOWNLOAD_TYPE, SHAPEFILE_DOWNLOAD_TYPE, API_QUERY_DOWNLOAD_TYPE, LAYER,
    OK_HOLDING_DETAIL_ID, OK_TRUST_FUNDS_ID_MAP, OK_TRUST_FUND_ID,
    OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE, EXISTING_COLUMN_TO_FINAL_COLUMN_MAP)

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
  return f'{_to_kebab_case(state)}-{_to_kebab_case(label)}-{_to_kebab_case(alias)}{filetype}'


def _get_merged_dataset_filename(state=None):
  if state:
    return state.lower() + '-merged.geojson'
  else:
    return 'all-states.geojson'


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

  if source == 'OK-surface':
    gdf = _filter_queried_oklahoma_data(gdf)

  gdf = _format_columns(gdf, config)

  filename = _get_filename(source, label, alias, '.geojson')
  gdf.to_file(cleaned_data_directory + filename, driver='GeoJSON')


def _filter_and_clean_shapefile(gdf, config, source, label, code, alias,
                                cleaned_data_directory):
  if label != '*':
    filtered_gdf = gdf[gdf[label] == code].copy()
  else:
    filtered_gdf = gdf

  filtered_gdf = _format_columns(filtered_gdf, config)

  filename = _get_filename(source, label, alias, '.geojson')
  filtered_gdf.to_file(cleaned_data_directory + filename, driver='GeoJSON')


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

  # clean and filter by the trust funds we care about, 5 for OSU, 5 for
  # langston university
  df = df[[OK_HOLDING_DETAIL_ID, OK_TRUST_FUND_ID]].copy()
  df = df[df[OK_TRUST_FUND_ID].isin([5, 7])]
  df[UNIVERSITY] = df[OK_TRUST_FUND_ID].map(OK_TRUST_FUNDS_ID_MAP)
  df[OK_HOLDING_DETAIL_ID] = df[OK_HOLDING_DETAIL_ID].astype(str)
  return df


def _format_columns(gdf, config):
  '''
  Column formatting used in final dataset
  '''
  # if the initial dataset contains any columns that can be used in our final
  # dataset, rename them to the final dataset column name
  if (config[EXISTING_COLUMN_TO_FINAL_COLUMN_MAP]):
    gdf = gdf.rename(columns=config[EXISTING_COLUMN_TO_FINAL_COLUMN_MAP])

  # add any other data if it exists in the config
  for column in COLUMNS:
    if ((column not in gdf.columns) and config.get(column)):
      gdf[column] = config[column]

  # remove remaining columns
  columns_to_drop = [column for column in gdf.columns if column not in COLUMNS]
  return gdf.drop(columns_to_drop, axis=1)


#############################################
##### helper functions for merging data #####
#############################################


def _merge_dataframes(df_list):
  '''
  Merge multiple dataframes for a state, correctly merging the different
  rights type column values (surface, mineral, etc)
  '''
  # rights_types = pd.unique([df[RIGHTS_TYPE] for df in df_list])
  # find columns to join on
  columns_to_join_on = [
      column for column in COLUMNS
      if column not in [RIGHTS_TYPE, ATTRIBUTE_FILTER]
  ]
  # merged = pd.merge(df1, df2, on=columns_to_join_on, how='outer', indicator=True)
  # merge dataframes one by one until only 1 exists
  while len(df_list) > 1:
    df1 = df_list.pop()
    df2 = df_list.pop()
    merged = pd.merge(df1, df2, on=columns_to_join_on, how='outer')
    df_list.append(merged)

  merged = df_list.pop()

  # if there are any rights type columns in the merged dataset,
  # correctly merge those columns to cintain a readable rights type
  if merged.columns.str.contains(RIGHTS_TYPE).any():
    merged[RIGHTS_TYPE] = merged.apply(_merge_rights_type, axis=1)

  # remove remaining columns
  columns_to_drop = [
      column for column in merged.columns if column not in COLUMNS
  ]
  return merged.drop(columns_to_drop, axis=1)


def _merge_rights_type(row):
  '''
    Correctly merge the rights type columns, removing duplicated, etc
  '''
  # get all rights type values from datasets
  rights_types = row.filter(like=RIGHTS_TYPE).dropna()
  if rights_types.any():
    rights_types = pd.unique(rights_types)
    return '+'.join(rights_types)
  else:
    return None
  # see if there are any rights type columns
  # rights_type_columns = [
  #     column for column in row.index if RIGHTS_TYPE in column
  # ]
  # # if there are rights type columns, get all unique rights types, join them and return
  # if rights_type_columns:
  #   # print(row[rights_type_columns].fillna('').unique())
  #   # return '+'.join(row[rights_type_columns].fillna('').unique())
  #   row = row.fillna('')
  #   rights_type = []
  #   for column in rights_type_columns:
  # for rights_type in rights_types:
  #   if rights_type:
  #     breakpoint()
  #     if row[column]:
  #       rights_type.append(row[column])
  #   rights_type = pd.unique(rights_type)
  #   return '+'.join(rights_type)
  # else:
  #   return None


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
    gdf = gpd.read_file(config[DATA_SOURCE], layer=config.get(LAYER))

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

  filename = _get_merged_dataset_filename(state)
  gdf.to_file(merged_data_directory + filename, driver='GeoJSON')

  return gdf


def merge_all_states_helper(cleaned_data_directory, merged_data_directory):
  state_datasets_to_merge = []
  for state in os.listdir(cleaned_data_directory):
    print(state)
    state_cleaned_data_directory = state_specific_directory(
        cleaned_data_directory, state)
    # TODO: finalize which projection we want the data in
    state_datasets_to_merge.append(
        merge_single_state_helper(state, state_cleaned_data_directory,
                                  merged_data_directory).to_crs('WGS 84'))

  # merged_data_directory = _merged_data_directory()
  # gdfs = []
  # for state in os.listdir(merged_data_directory):
  #   print(merged_data_directory + state)
  #   merged_single_state_file = _merged_data_directory(
  #       state) + get_single_state_merged_filename(state)
  #   gdf = gpd.read_file(merged_single_state_file)
  #   gdfs.append(gdf.to_crs('WGS 84'))
  merged = pd.concat(state_datasets_to_merge, ignore_index=True)
  print(merged)
  filename = _get_merged_dataset_filename()
  merged.to_file(merged_data_directory + filename, driver='GeoJSON')
  return merged