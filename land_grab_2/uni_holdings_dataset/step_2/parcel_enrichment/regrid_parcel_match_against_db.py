import concurrent.futures
import logging
import traceback
from pathlib import Path
from typing import Optional, List, Any, Union

import pandas as pd

from land_grab_2.init_database.db.gristdb import GristDB
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.entities import Parcel
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.az_universityofarizona_parser import azua_parser
# from land_grab.university_real_estate.parsers.ca_universityofcalifornia_parser import cauc_parser
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.fl_universityofflorida_parser import fluf_parser
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.in_purdueuniversity_parser import inpu_parser
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.mo_universityofmissouri_parser import moum_parser
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.nj_rutgersuniversity_parser import njru_parser
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.oh_ohiostateuniversity_parser import ohos_parser
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.tn_universityoftennessee_parser import \
    tnut_parser
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.tx_texasaandm_mineral_parser import \
    txam_mineral_parser
from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.parsers.tx_texasaandm_property_parser import \
    txam_property_parser

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


def safe_parse(parser, line) -> Optional[Parcel]:
    try:
        return parser([str(s) for s in line])
    except:
        return None


def unwrap_futures(futures) -> List[Parcel]:
    concurrent.futures.wait(futures)
    parcels = []
    for f in futures:
        result: Union[List[Parcel], Parcel] = f.result()

        if not result:
            continue

        if not isinstance(result, list):
            result = [result]

        parcels += result

    return parcels


def pandas_extract_parcel_numbers(csv_path: Path, parser, batch_size=10) -> List[Parcel]:
    try:
        pandas_futures = []
        df = pd.read_csv(csv_path, skiprows=8, index_col=False, dtype=str)
        rows = list(df.iterrows())
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as t_pool:
            for i, line in rows:
                line = line.tolist()
                pandas_futures.append(t_pool.submit(safe_parse, parser, line))

        return unwrap_futures(pandas_futures)
    except Exception as err:
        log.error(f'pandas_extract_parcel_numbersError for csv {csv_path.name}: {err}')
        return []


def line_by_line_read_parcel_numbers(csv_path: Path, parser, batch_size=10) -> List[Parcel]:
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


def catalog_unmatched_parcels(parcel_numbers: List[Parcel], regrid_parcels):
    if not regrid_parcels:
        return parcel_numbers

    regrid_parcel_numbers = set([])
    for r in regrid_parcels:
        regrid_parcel_numbers.add(r['parcelnumb_no_formatting'])
        regrid_parcel_numbers.add(r['alt_parcelnumb2'])

    unmatched_parcels = []
    for p in parcel_numbers:
        if p.normalized_number and p.normalized_number.strip() in regrid_parcel_numbers:
            continue

        if p.alt_county_parcel and p.alt_county_parcel.strip() in regrid_parcel_numbers:
            continue

        unmatched_parcels.append(p)

    return unmatched_parcels


def write_parcels_csv(output_dir,
                      outfile_name,
                      regrid_parcel_rows,
                      unmatched_parcels,
                      parcel_lookup_table):
    if not output_dir:
        output_dir = Path(f'').resolve()

    if not output_dir.exists():
        output_dir.mkdir(exist_ok=True, parents=True)

    scoped_dir = output_dir / outfile_name
    if not scoped_dir.exists():
        scoped_dir.mkdir(exist_ok=True, parents=True)

    unmatched_w_ctx = []
    for u in unmatched_parcels:
        if u.normalized_number and str(u.normalized_number.strip()) in parcel_lookup_table:
            p = parcel_lookup_table[u.normalized_number.strip()]
            unmatched_w_ctx.append(p.to_dict())
            continue

        if u.alt_county_parcel and str(u.alt_county_parcel.strip()) in parcel_lookup_table:
            p = parcel_lookup_table[u.alt_county_parcel.strip()]
            unmatched_w_ctx.append(p.to_dict())
            continue

    regrid_w_ctx = []
    for r in regrid_parcel_rows:
        ctx = Parcel().to_dict()
        parcelnumb = str(r['parcelnumb_no_formatting'])
        if parcelnumb in parcel_lookup_table:
            ctx = parcel_lookup_table[parcelnumb].to_dict()
        regrid_w_ctx.append({**r, **ctx})

    # log.info(f'writing matched and unmatched parcel_numbers for {outfile_name}')
    pd.DataFrame(regrid_w_ctx).to_csv(scoped_dir / 'matched.csv', index=False)
    pd.DataFrame(unmatched_w_ctx).to_csv(scoped_dir / 'not_matched.csv', index=False)


def parcel_match(db, csv, output_dir):
    parser = PARSER_MAPPING.get(csv.stem)
    strategy = PARSER_STRATEGIES.get(csv.stem)

    if not parser:
        log.error(f'NoParserError: No parcel_number-parser found for {csv.name}')
        return

    parcels: List[Parcel] = extract_parcel_numbers(csv, parser)

    parcel_lookup_table = {p.normalized_number.strip(): p for p in parcels if p.normalized_number}
    parcel_lookup_table_2 = {p.alt_county_parcel.strip(): p for p in parcels if p.alt_county_parcel}
    parcel_lookup_table = {**parcel_lookup_table, **parcel_lookup_table_2}

    parcel_numbers = [p.normalized_number.strip() for p in parcels if p.normalized_number]

    if not parcel_numbers:
        log.info(f'Found ZERO parcel numbers for {csv.name}')
        return

    # log.info(f'Found {len(parcel_numbers)} for {csv}')
    regrid_parcel_rows = db.search_column_value_in_set('regrid',
                                                       'parcelnumb_no_formatting',
                                                       parcel_numbers)

    unmatched_parcels = catalog_unmatched_parcels(parcels, regrid_parcel_rows)
    # only perform secondary search for tennessee
    if 'tn_ut' in csv.name and unmatched_parcels:
        unmatched_w_ctx = []
        for u in unmatched_parcels:
            if str(u.alt_county_parcel.strip()) in parcel_lookup_table:
                p = parcel_lookup_table[u.normalized_number.strip()]
                unmatched_w_ctx.append(p.alt_county_parcel.strip())

        if unmatched_w_ctx:
            regrid_parcel_rows_2 = db.search_column_value_in_set('regrid', 'alt_parcelnumb2', unmatched_w_ctx)
            regrid_parcel_rows = regrid_parcel_rows + regrid_parcel_rows_2
            unmatched_parcels = catalog_unmatched_parcels(parcels, regrid_parcel_rows)

    if len(unmatched_parcels) > len(regrid_parcel_rows):
        log.info(f'INVESTIGATE: {csv.name}')

    write_parcels_csv(output_dir, csv.stem, regrid_parcel_rows, unmatched_parcels, parcel_lookup_table)


def main(univ_csvs_dir: Path, output_dir: Optional[Path] = None):
    db = GristDB()
    university_csvs = list(univ_csvs_dir.iterdir())
    for csv in university_csvs:
        if csv.is_dir() or 'csv' not in csv.suffix:
            continue

        try:
            parcel_match(db, csv, output_dir)
        except Exception as err:
            traceback.print_exc()
            log.error(err)


if __name__ == '__main__':
    # univ_dir = Path('/Users/marcellebonterre/Downloads/parcel_ID_lists')
    # output_dir = Path('/Users/marcellebonterre/Downloads/parcel_ID_lists/parcel_id_regrid')
    univ_dir = Path('/tests/ignored_dir/foo')
    output_dir = Path('/tests/ignored_dir/foo/parcel_id_regrid')
    main(univ_dir, output_dir)
