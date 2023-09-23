from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.entities import Parcel


def njru_parser(l) -> Parcel:
    parcel_number = l[2]
    p = Parcel(original_number=parcel_number, county=l[6])

    if 'PAMS_PIN' in parcel_number:
        return None

    if '_' in parcel_number:
        parcel_number = ''.join(parcel_number.split('_'))
        p.normalized_number = parcel_number

    if '.' in parcel_number:
        parcel_number = ''.join(parcel_number.split('.'))
        p.normalized_number = parcel_number

    p.normalized_number = parcel_number
    return p
