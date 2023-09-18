from land_grab_2.uni_holdings_dataset.step_2.parcel_enrichment.entities import Parcel


def ohos_parser(l) -> Parcel:
    # column 1 or [0], take out - and spaces, concatenate
    # ignore header cell (ParcelNo)

    parcel_number = l[0]
    p = Parcel(original_number=parcel_number, county=l[5])

    if 'ParcelNo' in parcel_number:
        return None

    if '-' in parcel_number:
        parcel_number = ''.join(parcel_number.split('-'))
        p.normalized_number = parcel_number

    if '.' in parcel_number:
        parcel_number = ''.join(parcel_number.split('.'))
        p.normalized_number = parcel_number

    return p
