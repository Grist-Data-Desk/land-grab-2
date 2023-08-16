import re

def basic_clean(l):
  if '-' in parcel_number:
    parcel_number = ''.join(parcel_number.split('-'))

  if '.' in parcel_number:
    parcel_number = ''.join(parcel_number.split('.'))

  if ' ' in parcel_number:
    parcel_number = ''.join(parcel_number.split(''))

def moum_parser(l):
  # if there are ., -, or spaces, take those out and concatenate
  # if there are ; or & symbols, those are delimiters; the values listed are individual parcel IDs
  # if there is a string description, return that line so we can inspect
  # if there are values within parens, return that line so we can inspect
  # use column 8 or [7]
  # ignore header cell

  parcel_number = l[7]



  # if parcel_number is a single parcel ID

   #if parcel_number is a single parcel ID that contains ()s or is a long string description

  # if parcel_number is a list of parcel IDs

   # if parcel_number is a list of parcel IDs that contains ()s or is a long string description


  delimited_parcels = re.split(r'[\/&;]',parcel_number)

  for parcel in delimited_parcels:
    if 'Suite' in parcel:
      fixed_suite = re.sub(r'Suite\s\d+\w*\s-\s','',parcel)

      if '-' in fixed_suite:
        parcel_number = ''.join(parcel_number.split('-'))

      if '.' in fixed_suite:
        parcel_number = ''.join(parcel_number.split('.'))

      if ' ' in fixed_suite:
        parcel_number = ''.join(parcel_number.split(''))



