# labels
import os

OBJECT_ID = 'object_id'
STATE = 'state'
UNIVERSITY = 'university'
MANAGING_AGENCY = 'managing_agency'
RIGHTS_TYPE = 'rights_type'
ACTIVITY = 'activity'
ACTIVITY_INFO = 'activity_info'
ACRES = 'acres'
GIS_ACRES = 'gis_acres'
NET_ACRES = 'net_acres'
COUNTY = 'county'
MERIDIAN = 'meridian'
ALIQUOT = 'aliquot'
RANGE = 'range'
TOWNSHIP = 'township'
SECTION = 'section'
BLOCK = 'block'
PARCEL_COUNT = 'parcel_count'
ACRES_AGG = 'acres_agg'
GEOMETRY = 'geometry'
ATTRIBUTE_FILTER = 'attribute_filter'
TRUST_NAME = 'trust_name'
STATE_ENABLING_ACT = 'state_enabling_act'
SURFACE_RIGHTS_TYPE = 'surface'
SUBSURFACE_RIGHTS_TYPE = 'subsurface'
TIMBER_RIGHTS_TYPE = 'timber'
DOWNLOAD_TYPE = 'download_type'
API_QUERY_DOWNLOAD_TYPE = 'api_query'
SHAPEFILE_DOWNLOAD_TYPE = 'shapefile'
GEOJSON_TYPE = 'geojson'
DATA_SOURCE = 'data_source'
LOCAL_DATA_SOURCE = 'local_data_source'
LAYER = 'layer'
ATTRIBUTE_LABEL_TO_FILTER_BY = 'attribute_label_to_filter_by'
SURFACE_ATTRIBUTE_LABEL_TO_FILTER_BY = 'surface_attribute_label_to_filter_by'
SUBSURFACE_ATTRIBUTE_LABEL_TO_FILTER_BY = 'subsurface_attribute_label_to_filter_by'
ATTRIBUTE_CODE_TO_ALIAS_MAP = 'attribute_code_to_alias_map'
EXISTING_COLUMN_TO_FINAL_COLUMN_MAP = 'existing_column_to_final_column_map'

# data directories
data_tld = os.environ.get('DATA')
if data_tld is None:
    raise Exception('NoDataError: Env var: DATA must be set as the path to all project input data.')

DATA_DIRECTORY = f'{data_tld}/stl_dataset/step_1/input/'
STL_OUTPUT_DIRECTORY = f'{data_tld}/stl_dataset/step_1/output/'
STATE_TRUST_DIRECTORY = DATA_DIRECTORY + 'state_trust/'
UNIVERSITY_DIRECTORY = DATA_DIRECTORY + 'university/'
QUERIED_DIRECTORY = 'queried/'
MERGED_DIRECTORY = 'merged/'
CLEANED_DIRECTORY = 'cleaned/'
CESSIONS_DIRECTORY = 'cessions/'
SUMMARY_STATISTICS_DIRECTORY = 'summary_statistics/'
# SOURCE_DIRECTORY = 'parcel_ID_lists/'
SOURCE_DIRECTORY = 'source/'
UNIVERSITY_DATA_SOURCE_DIRECTORY = UNIVERSITY_DIRECTORY + SOURCE_DIRECTORY
STATE_TRUST_DATA_SOURCE_DIRECTORY = STATE_TRUST_DIRECTORY + SOURCE_DIRECTORY

# file names
UNIVERSITY_SUMMARY = 'university-summary.csv'
TRIBE_SUMMARY = 'tribe-summary.csv'
ALL_STATES = 'all-states'

# cleaning oklahoma specific constants
OK_TRUST_FUND_ID = 'TrustFundID'
OK_HOLDING_DETAIL_ID = 'HoldingDetailID'
OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_1 = STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/OK-surface-agricultural-lease.csv'
OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_2 = STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/OK-surface-long-term-commercial-lease.csv'
OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_3 = STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/OK-surface-short-term-commercial-lease.csv'
OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SUB = STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/OK-subsurface-mineral-lease.csv'
OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_OSU = STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/All CLO Holdings.xlsx'

# final dataset columns, in order we want them to be saved
FINAL_DATASET_COLUMNS = [
    OBJECT_ID, STATE, STATE_ENABLING_ACT, TRUST_NAME, MANAGING_AGENCY,
    UNIVERSITY, ACRES, GIS_ACRES, NET_ACRES, RIGHTS_TYPE, ACTIVITY, ACTIVITY_INFO, COUNTY, MERIDIAN,
    TOWNSHIP, RANGE, SECTION, ALIQUOT, BLOCK, DATA_SOURCE, PARCEL_COUNT, ACRES_AGG, GEOMETRY
]

# unit conversions
ACRES_TO_SQUARE_METERS = 4046.8564224

# map projection
ALBERS_EQUAL_AREA = 'EPSG:5070'
WGS_84 = 'EPSG:4326'

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'
