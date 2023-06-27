# labels
STATE = 'state'
UNIVERSITY = 'university'
MANAGING_AGENCY = 'managing_agency'
RIGHTS_TYPE = 'rights_type'
ACTIVITY = 'activity'
ACRES = 'acres'
ACRES_GIS = 'gis_calculated_acres'
COUNTY = 'county'
PLSS_NUMBER = 'plss_number'
MERIDIAN = 'meridian'
ALIQUOT = 'aliquot'
RANGE = 'range'
TOWNSHIP = 'township'
SECTION = 'section'
BLOCK = 'block'
GEOMETRY = 'geometry'
ATTRIBUTE_FILTER = 'attribute_filter'
TRUST_NAME = 'trust_name'
SURFACE_RIGHTS_TYPE = 'surface'
SUBSURFACE_RIGHTS_TYPE = 'subsurface'
TIMBER_RIGHTS_TYPE = 'timber'
DOWNLOAD_TYPE = 'download_type'
API_QUERY_DOWNLOAD_TYPE = 'api_query'
SHAPEFILE_DOWNLOAD_TYPE = 'shapefile'
DATA_SOURCE = 'data_source'
LAYER = 'layer'
ATTRIBUTE_LABEL_TO_FILTER_BY = 'attribute_label_to_filter_by'
SURFACE_ATTRIBUTE_LABEL_TO_FILTER_BY = 'surface_attribute_label_to_filter_by'
SUBSURFACE_ATTRIBUTE_LABEL_TO_FILTER_BY = 'subsurface_attribute_label_to_filter_by'
ATTRIBUTE_CODE_TO_ALIAS_MAP = 'attribute_code_to_alias_map'
EXISTING_COLUMN_TO_FINAL_COLUMN_MAP = 'existing_column_to_final_column_map'

# cleaning oklahoma specific constants
OK_TRUST_FUNDS_ID_MAP = {5: 'Oregon State University', 7: 'Langston University'}
OK_TRUST_FUND_ID = 'TrustFundID'
OK_HOLDING_DETAIL_ID = 'HoldingDetailID'
OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE = '../../Downloads/All CLO Holdings.xlsx'

# data directories
DATA_DIRECTORY = 'data/'
STATE_TRUST_DIRECTORY = DATA_DIRECTORY + 'state_trust/'
UNIVERSITY_DIRECTORY = DATA_DIRECTORY + 'university/'
QUERIED_DIRECTORY = 'queried/'
MERGED_DIRECTORY = 'merged/'
CLEANED_DIRECTORY = 'cleaned/'
SOURCE_DIRECTORY = 'source/'
UNIVERSITY_DATA_SOURCE_DIRECTORY = UNIVERSITY_DIRECTORY + SOURCE_DIRECTORY
STATE_TRUST_DATA_SOURCE_DIRECTORY = STATE_TRUST_DIRECTORY + SOURCE_DIRECTORY

# final dataset columns
COLUMNS = [
    STATE, UNIVERSITY, ACRES, ACRES_GIS, RIGHTS_TYPE, ACTIVITY, MANAGING_AGENCY, TRUST_NAME, COUNTY, PLSS_NUMBER,
    MERIDIAN, TOWNSHIP, RANGE, SECTION, ALIQUOT, BLOCK, GEOMETRY
]
