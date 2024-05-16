import os
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import ALBERS_EQUAL_AREA, EXISTING_COLUMN_TO_FINAL_COLUMN_MAP, \
    FINAL_DATASET_COLUMNS, \
    TRUST_NAME, TOWNSHIP, RANGE, SECTION, MERIDIAN, ALIQUOT, RIGHTS_TYPE, \
    OK_HOLDING_DETAIL_ID, ACTIVITY, NET_ACRES, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SUB, \
    OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_1, \
    OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_2, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_3
from land_grab_2.utilities.utils import _get_filename

os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'


def _get_net_acres(gdf, source, config, alias):
    if NET_ACRES not in config:
        return gdf

    all_net_acres_info = pd.read_csv(config[NET_ACRES])
    net_acres_info = all_net_acres_info[all_net_acres_info['Trust Name'] == alias].to_dict(orient='records')
    if not net_acres_info:
        return gdf

    net_acres_info = net_acres_info[0]
    percentage = net_acres_info['Percentage']
    gdf[NET_ACRES] = gdf['GISACRES'] * (percentage / 100)

    return gdf


def _clean_queried_data(source, config, label, alias, queried_data_directory,
                        cleaned_data_directory):
    '''
    Clean data queried from restapis
    '''

    filename = _get_filename(source, label, alias, '.json')
    gdf = gpd.read_file(queried_data_directory + filename)

    if gdf.empty:
        return gdf
    elif source == 'OK-real-estate-subdivs':
        gdf = _filter_queried_oklahoma_data_surface(gdf)
        gdf = _get_ok_surface_town_range(gdf)
    elif source == 'OK-subsurface-mineral-lease':
        gdf = _get_ok_activity(gdf, source)
        df = gdf.groupby(['geometry']).first().reset_index()
        gdf = gpd.GeoDataFrame(df, geometry=df.geometry, crs=gdf.crs)
    elif source == 'OK-subsurface-minerals':
        gdf = _filter_queried_oklahoma_data_subsurface(gdf, activity_source=source)
        gdf = _get_ok_surface_town_range(gdf)
    elif source == 'OK-subsurface-unleased-minerals':
        gdf = _filter_queried_oklahoma_data_subsurface(gdf, activity_source=source)
        gdf = _get_ok_surface_town_range(gdf)
    elif 'AZ' in source:
        gdf = _get_az_town_range_section(gdf)
    elif 'MT' in source:
        gdf = _get_mt_town_range_section(gdf)
    elif 'OR' in source:
        gdf = _get_or_town_range_section(gdf)
    elif 'UT' in source:
        gdf = _get_ut_activity(gdf, source)
    elif 'ND' in source:
        gdf = _get_nd_activity(gdf, source, config)
    elif 'ID' in source:
        gdf = _get_net_acres(gdf, source, config, alias)

    gdf = _format_columns(gdf, config, alias)

    if not gdf.empty:
        filename = _get_filename(source, label, alias, '.geojson')
        gdf.to_file(cleaned_data_directory + filename, driver='GeoJSON')

    return gdf


def _get_ok_activity(filtered_gdf, source):
    """
    extract activity value from directory name
    """
    surface = 'OK-surface-'
    subsurface = 'OK-subsurface-'
    prefix = (surface in source and surface) or (subsurface in source and subsurface)
    if not prefix:
        return filtered_gdf

    source = Path(source).resolve().stem
    activity_name = source[len(prefix):].replace('-', ' ').replace('and', '&')
    if not activity_name:
        return filtered_gdf

    activity_name = activity_name.title()
    if ACTIVITY in filtered_gdf.columns:
        filtered_gdf[ACTIVITY] = filtered_gdf[ACTIVITY].map(lambda v: activity_name)
    else:
        filtered_gdf[ACTIVITY] = activity_name

    return filtered_gdf


