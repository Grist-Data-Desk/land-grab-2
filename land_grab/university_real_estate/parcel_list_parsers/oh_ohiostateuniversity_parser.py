def ohos_parser(l):
    # column 1 or [0], take out - and spaces, concatenate
    # ignore header cell (ParcelNo)

    parcel_number = l[0]

    if 'ParcelNo' in parcel_number:
        return None

    if '-' in parcel_number:
        parcel_number = ''.join(parcel_number.split('-'))

    if '.' in parcel_number:
        parcel_number = ''.join(parcel_number.split('.'))

    return parcel_number
