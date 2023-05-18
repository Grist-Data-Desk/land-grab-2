def azua_parser(filename):
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
