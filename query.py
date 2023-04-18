import os

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'

import geopandas as gpd
import restapi
import typer

from config import QUERY_CONFIGS, STATE, UNIVERSITY, MANAGING_AGENCY, RIGHTS_TYPE, ATTRIBUTE_FILTER, COLUMNS


def to_kebab_case(value):
  '''convert string to kebab case'''
  if '_' in value:
    return "-".join(value.lower().split('_'))
  else:
    return "-".join(value.lower().split())


def get_filename(state, label, alias, filetype):
  '''return a filename in kebabcase'''
  return f'{to_kebab_case(state)}-{to_kebab_case(label)}-{to_kebab_case(alias)}{filetype}'


def get_query_data_directory(query_config):
  state = query_config[STATE]
  return f'query-data/{state}/'


def get_cleaned_data_directory(query_config):
  state = query_config[STATE]
  return f'cleaned-data/{state}/'


def get_state_abbreviation(api_source):
  return api_source.split('-')[0]


def query_arcgis_restapi(query_config, api_source, label, value, directory,
                         filename):

  # url for specific Map Server
  url = query_config['url']
  layer = restapi.MapServiceLayer(url)
  # layer = restapi.FeatureLayer(url)

  # to get feature set as GeoJson, must set outSR to 4326 for geojson
  # first get the state's metadata by submitting an incorrect query
  features = layer.query(where='OBJECTID=20',
                         outSR=4326,
                         f='geojson',
                         exceed_limit=True)
  features.dump(directory + f'{to_kebab_case(api_source)}-metadata.geojson',
                indent=2)  # indent allows for pretty view

  # desired attribute conditions to filter the query by
  attribute_filter = f'{label}={value}'

  # then filter by specific attributes
  features = layer.query(where=attribute_filter,
                         outSR=4326,
                         f='geojson',
                         exceed_limit=True)
  # features = layer.query(outSR=4326, f='geojson', exceed_limit=True)
  # features = layer.query(where="bene_abrev = 'USU'", outSR=4326, f='geojson', exceed_limit=True)

  # count the number of features
  print(f'Found {len(features)} features with {attribute_filter}')

  # save geojson file, may save as json depending on the esri api version, needs 10.3 to saave as geojson
  features.dump(directory + filename,
                indent=2)  # indent allows for pretty view
  # features.dump('test.json', indent=2) # indent allows for pretty view

  # OR, you can save it directly to a shapefile (does not require arcpy)
  # layer.export_layer('test.shp', where=attribute_filter)


def main(api_source: str):

  query_config = QUERY_CONFIGS[api_source]

  # create the correct data directoies
  query_data_directory = get_query_data_directory(query_config)
  if not os.path.exists(query_data_directory):
    os.makedirs(query_data_directory)

  cleaned_data_directory = get_cleaned_data_directory(query_config)
  if not os.path.exists(cleaned_data_directory):
    os.makedirs(cleaned_data_directory)

  for label in query_config['attribute_label_to_filter_by']:
    for value, alias in query_config['attribute_value_to_alias_map'].items():
      # create a descriptive filename to store query info
      filename = get_filename(api_source, label, alias, '.geojson')

      query_arcgis_restapi(query_config, api_source, label, value,
                           query_data_directory, filename)

      filename = get_filename(api_source, label, alias, '.json')
      gdf = gpd.read_file(query_data_directory + filename)

      # add useful column data to dataset
      gdf[STATE] = query_config[STATE]
      gdf[UNIVERSITY] = query_config[UNIVERSITY]
      gdf[MANAGING_AGENCY] = query_config[MANAGING_AGENCY]
      if (query_config.get(RIGHTS_TYPE)):
        gdf[RIGHTS_TYPE] = query_config[RIGHTS_TYPE]

      # get the readable attribute filer which we used in the query
      gdf[ATTRIBUTE_FILTER] = f'{label}={alias}'

      # remove remaining columns
      columns_to_drop = [
          column for column in gdf.columns if column not in COLUMNS
      ]
      gdf.drop(columns_to_drop, axis=1, inplace=True)

      filename = get_filename(api_source, label, alias, '.geojson')
      gdf.to_file(cleaned_data_directory + filename, driver='GeoJSON')


if __name__ == "__main__":
  typer.run(main)
