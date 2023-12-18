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


def add_price_columns(stl_data, price_data):
    log.info('processing price information')
    all_columns = stl_data.columns.tolist()
    cession_columns = [c for c in all_columns if c.endswith('present_day_tribe')]
    cession_price_columns = [f'C{i}_price_paid_per_acre' for i, _ in enumerate(cession_columns, start=1)]

    out_rows = []
    for row in stl_data.to_dict(orient='records'):
        # ensure all cessions have a correlated, initially blank, price column
        for c in cession_price_columns:
            row[c] = ''

        cession_nums = ([]
                        if ('all_cession_numbers' not in row.keys() or
                            (not isinstance(row['all_cession_numbers'], str) and np.isnan(row['all_cession_numbers'])))
                        else row['all_cession_numbers'].split(','))
        cession_nums = list(itertools.chain.from_iterable([c if ' ' not in c else c.split(' ') for c in cession_nums]))
        cession_prices = {}
        for i, cession in enumerate(cession_nums, start=1):
            cession_price_rows = price_data[price_data['Cession_Number'] == cession].to_dict(orient='records')
            if not cession_price_rows:
                continue
            price_info = (
                cession_price_rows[0]["US_Paid_Per_Acre"].lstrip("$")
                if not pd.isna(cession_price_rows[0]["US_Paid_Per_Acre"])
                else cession_price_rows[0]["US_Paid_Per_Acre"]
            )
            row[f'C{i}_price_paid_per_acre'] = 0.0 if not price_info else float(price_info)
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
    for c in all_columns:
        if 'all_cession_numbers' in c:
            new_col_seq.append(c)
            new_col_seq.append('price_paid_for_parcel')
        elif c.endswith('present_day_tribe'):
            new_col_seq.append(cession_price_column_names.pop(0))
            new_col_seq.append(c)
        else:
            new_col_seq.append(c)

    df = pd.DataFrame(out_rows)
    df = df[new_col_seq]
    return df


def main(
    stl_path: Path,
    stl_path_geo: Path,
    stl_path_geo_wgs84,
    cession_price_path: Path,
    out_dir: Path,
):
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)

    log.info(f'reading {stl_path}')
    stl_data = pd.read_csv(stl_path)
    stl_geo = gpd.read_file(stl_path_geo)
    stl_geo_wgs84 = gpd.read_file(stl_path_geo_wgs84)

    log.info(f'reading {cession_price_path}')
    price_data = pd.read_csv(cession_price_path)

    stl_w_price = add_price_columns(stl_data, price_data)
    stl_w_price_geo = gpd.GeoDataFrame(stl_w_price, geometry=stl_geo.geometry, crs=stl_geo.crs)
    stl_w_price_geo_wgs84 = gpd.GeoDataFrame(stl_w_price, geometry=stl_geo_wgs84.geometry, crs=stl_geo_wgs84.crs)

    log.info(f'final grist_data row_count: {stl_w_price.shape[0]}')
    stl_w_price.to_csv(out_dir / 'stl_dataset_extra_activities_plus_cessions_plus_prices.csv', index=False)
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
    stl_path_geo = prev_data_dir / 'output/stl_dataset_extra_activities_plus_cessions.geojson'
    stl_path_geo_wgs84 = prev_data_dir / 'output/stl_dataset_extra_activities_plus_cessions_wgs84.geojson'
    if not stl_path:
        raise Exception(f'MissingInputFile: No CSV was found in: {prev_step_output}.')

    out_dir = base_data_dir / 'output'
    main(
        stl_path=stl_path,
        stl_path_geo=stl_path_geo,
        stl_path_geo_wgs84=stl_path_geo_wgs84,
        cession_price_path=cession_price_path,
        out_dir=out_dir
    )


if __name__ == '__main__':
    run()
