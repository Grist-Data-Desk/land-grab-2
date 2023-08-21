def njru_parser(l):
  parcel_number = l[2]

  if 'PAMS_PIN' in parcel_number:
    return None

  if '_' in parcel_number:
    parcel_number = ''.join(parcel_number.split('_'))
    return parcel_number

  if '.' in parcel_number:
    parcel_number = ''.join(parcel_number.split('.'))
    return parcel_number

  return parcel_number