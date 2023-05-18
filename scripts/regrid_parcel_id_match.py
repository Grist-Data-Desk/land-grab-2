# This program will accept two parameters:
# -p is a string representing the appropriate parser to use on a university reported parcel dataset
# -d is the path to the location of the university reported parcel dataset on the computer
# This script will also use the parser requested by the -p that exists within the land_grab package to
#   parse the dataset located at the path specified by -d
# Then it will also use the Regrid logic that exists within the land_grab package to match the cleaned parcel dataset
#   to find the matches between Regrid
# Then it will write the matched parcels to a .csv file.
import pandas as pd

from land_grab.university_real_estate.parcel_extractor import regrid_matching
from land_grab.university_real_estate.parcel_list_parsers.az_universityofarizona_parser import azua_parser
from land_grab.university_real_estate.parcel_list_parsers.in_purdueuniversity_parser import inpu_parser
from land_grab.university_real_estate.parcel_list_parsers.mo_universityofmissouri_parser import moum_parser

parser_mapping = {
    'azua_parser':azua_parser,
    'inpu_parser': inpu_parser,
    'moum_parser': moum_parser,

} #azua_parser will change to reflect diff universities

def read_csv(dataset_location):
    csv = pd.read_csv(dataset_location)
    return csv
def write_csv(data):
    pass

def parse_arguments():
    pass

def main():
    args = parse_arguments() # will be a dictionary

    requested_parser = args['parser']
    dataset_location = args['dataset']
    parcel_database = args['database'] # database will be a path to where the Regrid .csvs are (by county in a state folder)

    parser = parser_mapping[requested_parser]
    data = read_csv(dataset_location) # the csv here is the cleaned parcel id list

    parcel_id_list = parser(data)
    regrid_matched_parcels_parcel_id = regrid_matching(parcel_id_list, parcel_database) # will need two parameters in regrid_matching

    write_csv(regrid_matched_parcels_parcel_id) # write_csv doesn't exist yet





if __name__ == '__main__':
    main()