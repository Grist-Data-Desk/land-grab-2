def tnut_parser(l):
    # take out spaces and concatenate
    # parcel code column 3 (or [2])
    # ignore header cell

    parcel_number = l[2]

    if 'Parcel Code' in l:
        return None

    if ' ' in parcel_number:
        parcel_number = ''.join(parcel_number.split(' '))
        return parcel_number
