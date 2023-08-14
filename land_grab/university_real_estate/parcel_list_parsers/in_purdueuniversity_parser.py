def inpu_parser(l):
    parcel_number = l[0]

    if len(parcel_number.split(' ')) > 1:
        return None

    if '-' not in parcel_number:
        return parcel_number