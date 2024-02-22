from land_grab_2.uni_holdings_dataset.also_old_stuff_figure_out.parcel_enrichment.entities import Parcel


def tnut_parser(l) -> Parcel:
    # take out spaces and concatenate
    # parcel code column 3 (or [2])
    # ignore header cell

    parcel_number = l[2]
    alt_county_parcel = l[3]
    p = Parcel(original_number=parcel_number, county=l[1], alt_county_parcel=alt_county_parcel)

    if 'Parcel Code' in parcel_number or 'ParcelCode' in parcel_number:
        return None

    if ' ' in parcel_number:
        parcel_number = ''.join(parcel_number.split(' '))
        p.normalized_number = parcel_number
        return p

    p.normalized_number = parcel_number
    return p
