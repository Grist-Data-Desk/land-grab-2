from land_grab.university_real_estate.entities import Parcel


def txam_property_parser(l) -> Parcel:
    # for property holdings, don't include any with text string. just take out - and concatenate
    # column 1 or [0]
    # ignore rows 1-8 (string descriptions)

    parcel_number = l[0]
    county = l[1].replace(' - ', '')
    p = Parcel(original_number=parcel_number, county=county)

    if len(parcel_number.split('-')) != 3:
        return None

    if '-' in parcel_number:
        parcel_number = ''.join(parcel_number.split('-'))
        p.normalized_number = parcel_number

    return p
