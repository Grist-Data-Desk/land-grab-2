import csv
from collections import Counter
from pathlib import Path


def write_csv(data, output_location):
    file = open(Path(output_location).resolve(), 'w+')
    with file:
        write = csv.writer(file, quoting=csv.QUOTE_ALL)
        write.writerows(data)


def main():
    regrid_parcel_nums = []
    matched_parcels = []
    with open('/data_output/clean_uni_parcel_id_list.csv', 'r') as t1, open(
            '/data_output/regrid_matched_parcels_parcel_id.csv', 'r') as t2:
        fileone = t1.readlines()
        fileone = [f.strip().strip('"') for f in fileone]
        filetwo = t2.readlines()
        for line in filetwo:
            row = line.split(',')
            regrid_parcel_nums.append(row[3].strip().strip('"'))

    no_match = set(fileone)-set(regrid_parcel_nums)

    c = Counter(regrid_parcel_nums)
    dupes = []
    for i, (item, quantity) in enumerate(c.items()):
        if quantity > 1:
            dupes.append([filetwo[i]])
    write_csv(dupes, '/Users/mpr/Pycharm Projects/land-grab-2/data_output/duplicated_parcels.csv')

    # with open('matched_parcels.csv', 'w') as outFile:  # Create CSV file with differences
    #     for line in fileone:
    #         if row[3] not in filetwo row[3]:
    #             outFile.write(line)

    assert 1


if __name__ == '__main__':
    main()
