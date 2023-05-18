import csv


def main():
    matched_parcels = []
    with open('uazreportedparcels.csv', 'r') as t1, open('matchingparcels_regrid_uaz.csv', 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    with open('matched_parcels.csv', 'w') as outFile:  # Create CSV file with differences
        for line in fileone:
            if row[3] not in filetwo row[3]:
                outFile.write(line)

assert 1

if __name__ == '__main__':
    main()



