# Read file [downloaded list of parcel ID #s from University of Arizona]
#   line by line
#   split the line on commas
#   if line contains only one item [some lines contain county names], skip.
#   otherwise, save first item as parcel number.
# def parse_parcel_number is the process to clean and get university-reported parcel # IDs.

import csv
from pathlib import Path

from land_grab.university_real_estate.parcel_list_parsers.az_universityofarizona_parser import azua_parser


# Download all AZ county .csv zip files to drive (from Cyberduck)
#   create AZ-specific folder and compare parcel_numbers list (University of AZ reported)
#   against rows in each county .csv in AZ folder.
#   *One of the csv files was hidden, so filter out for '.' in csv file name.
# def main is the process to compare parcel # IDs with Regrid data and select matches.
# can we link to Cyberduck folders?

def regrid_matching(parcel_numbers, row):
    parcel_number = row[3]
    if parcel_number in parcel_numbers:
        return row

    # file = open('data_local/matchingparcels_regrid_uaz.csv', 'w+', newline='')
    # with file:
    #     write = csv.writer(file)
    #     write.writerows(saved)
    #
    # file = open('data_local/uazparcelnum.csv', 'w+', newline='')
    # with file:
    #     write = csv.writer(file)
    #     write.writerows(parcel_numbers)
