# for surface+mineral, ignore blanks and ones that say "Parcel Number", take out spaces and - and concatenate
# column 3 or [2]

def txam_mineral_parser(l):

  parcel_number = l[2]

  if len(parcel_number.split('-')) != 3:
    return None

  if '-' in parcel_number:
    parcel_number = ''.join(parcel_number.split('-'))

  return parcel_number

