import logging
import os
from pathlib import Path

import geopandas
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

        cession_nums = [] if 'all_cession_numbers' not in row.keys() else row['all_cession_numbers'].split(',')
        cession_prices = {}
        for i, cession in enumerate(cession_nums, start=1):
            cession_price_rows = price_data[price_data['Cession_Number'] == cession].to_dict(orient='records')
            if not cession_price_rows:
                continue
            price_info = cession_price_rows[0]['US_Paid_Per_Acre'].lstrip('$')
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
    gdf = geopandas.GeoDataFrame(df, geometry=df.geometry, crs=stl_data.crs)

    return gdf


def main(stl_path: Path, cession_price_data: Path, the_out_dir: Path):
    if not the_out_dir.exists():
        the_out_dir.mkdir(parents=True, exist_ok=True)

    log.info(f'reading {stl_path}')
    stl_data = geopandas.read_file(str(stl_path))

    log.info(f'reading {cession_price_data}')
    price_data = geopandas.read_file(str(cession_price_data))

    stl_w_price = add_price_columns(stl_data, price_data)

    log.info(f'final grist_data row_count: {stl_w_price.shape[0]}')
    stl_w_price.to_csv(str(the_out_dir / 'updated_grist_stl.csv'), index=False)
    stl_w_price.to_file(str(the_out_dir / 'updated_grist_stl.geojson'), driver='GeoJSON')
    log.info(f'original grist_data row_count: {stl_data.shape[0]}')


def run():
    print('running cession purchase price calculation')
    required_envs = ['DATA']
    missing_envs = [env for env in required_envs if os.environ.get(env) is None]
    if any(missing_envs):
        raise Exception(f'RequiredEnvVar: The following ENV vars must be set. {missing_envs}')

    data_tld = os.environ.get('DATA')
    data_directory = f'{data_tld}/stl_dataset/step_3'
    base_data_dir = Path(data_directory).resolve()
    out_dir = base_data_dir / 'output'
    cession_price_data = base_data_dir / 'input/Cession_Data.csv'

    step_2_data_directory = Path(f'{data_tld}/stl_dataset/step_2').resolve()
    stl = step_2_data_directory / 'output/updated_grist_stl.geojson'
    main(stl, cession_price_data, out_dir)


if __name__ == '__main__':
    run()
