# With this file we will get the missing OK parcels.
# we read in the missing parcel CSVs and match against the state servers (for aliquots AND lots)
# we create a new query ID for the values from the state that concat the columns in this order:
# aliquots: MER, TWP, TDIR, RNG, RDIR, SEC, ALIQUOT
# or lot: MER, TWP, TDIR, RNG, RDIR, SEC, SURV_TYPE, SURV_NUMB
# then we match the new value from the state server to the SEARCH_ID column in the missing parcel csvs
# take the new geometries and combine into the OK stuff
# take the rows that didn't get a geometric match and add them in, too. we have to include
# all the state config information plus directional info, but then it gets N/A in the geometry
import json
from collections import defaultdict
from pathlib import Path

import geopandas as gpd
import pandas as pd
import restapi
import typer
from numpy import isnan
from tqdm import tqdm

from land_grab_2.stl_dataset.step_1.constants import (OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_1, \
    OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_2, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_3, \
    OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SUB, ATTRIBUTE_LABEL_TO_FILTER_BY, ATTRIBUTE_CODE_TO_ALIAS_MAP,
                                                      STATE_TRUST_DATA_SOURCE_DIRECTORY)
from land_grab_2.stl_dataset.step_1.dataset_cleaning import clean_holding_detail_id, \
    _filter_queried_oklahoma_data
from land_grab_2.stl_dataset.step_1.state_trust_config import STATE_TRUST_CONFIGS
from land_grab_2.utilities.overlap import fix_geometries
from land_grab_2.utilities.utils import _get_filename, _queried_data_directory

app = typer.Typer()


def import_csv(loc):
    the_csv = pd.read_csv(loc)
    return the_csv


def process_missing_csv_rows(missing_csv, data_source, csv_name):
    match_ledger = []
    if data_source == 'https://gis.clo.ok.gov/arcgis/rest/services/Public/PLSSProd/MapServer/2':
        specific_col = 'ALIQUOT'
    else:
        specific_col = 'SURV_NUMB'

    all_parcels = []
    missing_items = missing_csv.to_dict(orient='records')
    for i, row in tqdm(enumerate(missing_items),total=len(missing_items)):
        mer = row['Meridian']
        twp = None if isnan(row['Township']) else int(row['Township'])
        tdir = row['TownshipDirection']
        rng = None if isnan(row['Range']) else int(row['Range'])
        rdir = row['RangeDirection']
        sec = None if isnan(row['Section']) else int(row['Section'])
        legal_desc = row['Legal_Description']

        if any(item is None for item in [mer, twp, tdir, rng, rdir, sec, legal_desc]):
            continue

        try:
            parcel = _query_arcgis_restapi(mer, twp, tdir, rng, rdir, sec, specific_col, legal_desc, data_source)
            if len(parcel) > 0:
                parcel = gpd.GeoDataFrame.from_features(json.loads(parcel.dumps()))
                all_parcels.append(parcel)
                match_ledger.append(i)
        except Exception as err:
            assert 1

    if not all_parcels:
        return (None, [])

    df = pd.concat(all_parcels)
    gdf = gpd.GeoDataFrame(df, geometry=df.geometry, crs=all_parcels[0].crs)

    geojson_destination = Path(f'./found-parcels-{csv_name}.geojson').resolve()
    i = 0
    while geojson_destination.exists():
        geojson_destination = Path(f'./found-parcels-{csv_name}-{i}.geojson').resolve()
        i += 1

    gdf.to_file(geojson_destination, driver='GeoJSON')

    return gdf, match_ledger


def _query_arcgis_restapi(mer, twp, tdir, rng, rdir, sec, specific_col, legal_desc, data_source):
    attribute_filter = (
        f"MER='{mer}' and TWP='{twp}' and TDIR='{tdir}' and RNG='{rng}' and RDIR='{rdir}' and SEC='{sec}'"
        f" and {specific_col}='{legal_desc}'"
    )

    layer = restapi.MapServiceLayer(data_source)

    features = layer.query(where=attribute_filter,
                           outSR=4326,
                           f='geojson',
                           exceed_limit=True)

    return features


def process_single_search_results(search_one, source_name):
    found_aliquots, matches_1 = process_missing_csv_rows(
        search_one,
        'https://gis.clo.ok.gov/arcgis/rest/services/Public/PLSSProd/MapServer/2',
        csv_name=source_name,
    )
    all_non_matches = set(list(range(search_one.shape[0]))) - set(matches_1)
    found_lots, matches_2 = process_missing_csv_rows(
        search_one,
        'https://gis.clo.ok.gov/arcgis/rest/services/Public/PLSSProd/MapServer/3',
        csv_name=source_name,
    )
    all_non_matches = all_non_matches - set(matches_2)

    missing = search_one[search_one.index.isin(all_non_matches)]

    csv_destination = Path(f'./still_missing-{source_name}.csv').resolve()
    i = 0
    while csv_destination.exists():
        csv_destination = Path(f'./still-missing-{source_name}-{i}.csv').resolve()
        i += 1

    missing.to_csv(csv_destination, index=False)


