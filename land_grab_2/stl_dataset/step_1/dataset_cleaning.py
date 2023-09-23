import os

import geopandas as gpd
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import ALBERS_EQUAL_AREA, EXISTING_COLUMN_TO_FINAL_COLUMN_MAP, COLUMNS, \
    TRUST_NAME, TOWNSHIP, RANGE, SECTION, MERIDIAN, COUNTY, ALIQUOT, RIGHTS_TYPE, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE, \
    OK_HOLDING_DETAIL_ID, ACTIVITY, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_2, OK_TRUST_FUND_ID
from land_grab_2.utils import _get_filename, add_uuid

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'


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
    if 'uuid' not in gdf.columns:
        assert 1

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
    if 'uuid' not in filtered_gdf.columns:
        assert 1

    # more custom cleaning
    if 'NM' in source:
        filtered_gdf = _clean_nm_town_range(filtered_gdf)

    filename = _get_filename(source, label, alias, '.geojson')
    filtered_gdf.to_file(cleaned_data_directory + filename, driver='GeoJSON')

    return filtered_gdf


def add_uuid_col(gdf):
    uuid_cols = ['OBJECTID', 'objectid', 'HoldingDetailID', 'GlobalID', 'SU_SUID', 'TRACT_ID']
    uuid_cols_paired = [('STR', 'Shape_Leng'), ('DTRSQQ', 'CALCACRES')]
    uuid_cols_paired_gen = ((c1, c2) for c1, c2 in uuid_cols_paired if (c1 in gdf.columns and c2 in gdf.columns))

    if any(col for col in uuid_cols if col in gdf.columns):
        uuid_col = next((col for col in uuid_cols if col in gdf.columns), None)
        gdf['uuid'] = gdf[uuid_col].map(lambda v: add_uuid(*[v]))
    else:
        if any((c1, c2) for c1, c2 in uuid_cols_paired if (c1 in gdf.columns and c2 in gdf.columns)):
            uuid_col_1, uuid_col_2 = next(uuid_cols_paired_gen, None)
            gdf['uuid'] = gdf.apply(lambda row: add_uuid(*[uuid_col_1, uuid_col_2]), axis=1)
        else:
            if 'Meridian' in gdf.columns or 'meridian' in gdf.columns:
                gdf['uuid'] = gdf.apply(lambda row: add_uuid(*[v for k, v in row.items() if 'geometry' not in k]),
                                        axis=1)
            else:
                print('NO UUID EFFECTIVE COLUMN!!!!')
                print(gdf.columns)

    return gdf


def _format_columns(gdf, config, alias):
    '''
    Column formatting used in final dataset
    '''

    gdf = add_uuid_col(gdf)
    if 'uuid' not in gdf.columns:
        assert 1

    # if the initial dataset contains any columns that can be used in our final
    # dataset, rename them to the final dataset column name
    if config.get(EXISTING_COLUMN_TO_FINAL_COLUMN_MAP):
        gdf = gdf.rename(columns=config[EXISTING_COLUMN_TO_FINAL_COLUMN_MAP])

    # add any other data if it exists in the config
    for column in COLUMNS:
        if ((column not in gdf.columns) and config.get(column)):
            gdf[column] = config[column]

    # remove remaining columns
    columns_to_drop = [column for column in gdf.columns if column not in COLUMNS + ['uuid']]

    # add trust name columns
    if alias:
        gdf[TRUST_NAME] = alias
    return gdf.drop(columns_to_drop, axis=1)


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
    df = pd.read_excel(OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_2)

    # clean and filter by the trust funds we care about, 5 for OSU
    df = df[[OK_HOLDING_DETAIL_ID, OK_TRUST_FUND_ID]].copy()
    df = df[df[OK_TRUST_FUND_ID].isin([5])]
    df[OK_HOLDING_DETAIL_ID] = df[OK_HOLDING_DETAIL_ID].astype(str)
    return df
