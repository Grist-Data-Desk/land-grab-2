import json
import logging
from copy import deepcopy
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely import Polygon

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def extract_ring_data(raw_geo_data):
    hydrated_geos = [
        Polygon(feature['geometry']['rings'][0])
        for feature in raw_geo_data['features']
        if len(feature['geometry']['rings']) == 1
    ]
    return hydrated_geos


def extract_attributes(a_json):
    return [feat['attributes'] for feat in a_json['features']]


def union_parcel_jsons(parcel_jsons_dir):
    log.info('merge all jsons')
    all_jsons = []
    for file in parcel_jsons_dir.iterdir():
        if 'DS_Store' in file.name:
            continue

        with file.open() as fh:
            a_json = json.load(fh)
            geometries = extract_ring_data(a_json)
            attributes = extract_attributes(a_json)
            rows = [{**a, 'geometry': g} for a, g in zip(attributes, geometries)]
            all_jsons += rows

    return all_jsons


def create_compiled_geodf(done_csv, match_report_csv, all_parcel_jsons, match_type):
    log.info('compiling all data into geopandas dataframe')
    new_df = deepcopy(done_csv)
    new_df[match_report_csv.columns] = match_report_csv[match_report_csv.columns]
    new_df['geometry'] = new_df['geometry'].apply(lambda v: Polygon(json.loads(v)))
    done_keep_cols = ['STATEABBR', 'TWNSHPNO', 'RANGENO', 'PLSSID', 'FRSTDIVID', 'SECDIVID', 'QQSEC', 'GOVLOT',
                      'RECRDAREANO', 'GISACRE', 'OBJECTID', 'Shape.STArea()', 'Shape.STLength()', 'geometry']
    json_df = pd.DataFrame(data=all_parcel_jsons, columns=done_keep_cols)
    json_df['match_type'] = match_type
    # Needs to match match_type column from match_report.csv
    json_df['has_match'] = True

    return json_df, new_df


def main(sd_folder):
    sd_folder_p = Path(sd_folder)
    log.info('read done.csv')
    done_csv_p = sd_folder_p / 'sd_parcel_match_SAMPLE_FILES/done.csv'
    done_keep_cols = ['STATEABBR', 'TWNSHPNO', 'RANGENO', 'PLSSID', 'FRSTDIVID', 'SECDIVID', 'QQSEC', 'GOVLOT',
                      'RECRDAREANO', 'GISACRE', 'OBJECTID', 'Shape.STArea()', 'Shape.STLength()', 'geometry']
    done_csv = pd.read_csv(done_csv_p, usecols=done_keep_cols)

    log.info('read match report')
    match_report_p = sd_folder_p / 'sd_parcel_match_report_SAMPLE_FILES/match_report.csv'
    match_report_keep_cols = ['has_match', 'match_type']
    match_report_csv = pd.read_csv(match_report_p, usecols=match_report_keep_cols)

    log.info('read all jsons')
    surface_p = sd_folder_p / 'sd_found_surface_jsons'
    subsurface_p = sd_folder_p / 'sd_found_subsurface_jsons'
    paths_to_parcels_data = [surface_p, subsurface_p]

    concat_data = []
    new_df = None
    for p in paths_to_parcels_data:
        match_type = 'subsurface' if 'subsurface' in p.name else 'surface'
        all_parcel_jsons = union_parcel_jsons(p)

        json_df, new_df = create_compiled_geodf(done_csv, match_report_csv, all_parcel_jsons, match_type)
        concat_data.append(json_df)

    compiled_data = pd.concat([new_df] + concat_data)

    # create geopandas dataframe
    gdf = gpd.GeoDataFrame(data=compiled_data, crs='epsg:4326')

    log.info('set geometry column')
    gdf.set_geometry(gdf['geometry'])

    log.info('write geojson')
    out_dir = Path('data/out')
    out_dir.mkdir(parents=True, exist_ok=True)
    gdf.to_file(str(out_dir / 'complete_sd_stl_parcels.json'), driver="GeoJSON")

    log.info('done')


if __name__ == '__main__':
    main(sd_folder='/Users/mpr/Documents/01_Current Projects/Grist_LGU2/FACT CHECK/03_South Dakota')