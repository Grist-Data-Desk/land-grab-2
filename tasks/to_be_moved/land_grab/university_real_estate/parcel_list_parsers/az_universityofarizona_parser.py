from tasks.to_be_moved.land_grab.university_real_estate.entities import Parcel


def normalize_parcel_number(l):
    parcel_number = l[0]
    p = Parcel(original_number=parcel_number)
    if len(l) < 2:
        return None

    if len(parcel_number.split(' ')) > 1:
        return None

    if len(parcel_number.split('-')) != 3:
        if not all(d in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] for d in parcel_number):
            return None

    if '-' in parcel_number:
        parcel_number = ''.join(parcel_number.split('-'))
        p.normalized_number = parcel_number
        return p

    return p


def azua_parser(l) -> Parcel:
    parcel = normalize_parcel_number(l)
    return parcel
