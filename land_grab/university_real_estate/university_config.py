from land_grab.constants import (
    DOWNLOAD_TYPE, API_QUERY_DOWNLOAD_TYPE, SHAPEFILE_DOWNLOAD_TYPE, STATE,
    UNIVERSITY, MANAGING_AGENCY, DATA_SOURCE, ATTRIBUTE_LABEL_TO_FILTER_BY,
    ATTRIBUTE_CODE_TO_ALIAS_MAP, UNIVERSITY_DATA_SOURCE_DIRECTORY, EXISTING_COLUMN_TO_FINAL_COLUMN_MAP)

UNIVERSITY_CONFIGS = {
    'AZ': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'AZ',
        UNIVERSITY: 'University of Arizona',
        MANAGING_AGENCY: 'State Land Department',
        DATA_SOURCE:
        'https://server.azgeo.az.gov/arcgis/rest/services/azland/State_Trust_Parcels/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['fundtxt'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'UNIVERSITY'": 'UNIVERSITY',
            "'UNIV OF ARIZ (ACT 2/18/1881)'": 'UNIV OF ARIZ (ACT 2.18.1881)'
        },
    },
    'UMN': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'MN',
        UNIVERSITY: 'University of Minnesota',
        DATA_SOURCE:
        UNIVERSITY_DATA_SOURCE_DIRECTORY + 'REO_UMN_Data_2022-01-28',
        # TODO: other possible columsn to add, county, also percentage of surface and mineral ownership
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'STATE': STATE,
            'SUBQOWN': MANAGING_AGENCY
        },
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['*'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "*": 'All'
        },
    },
}