@app.command()
def search_missing_parcels():
    agriculture_parcels_csv = import_csv(
        STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/OK_missing_agricultural_parcels.csv')
    longterm_parcels_csv = import_csv(
        STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/OK_missing_longterm_commercial_parcels.csv')
    shortterm_parcels_csv = import_csv(
        STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/OK_missing_shortterm_commercial_parcels.csv')
    mineral_parcels_csv = import_csv(
        STATE_TRUST_DATA_SOURCE_DIRECTORY + 'OK/OK_missing_mineral_parcels.csv')

    missing_csvs = [
        (agriculture_parcels_csv, 'agriculture_parcels'),
        (longterm_parcels_csv, 'longterm_parcels'),
        (shortterm_parcels_csv, 'shortterm_parcels'),
        (mineral_parcels_csv, 'mineral_parcels')
    ]

    for csv, name in missing_csvs:
        found_aliquots, matches_1 = process_missing_csv_rows(
            csv,
            'https://gis.clo.ok.gov/arcgis/rest/services/Public/PLSSProd/MapServer/2',
            csv_name=name,
        )
        all_non_matches = set(list(range(csv.shape[0]))) - set(matches_1)
        found_lots, matches_2 = process_missing_csv_rows(
            csv,
            'https://gis.clo.ok.gov/arcgis/rest/services/Public/PLSSProd/MapServer/3',
            csv_name=name,
        )
        all_non_matches = all_non_matches - set(matches_2)

        missing = csv[csv.index.isin(all_non_matches)]

        csv_destination = Path(f'./still_missing-{name}.csv').resolve()
        i = 0
        while csv_destination.exists():
            csv_destination = Path(f'./still-missing-{name}-{i}.csv').resolve()
            i += 1

        missing.to_csv(csv_destination, index=False)


def find_unmatched_ok_parcels(gdf_search_one, original_parcel_reference_gdf, activity_source):
    # we want to find the parcels (rows) from the four source csvs (ag, min, long term, short term) from the state
    # that did not find a match in the recommended state servers. Then, those will go into their own csvs. We will then
    # take the csvs and manually generate a new column that combines PLSS data and can be matched against the state
    # server. It needs to be manual because the legal description is not broken up by aliquot appropriately.
    # Then, we call on the state server and combine columns to create a new value that can match the geographic
    # description we just created. We call on the server in the same way as before, using a list of IDs and reformatting
    # the state data. Then we generate new csvs that can be merged to the ones with the original findings.

    # take the values in HoldingDetailID fields for both gdfs, clean ones from state server
    original_parcel_reference_gdf = pd.read_csv(original_parcel_reference_gdf)

    original_reference_ids = original_parcel_reference_gdf['HoldingDetailID'].tolist()
    search_one_ids = gdf_search_one['HoldingDetailID'].tolist()
    search_one_ids = [clean_holding_detail_id(item) for item in search_one_ids]
    missing_ids = list(set(original_reference_ids) - set(search_one_ids))
    if not missing_ids:
        return gdf_search_one
    # I want the rows of the original reference gdf where the
    # holdingdetailID field is in the list of missing IDs
    csv_destination = Path(f'./missing-parcels-{activity_source}.csv').resolve()
    i = 0
    while csv_destination.exists():
        csv_destination = Path(f'./missing-parcels-{activity_source}-{i}.csv').resolve()
        i += 1

    missing_parcels_gdf = original_parcel_reference_gdf[
        original_parcel_reference_gdf['HoldingDetailID'].isin(missing_ids)
    ]

    missing_parcels_gdf.to_csv(csv_destination, index=False)
    # found_aliquot = process_missing_csv_rows(missing_parcels_gdf,
    #                                          'https://gis.clo.ok.gov/arcgis/rest/services/Public/PLSSProd/MapServer/2',
    #                                          csv_name=name, match_ledger=None)
    # found_lot = process_missing_csv_rows(csv, 'https://gis.clo.ok.gov/arcgis/rest/services/Public/PLSSProd/MapServer/3',
    #                                      csv_name=name, match_ledger=None)


@app.command()
def generate_raw_missing_parcels_list():
    queried_data_directory = _queried_data_directory(state='OK')
    # ok_config = [c for key, c in STATE_TRUST_CONFIGS.items() if key.startswith('OK')]

    all_ok_queried_files = defaultdict(list)
    state_sources = [source for source in STATE_TRUST_CONFIGS.keys() if 'OK' in source]
    for source in state_sources:
        config = STATE_TRUST_CONFIGS[source]
        for label in config[ATTRIBUTE_LABEL_TO_FILTER_BY]:
            if 'TrustName' in label:
                continue

            for code, alias in config[ATTRIBUTE_CODE_TO_ALIAS_MAP].items():
                filename = _get_filename(source, label, alias, '.json')
                queried_file_gdf = gpd.read_file(queried_data_directory + filename)
                if not queried_file_gdf.empty:
                    queried_file_gdf = fix_geometries(queried_file_gdf)
                    file_p = Path(filename).resolve()
                    if 'subsurface' in file_p.name:
                        all_ok_queried_files['subsurface'].append(queried_file_gdf)
                    # elif 'surface' not in file_p.name:
                    #     all_ok_cleaned_files['other'].append(cleaned_file_gdf)
                    else:
                        all_ok_queried_files['surface'].append(queried_file_gdf)

    for rights_type, queried_file_gdfs in all_ok_queried_files.items():
        for queried_file_gdf in queried_file_gdfs:
            if 'subsurface' in rights_type:
                gdf = _filter_queried_oklahoma_data(
                    queried_file_gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SUB, activity_source=None
                )

                find_unmatched_ok_parcels(
                    gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SUB, 'mineral_parcels'
                )
            else:
                gdf = _filter_queried_oklahoma_data(
                    queried_file_gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SUB, activity_source=None
                )

                find_unmatched_ok_parcels(
                    gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_1, 'agricultural_lease'
                )
                find_unmatched_ok_parcels(
                    gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_2, 'longterm_commercial_lease'
                )
                find_unmatched_ok_parcels(
                    gdf, OK_TRUST_FUNDS_TO_HOLDING_DETAIL_FILE_SURF_3, 'shortterm_commercial_lease'
                )


if __name__ == '__main__':
    # generate_raw_missing_parcels_list()
    search_missing_parcels()
    # app()
