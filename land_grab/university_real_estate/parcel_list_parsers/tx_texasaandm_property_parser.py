def txam_property_parser(l):
    # for property holdings, don't include any with text string. just take out - and concatenate
    # column 1 or [0]
    # ignore rows 1-8 (string descriptions)

    parcel_number = l[0]

    if len(parcel_number.split('-')) != 3:
        return None

    if '-' in parcel_number:
        parcel_number = ''.join(parcel_number.split('-'))

    return parcel_number
