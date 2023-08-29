import concurrent.futures
import itertools
import logging
import numpy as np
import traceback
from pathlib import Path
from typing import Optional, List, Tuple, Any

import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

from land_grab.db.gristdb import GristDB
from land_grab.university_real_estate.parcel_list_parsers.az_universityofarizona_parser import azua_parser
# from land_grab.university_real_estate.parcel_list_parsers.ca_universityofcalifornia_parser import cauc_parser
from land_grab.university_real_estate.parcel_list_parsers.fl_universityofflorida_parser import fluf_parser
from land_grab.university_real_estate.parcel_list_parsers.in_purdueuniversity_parser import inpu_parser
from land_grab.university_real_estate.parcel_list_parsers.mo_universityofmissouri_parser import moum_parser
from land_grab.university_real_estate.parcel_list_parsers.nj_rutgersuniversity_parser import njru_parser
from land_grab.university_real_estate.parcel_list_parsers.oh_ohiostateuniversity_parser import ohos_parser
from land_grab.university_real_estate.parcel_list_parsers.tn_universityoftennessee_parser import tnut_parser
from land_grab.university_real_estate.parcel_list_parsers.tx_texasaandm_mineral_parser import txam_mineral_parser
from land_grab.university_real_estate.parcel_list_parsers.tx_texasaandm_property_parser import txam_property_parser

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

PARSER_MAPPING = {
    'az_ua_parcel_list_raw': azua_parser,
    'in_purdue_parcel_list_raw': inpu_parser,
    'mo_um_parcel_list_raw': moum_parser,
    'oh_osu_parcel_list_raw': ohos_parser,

    # 'ca_uca_parcel_list_raw': cauc_parser,
    'fl_uf_parcel_list_raw': fluf_parser,
    'nj_rutgers_parcel_list_raw': njru_parser,
    'tn_ut_parcel_list_raw': tnut_parser,
    'tx_txam_surfacemineralholdings_parcel_list_raw': txam_mineral_parser,
    'tx_txam_propertyholdings_parcel_list_raw': txam_property_parser,
}

PARSER_STRATEGIES = {
    'tx_txam_surfacemineralholdings_parcel_list_raw': 'pandas',
    'tx_txam_propertyholdings_parcel_list_raw': 'pandas',
}


def safe_parse(parser, line):
    try:
        return parser([str(s) for s in line])
    except:
        return None


def unwrap_futures(futures):
    concurrent.futures.wait(futures)
    parcel_numbers = []
    for f in futures:
        result = f.result()
        if not result:
            continue

        if not isinstance(result, list):
            result = [str(result)]

        for r in result:
            if not isinstance(r, str):
                r = str(r)
            parcel_numbers.append(r.strip())

    return parcel_numbers


def pandas_extract_parcel_numbers(csv_path: Path, parser, batch_size=10):
    try:
        panda_futures = []
        df = pd.read_csv(csv_path, skiprows=8, index_col=False, dtype=str)
        rows = list(df.iterrows())
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as t_pool:
            for i, line in rows:
                line = line.tolist()
                panda_futures.append(t_pool.submit(safe_parse, parser, line))

        return unwrap_futures(panda_futures)
    except Exception as err:
        log.error(f'pandas_extract_parcel_numbersError for csv {csv_path.name}: {err}')
        return []


def line_by_line_read_parcel_numbers(csv_path: Path, parser, batch_size=10):
    try:
        line_by_line_futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as t_pool:
            with csv_path.resolve().open() as file:
                while line := file.readline():
                    line_arr = line.rstrip().split(',')
                    line_by_line_futures.append(t_pool.submit(safe_parse, parser, line_arr))

        return unwrap_futures(line_by_line_futures)
    except Exception as err:
        log.error(f'line_by_line_read_parcel_numbers for csv {csv_path.name}: {err}')
        return []


def choose_largest(choices: List[List[Any]]):
    strategies_lens = [len(l) for l in choices]
    argmax = strategies_lens.index(max(strategies_lens))
    return choices[argmax]


def extract_parcel_numbers(csv_path: Path, parser, batch_size=10):
    parcel_numbers_pandas = pandas_extract_parcel_numbers(csv_path, parser, batch_size=batch_size)
    parcel_numbers_line_by_line = line_by_line_read_parcel_numbers(csv_path, parser, batch_size=batch_size)
    parcel_numbers = choose_largest([parcel_numbers_pandas, parcel_numbers_line_by_line])

    return parcel_numbers


def catalog_unmatched_parcels(parcel_numbers, regrid_parcels):
    if not regrid_parcels:
        return parcel_numbers
    regrid_parcel_numbers = set([r['parcelnumb_no_formatting'] for r in regrid_parcels])
    unmatched_parcels = set(parcel_numbers) - regrid_parcel_numbers
    return unmatched_parcels


def write_parcels_csv(output_dir, outfile_name, regrid_parcel_rows, unmatched_parcels):
    if not output_dir:
        output_dir = Path(f'.').resolve()

    if not output_dir.exists():
        output_dir.mkdir(exist_ok=True, parents=True)

    scoped_dir = output_dir / outfile_name
    if not scoped_dir.exists():
        scoped_dir.mkdir(exist_ok=True, parents=True)

    # log.info(f'writing matched and unmatched parcel_numbers for {outfile_name}')
    pd.DataFrame(regrid_parcel_rows).to_csv(scoped_dir / 'matched.csv', index=False)
    pd.DataFrame({
        'unmatched_parcelnumber': [str(p) for p in unmatched_parcels]
    }).to_csv(scoped_dir / 'not_matched.csv', index=False)


def main(univ_csvs_dir: Path, output_dir: Optional[Path] = None):
    db = GristDB()
    university_csvs = list(univ_csvs_dir.iterdir())
    for csv in university_csvs:
        if csv.is_dir() or 'csv' not in csv.suffix:
            continue

        try:
            parser = PARSER_MAPPING.get(csv.stem)
            strategy = PARSER_STRATEGIES.get(csv.stem)

            if not parser:
                log.error(f'NoParserError: No parcel_number-parser found for {csv.name}')
                continue

            parcel_numbers = extract_parcel_numbers(csv, parser)
            if not parcel_numbers:
                log.info(f'Found ZERO parcel numbers for {csv.name}')
                continue

            # log.info(f'Found {len(parcel_numbers)} for {csv}')
            regrid_parcel_rows = db.search_column_value_in_set('regrid',
                                                               'parcelnumb_no_formatting',
                                                               parcel_numbers)

            unmatched_parcels = catalog_unmatched_parcels(parcel_numbers, regrid_parcel_rows)
            if len(unmatched_parcels) > len(regrid_parcel_rows):
                log.info(f'INVESTIGATE: {csv.name}')

            write_parcels_csv(output_dir, csv.stem, regrid_parcel_rows, unmatched_parcels)
        except Exception as err:
            traceback.print_exc()
            log.error(err)


if __name__ == '__main__':
    univ_dir = Path('/Users/marcellebonterre/Downloads/parcel_ID_lists')
    output_dir = Path('/Users/marcellebonterre/Downloads/parcel_ID_lists/parcel_id_regrid')
    # univ_dir = Path('/Users/marcellebonterre/Projects/land-grab-2/tests/foo')
    # output_dir = Path('/Users/marcellebonterre/Projects/land-grab-2/tests/foo/parcel_id_regrid')
    main(univ_dir, output_dir)
