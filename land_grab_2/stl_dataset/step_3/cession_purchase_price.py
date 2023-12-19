import itertools
import logging
import os
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import GIS_ACRES

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

not_a_cession = ['336', '368', '496', '510', '524', '525', '552', '591', '596', '599', '618', '621', '625', '632',
                 '633', '651', '702', '713', '718', '540a']
unknown_cession_data = ['717']


def get_price_paid_per_acre(cession, price_info_raw):
    if cession in not_a_cession:
        return 'N/A'

    if cession in unknown_cession_data:
        return 'Unknown'

    if not isinstance(price_info_raw, str) and np.isnan(price_info_raw):
        return 'Unknown'

    price_info = price_info_raw.lstrip('$')
    return 0.0 if not price_info else float(price_info)


def find_cession_number_column_name(row):
    all_cession_nums_column = 'all_cession_numbers'
    if 'all_cessions_numbers' in row.keys():
        all_cession_nums_column = 'all_cessions_numbers'
        return all_cession_nums_column

    if 'all_cession_numbers' in row.keys():
        all_cession_nums_column = 'all_cession_numbers'
        return all_cession_nums_column

    return None


def extract_cession_numbers(row):
    all_cession_nums_column = find_cession_number_column_name(row)
    cession_nums = []

    if all_cession_nums_column is None:
        return cession_nums

    if not isinstance(row[all_cession_nums_column], str):
      return cession_nums
    
    space_split_cession_nums = row[all_cession_nums_column].split(' ')
    if space_split_cession_nums:
        return space_split_cession_nums

    comma_split_cession_nums = row[all_cession_nums_column].split(',')
    if comma_split_cession_nums:
        return comma_split_cession_nums

    return cession_nums


def convert_cession_num_to_int(df):
    cession_columns = [c for c in df.columns if c.startswith('cession_num_')]
    for c in cession_columns:
        df[c] = df[c].map(_convert_cession_num_to_int)

    return df


def _convert_cession_num_to_int(value):
    if not isinstance(value, str) and np.isnan(value):
        return ''
    if isinstance(value, str) and value.isalnum():
        return value
    if isinstance(value, str):
        value = value.replace(".0", "")
        return value

    value = str(int(value))

    return value


def add_price_columns(stl_data, price_data):
    log.info('processing price information')
    all_columns = stl_data.columns.tolist()
    cession_columns = [c for c in all_columns if c.endswith('present_day_tribe')]
    cession_price_columns = [f'C{i}_price_paid_per_acre' for i, _ in enumerate(cession_columns, start=1)]

    out_rows = []
    cession_prices_simple = {}
    stl_data_as_dict = stl_data.to_dict(orient='records')
    for i, row in enumerate(stl_data_as_dict):
        # ensure all cessions have a correlated, initially blank, price column
        for c in cession_price_columns:
            row[c] = ''

        cession_nums = extract_cession_numbers(row)

        if any(' ' in c for c in cession_nums):
            cession_nums = list(
                itertools.chain.from_iterable([c if ' ' not in c else c.split(' ') for c in cession_nums]))

        cession_prices = {}
        for i, cession in enumerate(cession_nums, start=1):
            if cession in cession_prices_simple:
                row[f'C{i}_price_paid_per_acre'] = cession_prices_simple[cession]
                if isinstance(row[f'C{i}_price_paid_per_acre'], str):
                    continue
                cession_prices[(i, cession)] = row[f'C{i}_price_paid_per_acre']
                continue

            cession_price_rows = price_data[price_data['Cession_Number'] == cession].to_dict(orient='records')
            if not cession_price_rows:
                continue

            price_info = cession_price_rows[0]['US_Paid_Per_Acre - Inflation Adjusted']
            row[f'C{i}_price_paid_per_acre'] = get_price_paid_per_acre(cession, price_info)
            cession_prices_simple[cession] = row[f'C{i}_price_paid_per_acre']

            if isinstance(row[f'C{i}_price_paid_per_acre'], str):
                continue

            cession_prices[(i, cession)] = row[f'C{i}_price_paid_per_acre']

        if 'gis_calculated_acres' in row and row['gis_calculated_acres']:
            parcel_size = float(row['gis_calculated_acres'])
        elif GIS_ACRES in row and row[GIS_ACRES]:
            parcel_size = float(row[GIS_ACRES])
        else:
            parcel_size = 0.0

        row[f'price_paid_for_parcel'] = round(sum([
            price * parcel_size
            for price in cession_prices.values()
        ]), 2)

        out_rows.append(row)

    log.info('formatting columns')
    new_col_seq = []
    cession_price_column_names = cession_price_columns.copy()
    all_cession_nums_column = find_cession_number_column_name(stl_data_as_dict[0])

    for c in all_columns:
        if all_cession_nums_column is not None and all_cession_nums_column in c:
            new_col_seq.append(c)
            new_col_seq.append('price_paid_for_parcel')
        elif c.endswith('present_day_tribe'):
            new_col_seq.append(cession_price_column_names.pop(0))
            new_col_seq.append(c)
        else:
            new_col_seq.append(c)

    df = pd.DataFrame(out_rows)
    df = df[new_col_seq]
    df = convert_cession_num_to_int(df)
    return df


