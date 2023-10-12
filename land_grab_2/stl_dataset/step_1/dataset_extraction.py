import os
from pathlib import Path

import geopandas as gpd

from land_grab_2.stl_dataset.step_1.constants import DOWNLOAD_TYPE, SHAPEFILE_DOWNLOAD_TYPE, LOCAL_DATA_SOURCE, LAYER, \
    ATTRIBUTE_LABEL_TO_FILTER_BY, ATTRIBUTE_CODE_TO_ALIAS_MAP, API_QUERY_DOWNLOAD_TYPE
from land_grab_2.stl_dataset.step_1.dataset_cleaning import _clean_queried_data, _filter_and_clean_shapefile
from land_grab_2.utilities.utils import _query_arcgis_restapi, memory

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'


def extract_and_clean_single_source_helper(source: str, config: dict,
                                           queried_data_directory: str,
                                           cleaned_data_directory: str):
    # create the correct data directories
    if not os.path.exists(queried_data_directory):
        Path(queried_data_directory).mkdir(exist_ok=True, parents=True)

    if not os.path.exists(cleaned_data_directory):
        Path(cleaned_data_directory).mkdir(exist_ok=True, parents=True)

    # if downloading shapefile
    if config[DOWNLOAD_TYPE] == SHAPEFILE_DOWNLOAD_TYPE:
        gdf = gpd.read_file(config[LOCAL_DATA_SOURCE], layer=config.get(LAYER))

    cached_query_arcgis_restapi = memory.cache(_query_arcgis_restapi)

    for label in config[ATTRIBUTE_LABEL_TO_FILTER_BY]:
        for code, alias in config[ATTRIBUTE_CODE_TO_ALIAS_MAP].items():

            # if querying from rest api
            if config[DOWNLOAD_TYPE] == API_QUERY_DOWNLOAD_TYPE:

                cached_query_arcgis_restapi(config, source, label, code, alias,
                                            queried_data_directory)

                _clean_queried_data(source, config, label, alias,
                                    queried_data_directory, cleaned_data_directory)

            # if cleaning a shapefile
            elif config[DOWNLOAD_TYPE] == SHAPEFILE_DOWNLOAD_TYPE:

                _filter_and_clean_shapefile(gdf, config, source, label, code, alias,
                                            cleaned_data_directory)
