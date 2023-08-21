import concurrent.futures
import itertools
import logging
import traceback
from pathlib import Path
from typing import Optional, List

import pandas as pd

from land_grab.db.gristdb import GristDB
from land_grab.university_real_estate.parcel_list_parsers.az_universityofarizona_parser import azua_parser
from land_grab.university_real_estate.parcel_list_parsers.ca_universityofcalifornia_parser import cauc_parser
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


def extract_parcel_numbers(csv_path: Path, parser, batch_size=10) -> List[str]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as t_pool:
        with csv_path.resolve().open() as file:
            futures = []
            while line := file.readline():
                futures.append(t_pool.submit(parser, line.rstrip().split(',')))

        parcel_numbers = []
        for f in concurrent.futures.as_completed(futures):
            result = f.result()
            if result:
                if not isinstance(result, list):
                    result = [result]
                parcel_numbers += [r.strip() for r in result]

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

    log.info(f'writing matched and unmatched parcel_numbers for {outfile_name}')
    pd.DataFrame(regrid_parcel_rows).to_csv(scoped_dir / 'matched.csv', index=False)
    pd.DataFrame(unmatched_parcels,
                 columns=['unmatched_parcelnumber']).to_csv(scoped_dir / 'not_matched.csv', index=False)


def main(univ_csvs_dir: Path, output_dir: Optional[Path] = None):
    db = GristDB()
    university_csvs = list(univ_csvs_dir.iterdir())
    for csv in university_csvs:
        if csv.is_dir() or 'csv' not in csv.suffix:
            log.info(f'IGNORING dir item: {csv}')
            continue

        try:
            parser = PARSER_MAPPING.get(csv.stem)
            if parser:
                parcel_numbers = extract_parcel_numbers(csv, parser)
                if not parcel_numbers:
                    log.info(f'Found ZERO parcel numbers for {csv}')
                    continue
                else:
                    log.info(f'Found {len(parcel_numbers)} for {csv}')

                regrid_parcel_rows = db.search_column_by_values('regrid',
                                                                'parcelnumb_no_formatting',
                                                                parcel_numbers)
                unmatched_parcels = catalog_unmatched_parcels(parcel_numbers, regrid_parcel_rows)
                if len(unmatched_parcels) > len(regrid_parcel_rows):
                    log.info(f'INVESTIGATE: {csv}')

                write_parcels_csv(output_dir, csv.stem, regrid_parcel_rows, unmatched_parcels)
            else:
                log.error(f'NoParserError: No parcel_number-parser found for {csv}')
        except Exception as err:
            traceback.print_exc()
            log.error(err)


if __name__ == '__main__':
    univ_dir = Path('/Users/marcellebonterre/Downloads/parcel_ID_lists')
    output_dir = Path('/Users/marcellebonterre/Downloads/parcel_ID_lists/parcel_id_regrid')
    # univ_dir = Path('/Users/marcellebonterre/Projects/land-grab-2/tests/foo')
    # output_dir = Path('/Users/marcellebonterre/Projects/land-grab-2/tests/foo/parcel_id_regrid')
    main(univ_dir, output_dir)