def map_and_impute_ok_data(df, activity_type):
    column_mapping = {
        'Acres': 'acres',
        'Meridian': 'meridian',
        'Section': 'section',
        'Legal_Description': 'aliquot',
        }

    mapped_df = df.rename(columns=column_mapping)

    mapped_df['township'] = df['Township'].astype(str) + df['TownshipDirection']
    mapped_df['range'] = df['Range'].astype(str) + df['RangeDirection']

    mapped_df['state'] = 'OK'
    mapped_df['state_enabling_act'] = '34. Stat. 267-286 , esp. 272, 274-75 (1906)'
    mapped_df['trust_name'] = 'Oklahoma State University'
    mapped_df['managing_agency'] = 'Commissioners of the Land Office'
    mapped_df['university'] = 'Oklahoma State University'

    if activity_type == 'agriculture':
        mapped_df['activity'] = 'Agriculture'
        mapped_df['rights_type'] = 'surface'
    elif activity_type == 'longterm':
        mapped_df['activity'] = 'Longterm Commercial'
        mapped_df['rights_type'] = 'surface'
    elif activity_type == 'mineral':
        mapped_df['activity'] = 'Mineral Lease'
        mapped_df['rights_type'] = 'subsurface'

    mapped_df['object_id'] = mapped_df.index + 1

    mapped_df = mapped_df[['object_id',
                           'state',
                           'state_enabling_act',
                           'trust_name',
                           'managing_agency',
                           'university',
                           'acres',
                           'meridian',
                           'section',
                           'aliquot',
                           'township',
                           'range',
                           'activity',
                           'rights_type']]
    return mapped_df


def main(
    stl_path: Path,
    stl_path_geo: Path,
    stl_path_geo_wgs84,
    cession_price_path: Path,
    ok_ag_path: Path,
    ok_longterm_path: Path,
    ok_mineral_path: Path,
    out_dir: Path,
):
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)

    log.info(f'reading {stl_path}')

    stl_data = pd.read_csv(str(stl_path), low_memory=False)
    stl_geo = gpd.read_file(stl_path_geo)
    stl_geo_wgs84 = gpd.read_file(stl_path_geo_wgs84)

    log.info(f'reading {cession_price_path}')
    price_data = pd.read_csv(cession_price_path)

    log.info(f'reading {ok_ag_path}')
    ok_ag_data = pd.read_csv(ok_ag_path)
    log.info(f'reading {ok_longterm_path}')
    ok_longterm_data = pd.read_csv(ok_longterm_path)
    log.info(f'reading {ok_mineral_path}')
    ok_mineral_data = pd.read_csv(ok_mineral_path)

    stl_w_price = add_price_columns(stl_data, price_data)
    ok_ag_data_mapped = map_and_impute_ok_data(ok_ag_data, 'agriculture')
    ok_longterm_data_mapped = map_and_impute_ok_data(ok_longterm_data, 'longterm')
    ok_mineral_data_mapped = map_and_impute_ok_data(ok_mineral_data, 'mineral')
    stl_w_price_and_ok = pd.concat([stl_w_price, ok_ag_data_mapped, ok_longterm_data_mapped, ok_mineral_data_mapped], ignore_index=True)
    stl_w_price_geo = gpd.GeoDataFrame(stl_w_price_and_ok, geometry=stl_geo.geometry, crs=stl_geo.crs)
    stl_w_price_geo_wgs84 = gpd.GeoDataFrame(stl_w_price_and_ok, geometry=stl_geo_wgs84.geometry, crs=stl_geo_wgs84.crs)

    log.info(f'final grist_data row_count: {stl_w_price_and_ok.shape[0]}')
    stl_w_price_and_ok.to_csv(out_dir / 'stl_dataset_extra_activities_plus_cessions_plus_prices.csv', index=False)
    stl_w_price_geo.to_file(
        out_dir / 'stl_dataset_extra_activities_plus_cessions_plus_prices.geojson',
        driver='GeoJSON'
    )
    stl_w_price_geo_wgs84.to_file(
        out_dir / 'stl_dataset_extra_activities_plus_cessions_plus_prices_wgs84.geojson',
        driver='GeoJSON'
    )
    log.info(f'original grist_data row_count: {stl_data.shape[0]}')


def run():
    print('running cession purchase price calculation')
    required_envs = ['DATA']
    missing_envs = [env for env in required_envs if os.environ.get(env) is None]
    if any(missing_envs):
        raise Exception(f'RequiredEnvVar: The following ENV vars must be set. {missing_envs}')

    data_tld = os.environ.get('DATA')
    prev_data_dir = Path(f'{data_tld}/stl_dataset/step_2_5').resolve()
    base_data_dir = Path(f'{data_tld}/stl_dataset/step_3').resolve()
    cession_price_path = base_data_dir / 'input/Cession_Data.csv'

    prev_step_output = prev_data_dir / 'output'
    stl_path = next((f for f in prev_step_output.iterdir() if 'csv' in f.name), None)
    ok_ag_path = base_data_dir / 'input/still_missing-agriculture_parcels.csv'
    ok_longterm_path = base_data_dir / 'input/still_missing-longterm_parcels.csv'
    ok_mineral_path = base_data_dir / 'input/still_missing-mineral_parcels.csv'
    stl_path_geo = prev_data_dir / 'output/stl_dataset_extra_activities_plus_cessions.geojson'
    stl_path_geo_wgs84 = prev_data_dir / 'output/stl_dataset_extra_activities_plus_cessions_wgs84.geojson'
    if not stl_path:
        raise Exception(f'MissingInputFile: No CSV was found in: {prev_step_output}.')

    out_dir = base_data_dir / 'output'
    main(
        stl_path=stl_path,
        ok_ag_path=ok_ag_path,
        ok_longterm_path=ok_longterm_path,
        stl_path_geo=stl_path_geo,
        ok_mineral_path=ok_mineral_path,
        stl_path_geo_wgs84=stl_path_geo_wgs84,
        cession_price_path=cession_price_path,
        out_dir=out_dir
    )


if __name__ == '__main__':
    run()
