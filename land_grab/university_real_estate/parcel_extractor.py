# Read file [downloaded list of parcel ID #s from University of Arizona]
#   line by line
#   split the line on commas
#   if line contains only one item [some lines contain county names], skip.
#   otherwise, save first item as parcel number.
# def parse_parcel_number is the process to clean and get university-reported parcel # IDs.

import csv
from pathlib import Path

def parse_parcel_number(filename):
    parcel_numbers = []
    with open(filename) as file:
        while line := file.readline():
            l = line.rstrip().split(',')
            parcel_number = l[0]
            if len(l) < 2:
                continue
            elif len(parcel_number.split(' ')) > 1:
                continue
            elif len(parcel_number.split('-')) != 3:
                if not all(d in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] for d in parcel_number):
                    continue
            else:
                if '-' in parcel_number:
                    parcel_number = ''.join(parcel_number.split('-'))
                parcel_numbers.append(parcel_number)

    return parcel_numbers

# Download all AZ county .csv zip files to drive (from Cyberduck)
#   create AZ-specific folder and compare parcel_numbers list (University of AZ reported)
#   against rows in each county .csv in AZ folder.
#   *One of the csv files was hidden, so filter out for '.' in csv file name.
# def main is the process to compare parcel # IDs with Regrid data and select matches.
# can we link to Cyberduck folders?

def main():
    saved = []
    database_directory = Path('/Users/mpr/Documents/01_Current Projects/Grist_LGU2/AZ').resolve()
    parcel_numbers = parse_parcel_number('/data_local/az_ua_parcel_list.csv')
    csvs = list(database_directory.glob('*.csv'))
    for csv_file in csvs:
        if '.' == csv_file.name[0]:
            continue
        with csv_file.open() as f:
            real_csv = csv.reader(f)
            for row in real_csv:
                parcel_number = row[3]
                if parcel_number in parcel_numbers:
                    saved.append(row)

    file = open('data_local/matchingparcels_regrid_uaz.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(saved)

    file = open('data_local/uazparcelnum.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(parcel_numbers)

    assert 1

if __name__ == '__main__':
    main()

# todo - compare lists!