import os

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'
import restapi
import typer

from config import queries


def to_kebab_case(value):
  '''convert string to kebab case'''
  if '_' in value:
    return "-".join(value.lower().split('_'))
  else:
    return "-".join(value.lower().split())


def get_filename(state, label, alias):
  '''return a filename in kebabcase'''
  return f'{to_kebab_case(state)}-{to_kebab_case(label)}-{to_kebab_case(alias)}.geojson'


def get_directory(state_abbreviation):
  return f'{state_abbreviation}/'


def get_state_abbreviation(api_source):
  return api_source.split('-')[0]


def query_arcgis_restapi(query, api_source):

  state = get_state_abbreviation(api_source)

  for label in query['attribute_label_to_filter_by']:
    for value, alias in query['attribute_value_to_alias_map'].items():

      # url for specific Map Server
      url = query['url']
      layer = restapi.MapServiceLayer(url)

      # desired attribute conditions to filter the query by
      attribute_filter = f'{label}={value}'

      # create the correct directory
      directory = get_directory(state)
      if not os.path.exists(directory):
        os.makedirs(directory)

      # to get feature set as GeoJson, must set outSR to 4326 for geojson
      # first get the state's metadata by submitting an incorrect query
      features = layer.query(where='OBJECTID=20',
                             outSR=4326,
                             f='geojson',
                             exceed_limit=True)
      features.dump(directory +
                    f'{to_kebab_case(api_source)}-metadata.geojson',
                    indent=2)  # indent allows for pretty view

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
      filename = get_filename(api_source, label, alias)
      features.dump(directory + filename,
                    indent=2)  # indent allows for pretty view
      # features.dump('test.json', indent=2) # indent allows for pretty view

      # OR, you can save it directly to a shapefile (does not require arcpy)
      # layer.export_layer('test.shp', where=attribute_filter)


def main(api_source: str):
  query = queries[api_source]
  query_arcgis_restapi(query, api_source)


if __name__ == "__main__":
  typer.run(main)
