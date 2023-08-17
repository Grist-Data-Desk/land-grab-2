import re

def basic_clean(parcel_number):
  if '-' in parcel_number:
    parcel_number = ''.join(parcel_number.split('-'))

  if '.' in parcel_number:
    parcel_number = ''.join(parcel_number.split('.'))

  if ' ' in parcel_number:
    parcel_number = ''.join(parcel_number.split(''))

def delimit_list(parcel_number):
  delimited_parcels = re.split(r'[\/&;]',parcel_number)
  return delimited_parcels

def moum_parser(l):
# if there is text, then we take it out. if no text, then continue as normal
# if it's a list, it will be r'[; &*]'

  parcel_number = l[7]

  # if there are words or figures in parens
  complex_ids = re.compile(r'\w+', parcel_number)

# if parcel_number is a single parcel ID
# no ; or & or and
  if ';' or '&' or 'and' not in parcel_number:
    single_id_simple = basic_clean(parcel_number)
    return single_id_simple

   #if parcel_number is a single parcel ID that contains ()s or is a long string description

  # if parcel_number is a list of parcel IDs

  if ';' or '&' or 'and' in parcel_number:
    delimit_list(parcel_number)

    r'[; &*]'


# if parcel_number is a list of parcel IDs that contains ()s or is a long string description
# put the complex_ids list through the parsers here that will take further action:

  for parcel in complex_ids:
    if ';' or '&' or 'and' or ',' or '/' in parcel:
      delimited_parcel = re.split(r'[\/&;,and]', parcel_number)

      if 'Suite' in delimited_parcel:
        fixed_suite = re.sub(r'Suite\s\d+\w*\s-\s','',parcel)

        if '-' in fixed_suite:
          parcel_number = ''.join(parcel_number.split('-'))

        if '.' in fixed_suite:
          parcel_number = ''.join(parcel_number.split('.'))

        if ' ' in fixed_suite:
          parcel_number = ''.join(parcel_number.split(''))

      # these should create the variable: fixed_delimited_parcel
      # write out other parsers here

    return delimited_parcel
    return fixed_delimited_parcel




  # if there are ., -, or spaces, take those out and concatenate
  # if there are ; or & symbols, those are delimiters; the values listed are individual parcel IDs
  # if there is a string description, return that line so we can inspect
  # if there are values within parens, return that line so we can inspect
  # use column 8 or [7]
  # ignore header cell