def azua_parser(l):
    parcel_number = l[0]
    if len(l) < 2:
        return None

    if len(parcel_number.split(' ')) > 1:
        return None

    if len(parcel_number.split('-')) != 3:
        if not all(d in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] for d in parcel_number):
            return None

    if '-' in parcel_number:
        parcel_number = ''.join(parcel_number.split('-'))
        return parcel_number
