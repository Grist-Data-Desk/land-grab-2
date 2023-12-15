import itertools
import logging
import os
from pathlib import Path

import geopandas
import numpy as np
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import GIS_ACRES

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

not_a_cession = ['336', '368', '496', '510', '524', '525', '552', '591', '596', '599', '618', '621', '625', '632',
                 '633', '651', '702', '713', '718', '540a']
unknown_cession_data = ['717']


def get_price_paid_per_acre(cession, price_info):
    if cession in not_a_cession:
        return 'N/A'

    if cession in unknown_cession_data:
        return 'Unknown'

    return 0.0 if not price_info else float(price_info)


def add_price_columns(stl_data, price_data):
    log.info('processing price information')
    all_columns = stl_data.columns.tolist()
    cession_columns = [c for c in all_columns if c.endswith('present_day_tribe')]
    cession_price_columns = [f'C{i}_price_paid_per_acre' for i, _ in enumerate(cession_columns, start=1)]

    out_rows = []
    cession_prices_simple = {}
    for row in stl_data.to_dict(orient='records'):
        # ensure all cessions have a correlated, initially blank, price column
        for c in cession_price_columns:
            row[c] = ''

        cession_nums = ([]
                        if ('all_cession_numbers' not in row.keys() or
                            (not isinstance(row['all_cession_numbers'], str) and np.isnan(row['all_cession_numbers'])))
                        else row['all_cession_numbers'].split(','))
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

            price_info = cession_price_rows[0]['US_Paid_Per_Acre - Inflation Adjusted'].lstrip('$')
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


def main(stl_path: Path, cession_price_data: Path, the_out_dir: Path):
    if not the_out_dir.exists():
        the_out_dir.mkdir(parents=True, exist_ok=True)

    log.info(f'reading {stl_path}')
    stl_data = pd.read_csv(str(stl_path), low_memory=False)

    log.info(f'reading {cession_price_data}')
    price_data = geopandas.read_file(str(cession_price_data))

    stl_w_price = add_price_columns(stl_data, price_data)

    log.info(f'final grist_data row_count: {stl_w_price.shape[0]}')
    stl_w_price.to_csv(str(the_out_dir / 'stl_dataset_extra_activities_plus_cessions_plus_prices.csv'), index=False)
    # stl_w_price.to_file(str(the_out_dir / 'stl_dataset_extra_activities_plus_cessions_plus_prices.geojson'),
    #                     driver='GeoJSON')
    log.info(f'original grist_data row_count: {stl_data.shape[0]}')


def run():
    print('running cession purchase price calculation')
    required_envs = ['DATA']
    missing_envs = [env for env in required_envs if os.environ.get(env) is None]
    if any(missing_envs):
        raise Exception(f'RequiredEnvVar: The following ENV vars must be set. {missing_envs}')

    data_tld = os.environ.get('DATA')
    base_data_dir = Path(f'{data_tld}/stl_dataset/step_3').resolve()
    cession_price_data = base_data_dir / 'input/Cession_Data.csv'

    prev_step_output = Path(f'{data_tld}/stl_dataset/step_2_5/output').resolve()
    stl = next(
        (f for f in prev_step_output.iterdir() if 'csv' in f.name),
        None
    )
    if not stl:
        raise Exception(f'MissingInputFile: No CSV was found in: {prev_step_output}.')

    out_dir = base_data_dir / 'output'
    main(stl, cession_price_data, out_dir)


if __name__ == '__main__':
    run()
