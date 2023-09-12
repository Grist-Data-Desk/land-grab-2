from tasks.to_be_moved.land_grab.university_real_estate.entities import Parcel


def inpu_parser(l) -> Parcel:
    # just take column 1 or [0], ignore header cell
    parcel_number = l[0]
    p = Parcel(original_number=parcel_number, county=l[2])

    if 'Parcel ID Number' in parcel_number:
        return None

    p.normalized_number = parcel_number
    return p
