# This program will accept two parameters:
# -p is a string representing the appropriate parser to use on a university reported parcel dataset
# -d is the path to the location of the university reported parcel dataset on the computer
# This script will use the parser requested by the -p that exists within the land_grab package to
#   parse the dataset located at the path specified by -d
# Then it will also use the Regrid logic that exists within the land_grab package to match the cleaned parcel dataset
#   to find the matches between Regrid
# Then it will write the matched parcels to a .csv file.
import argparse
import csv
import itertools
from functools import partial
from pathlib import Path

from land_grab.university_real_estate.parcel_list_parsers.ca_universityofcalifornia_parser import cauc_parser
from land_grab.university_real_estate.parcel_list_parsers.fl_universityofflorida_parser import fluf_parser
from land_grab.university_real_estate.parcel_list_parsers.nj_rutgersuniversity_parser import njru_parser
from land_grab.university_real_estate.parcel_list_parsers.oh_ohiostateuniversity_parser import ohos_parser
from land_grab.university_real_estate.parcel_list_parsers.tn_universityoftennessee_parser import tnut_parser
from land_grab.university_real_estate.parcel_list_parsers.tx_texasaandm_mineral_parser import txam_mineral_parser
from land_grab.university_real_estate.parcel_list_parsers.tx_texasaandm_property_parser import txam_property_parser
from land_grab.university_real_estate.regrid_matching import regrid_matching
from land_grab.university_real_estate.parcel_list_parsers.az_universityofarizona_parser import azua_parser
from land_grab.university_real_estate.parcel_list_parsers.in_purdueuniversity_parser import inpu_parser
from land_grab.university_real_estate.parcel_list_parsers.mo_universityofmissouri_parser import moum_parser

parser_mapping = {
    'azua_parser': azua_parser,
    'inpu_parser': inpu_parser,
    'moum_parser': moum_parser,
    'ohos_parser': ohos_parser,

    'cauc_parser': cauc_parser,
    'fluf_parser': fluf_parser,
    'njru_parser': njru_parser,
    'tnut_parser': tnut_parser,
    'txam_mineral_parser': txam_mineral_parser,
    'txam_property_parser': txam_property_parser,
}  # azua_parser will change to reflect diff universities


def collect_database_csvs(parcel_database):  # parcel database is Regrid state folder
    database_directory = Path(parcel_database).resolve()
    database_dir_contents = list(database_directory.glob('*.csv'))
    csvs = []
    for csv_file in database_dir_contents:
        if '.' == csv_file.name[0]:  # did this to skip over "invisible files" (it was a problem with AZ.)
            continue
        if csv_file is not None:
            csvs.append(csv_file)
    return csvs


def do_on_csv_as_csv(csv_file, action):
    results = []
    with csv_file.open() as f:
        real_csv = csv.reader(f)
        for row in real_csv:
            result = action(row)
            if result is not None:
                results.append(result)
    return results


def do_on_csv(dataset_location, action):
    results = []
    with open(Path(dataset_location).resolve()) as file:
        while line := file.readline():
            l = line.rstrip().split(',')
            result = action(l)
            if result is not None:
                results.append(result)
    return list(itertools.chain.from_iterable(results))


def write_csv(data, output_location):
    file = open(Path(output_location).resolve(), 'w+')
    with file:
        write = csv.writer(file, quoting=csv.QUOTE_ALL)
        write.writerows(data)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog=__name__,
        description='This program matches university parcel id datasets against the Regrid dataset')

    parser.add_argument('-p', '--parser')  # option that takes a value
    parser.add_argument('-d', '--dataset')  # option that takes a value
    parser.add_argument('-o', '--output')  # option that takes a value
    parser.add_argument('-db', '--database')  # option that takes a value

    args = parser.parse_args()
    return vars(args)


def main():
    args = parse_arguments()  # will be a dictionary

    # database will be a path to where the Regrid .csvs are (by county in a state folder)
    requested_parser = args['parser']
    dataset_location = args['dataset']
    output_location = args['output']
    parcel_database = args['database']

    parser = parser_mapping[requested_parser]
    clean_uni_parcel_id_list = do_on_csv(dataset_location, parser)  # the csv here is the cleaned parcel id list

    regrid_matching_with_parcel_numbers = partial(regrid_matching, clean_uni_parcel_id_list)  # creating a new function
    # partial allows you to pass fewer params than it needs, partial allows me to fill in a new param with this function
    # ... new function only has one parameter
    csvs = collect_database_csvs(parcel_database)
    regrid_matched_parcels_parcel_id = []  # these are parcels that have been matched on the parcel_id field
    for csv in csvs:
        results = do_on_csv_as_csv(csv, regrid_matching_with_parcel_numbers)  # second param is a function
        regrid_matched_parcels_parcel_id += results  # += to join at list level not item level

    write_csv(regrid_matched_parcels_parcel_id, Path(output_location) / 'regrid_matched_parcels_parcel_id.csv')
    # data will be regrid_matched_parcel_ids
    clean_uni_parcel_id_list = [[p] for p in clean_uni_parcel_id_list]
    # reformat after it has been read by regrid list so that it can be properly formatted
    write_csv(clean_uni_parcel_id_list, Path(output_location) / 'clean_uni_parcel_id_list.csv')
    # data will be uni_parcel_id list


if __name__ == '__main__':
    main()

# to change things just changed stuff in the config - parameters:
# -p "azua_parser" -d "data_input/az_ua_parcel_list_raw.csv"
# -o "data_output" -db "/Users/mpr/Documents/01_Current Projects/Grist_LGU2/AZ"
