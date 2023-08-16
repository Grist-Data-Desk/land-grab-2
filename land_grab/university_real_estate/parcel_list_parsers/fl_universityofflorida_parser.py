def fluf_parser(l):
  # take out - and concatenate
  # column 2 or [1]
  # ignore header cell

    parcel_number = l[1]

    if '-' in parcel_number:
      parcel_number = ''.join(parcel_number.split('-'))

      return parcel_number