def _get_ut_activity(filtered_gdf, source):
    """
    extract activity value from directory name
    """
    surface = 'UT-surface-'
    subsurface = 'UT-subsurface-'
    prefix = (surface in source and surface) or (subsurface in source and subsurface)
    if not prefix:
        return filtered_gdf

    activity_name = source[len(prefix):].replace('-', ' ')  # .replace('and', '&')
    if not activity_name:
        return filtered_gdf

    activity_name = activity_name.title()
    if ACTIVITY in filtered_gdf.columns:
        filtered_gdf[ACTIVITY] = filtered_gdf[ACTIVITY].map(lambda v: activity_name)
    else:
        filtered_gdf[ACTIVITY] = activity_name

    return filtered_gdf


def _get_nd_activity(filtered_gdf, source, config):
    """
    extract activity value from directory name
    """

    activity_name = config[ACTIVITY]
    filtered_gdf[ACTIVITY] = np.where(filtered_gdf['LEASE'].str.contains('none'), '', activity_name)

    return filtered_gdf


def _filter_and_clean_shapefile_or_geojson(gdf, config, source, label, code, alias,
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
        # filtered_gdf = _get_mt_activity(filtered_gdf, source)
    elif 'SD' in source:
        filtered_gdf = _get_sd_town_range_meridian(filtered_gdf)
        # filtered_gdf = _get_sd_rights_type(filtered_gdf)
    elif 'SD-surface' in source:
        filtered_gdf = _get_sd_surface_rights_type(filtered_gdf)
    elif 'SD-subsurface' in source:
        filtered_gdf = _get_sd_subsurface_rights_type(filtered_gdf)
    elif 'UT' in source:
        filtered_gdf = _get_ut_activity(gdf, source)
    elif source == 'OK-found-parcels-agriculture-parcels':
        gdf = _get_ok_variant_town_range(gdf)
    elif source == 'OK-found-parcels-agriculture-parcels-0':
        gdf = _get_ok_variant_town_range(gdf)
    elif source == 'OK-found-parcels-shortterm-parcels':
        gdf = _get_ok_variant_town_range(gdf)
    elif source == 'OK-found-parcels-longterm-parcels':
        gdf = _get_ok_variant_town_range(gdf)
    # elif source == 'OK-found-parcels-mineral-parcels':
    #     gdf = _get_ok_variant_town_range(gdf)
    # elif source == 'OK-found-parcels-mineral-parcels-0':
    #     gdf = _get_ok_variant_town_range(gdf)

    filtered_gdf = _format_columns(filtered_gdf, config, alias)

    # # more custom cleaning
    # if 'NM' in source:
    #     filtered_gdf = _clean_nm_town_range(filtered_gdf)

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
        out_cols = set(config[EXISTING_COLUMN_TO_FINAL_COLUMN_MAP].values()) - set(gdf.columns.tolist())
        deduplicated_cols = {k: v for k, v in config[EXISTING_COLUMN_TO_FINAL_COLUMN_MAP].items() if v in out_cols}
        gdf = gdf.rename(columns=deduplicated_cols)

    # add any other data if it exists in the config
    for column in FINAL_DATASET_COLUMNS:
        if ((column not in gdf.columns) and config.get(column)):
            gdf[column] = config[column]

    chlk = ['parcel', 'parcelid', 'globalid', 'objectid']
    groupby_col = next((c for c in gdf.columns for l in chlk if l.lower() in c.lower()), None)

    # remove remaining columns
    columns_to_drop = [column for column in gdf.columns if column not in FINAL_DATASET_COLUMNS + [groupby_col]]

    # add trust name columns
    if alias:
        if 'USE_ALIAS' not in config or 'USE_ALIAS' in config and config['USE_ALIAS']:
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


# def _clean_nm_town_range(gdf):
#     # nm section and range data has extra leading and trailing zeros in a funny way
#     # # for example Range 11E is formatted 0110E. So we remove the extra zeros here.
#     for column in [RANGE, TOWNSHIP]:
#         gdf[column] = gdf[column].str.slice(start=1,
#                                             stop=3) + gdf[column].str.slice(start=4)
#     return gdf

def _get_ok_variant_town_range(gdf):
    '''
    OK surface data has township and range divided into two parts, so merge those parts
    '''
    gdf[TOWNSHIP] = gdf['TWP'].astype(str) + gdf['TDIR']
    gdf[RANGE] = gdf['RNG'].astype(str) + gdf['RDIR']
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


# def _get_ut_town_range_section_county(gdf):
#     '''
#     data has a 'TRS_LABEL' column which is composed of township, range, sectionm meridian
#     '''
#     # first clean county name
#     gdf[COUNTY] = gdf['county_name'].str.strip()
#
#     split = gdf['TRS_LABEL'].str.split(' ', expand=True)
#     gdf[SECTION] = split[2].str.slice(start=3)
#
#     township_split = split[0].str.split('.', expand=True)
#     gdf[TOWNSHIP] = township_split[0].str.slice(
#         start=1) + township_split[1].str.slice(start=-1)
#
#     range_split = split[1].str.split('.', expand=True)
#     gdf[RANGE] = range_split[0].str.slice(start=1) + range_split[1].str.slice(
#         start=-1)
#     gdf[MERIDIAN] = split[3]
#     return gdf


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


def _get_sd_surface_rights_type(gdf):
    '''
    get and clean SD rights types to be consistent with the rest of the dataset
    '''
    both = gdf[gdf['match_type'] == 'both']
    both['match_type'] = both['match_type'].str.replace('both', 'surface')
    # gdf['match_type'] = gdf['match_type'].str.replace('both', 'subsurface')
    gdf = pd.concat([gdf, both], ignore_index=True)
    gdf[RIGHTS_TYPE] = gdf['match_type'].str.lower()
    return gdf


def _get_sd_subsurface_rights_type(gdf):
    '''
    get and clean SD rights types to be consistent with the rest of the dataset
    '''
    both = gdf[gdf['match_type'] == 'both']
    # both['match_type'] = both['match_type'].str.replace('both', 'surface')
    gdf['match_type'] = gdf['match_type'].str.replace('both', 'subsurface')
    gdf = pd.concat([gdf, both], ignore_index=True)
    gdf[RIGHTS_TYPE] = gdf['match_type'].str.lower()
    return gdf


def clean_holding_detail_id(item):
    item = str(item)
    item = item.replace('}', '')
    item = item.replace('{', '')
    return item


def _filter_queried_oklahoma_data(gdf, data_source, activity_source=None, debug_activity_source=None):
    filter_df = pd.read_csv(data_source)

    # change id from dictionary to string
    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].str.replace('}', '')
    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].str.replace('{', '')
    gdf[OK_HOLDING_DETAIL_ID] = gdf[OK_HOLDING_DETAIL_ID].astype(str)

    # filter dataframe by specific ids
    gdf = gdf[gdf[OK_HOLDING_DETAIL_ID].isin(filter_df[OK_HOLDING_DETAIL_ID])]

    df = gdf.merge(filter_df, on=OK_HOLDING_DETAIL_ID, how='left')
    ex, why = '_x', '_y'
    df.drop([c for c in df.columns if c.endswith(why)], inplace=True, axis=1)
    df.rename(columns={c: c.rstrip(ex) for c in df.columns if c.endswith(ex)}, inplace=True)
    df.drop_duplicates([OK_HOLDING_DETAIL_ID], inplace=True, ignore_index=True)

    df = _get_ok_activity(df, activity_source or data_source)

    gdf_out = gpd.GeoDataFrame(df, geometry=df.geometry, crs=gdf.crs)

    return gdf_out


def _filter_queried_oklahoma_data_surface(gdf):
    # OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SUB
    # OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_OSU

    # filter dataframe by specific ids
    gdf1 = _filter_queried_oklahoma_data(gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_1,
                                         debug_activity_source='agricultural_lease')
    gdf2 = _filter_queried_oklahoma_data(gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_2,
                                         debug_activity_source='longterm_commercial_lease')
    gdf3 = _filter_queried_oklahoma_data(gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_3,
                                         debug_activity_source='shortterm_commercial_lease')

    df = pd.concat([gdf1, gdf2, gdf3])
    gdf_out = gpd.GeoDataFrame(df, geometry=df.geometry, crs=gdf.crs)

    return gdf_out


def _filter_queried_oklahoma_data_subsurface(gdf, activity_source):
    # filter dataframe by specific ids
    gdf_out = _filter_queried_oklahoma_data(gdf,
                                            OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SUB,
                                            activity_source=activity_source)
    return gdf_out
