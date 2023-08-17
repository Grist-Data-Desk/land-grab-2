import re


def existing():
  def delimit_list(parcel_number):
    delimited_parcels = re.split(r'[\/&;]', parcel_number)
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

    # if parcel_number is a single parcel ID that contains ()s or is a long string description

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
          fixed_suite = re.sub(r'Suite\s\d+\w*\s-\s', '', parcel)

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


def basic_clean(parcel_number):
  if '-' in parcel_number:
    parcel_number = ''.join(parcel_number.split('-'))

  if '.' in parcel_number:
    parcel_number = ''.join(parcel_number.split('.'))

  if ' ' in parcel_number:
    parcel_number = ''.join(parcel_number.split(' '))

  return parcel_number


def parse_case_1(case_1):
  parts = case_1.split('&')
  colon_parts = [p.split(':') for p in parts]
  pids = [p[-1].strip() for p in colon_parts]
  return pids


def parse_case_2(case_2):
  clean_pids = []
  first, second = case_2.split('(')
  clean_pids.append(basic_clean(first))
  second_group = basic_clean(second.replace(')', ''))

  if second_group and all(d.isdigit() for d in second_group):
    clean_pids.append(second_group)
  return clean_pids


def parse_case_3(case_3):
  if 'City' in case_3 and 'County' in case_3:
    pids = []

    city_idx = case_3.find('City')
    county_idx = case_3.find('County')
    pid_region = case_3[city_idx:county_idx]
    pid_region_parts = pid_region.split(' ')
    if pid_region_parts:
      pid_with_county_code = sorted(pid_region_parts, key=len, reverse=True)[0]
      pid_start = next((i for i, c in enumerate(pid_with_county_code) if c.isdigit()), None)
      pid = pid_with_county_code[pid_start:]
      pids.append(pid)

    beginning_half = case_3[:city_idx]
    if ';' in beginning_half:
      delim_idx = beginning_half.find(';')
      clean_extra_info = case_3[delim_idx + 1:]
      pids.append(clean_extra_info)
    else:
      pids.append(case_3)

    return pids


def parse_case_4(case_4):
  pass


if __name__ == '__main__':
  case_1 = '8121 Evarts: 14H430334 & 8112 Oxeye: 14H431021'
  assert ['14H430334', '14H431021'] == parse_case_1(case_1)

  case_2 = '71-09-1.0-02-004-019-001.000 (07280.00)'
  assert ['71091002004019001000', '0728000'] == parse_case_2(case_2)

  case_3 = '30-810-13-05-00-0-00-000;143427 (City), JA30810130500000000 (County); Resurvey of Mulkey Park'
  case_6 = '125285 (City); JA29540160100000000 (County)'
  assert ['30810130500000000', '143427 (City), JA30810130500000000 (County); Resurvey of Mulkey Park'] == parse_case_3(
    case_3)
  assert ['29540160100000000', '125285 (City); JA29540160100000000 (County)'] == parse_case_3(case_6)

  case_4 = '25-400-20-00-002.00 (part of this parcel - NW to Hwy Y, south to edge, west to edge)'
  assert ['29540160100000000', '125285 (City); JA29540160100000000 (County)'] == parse_case_4(case_4)

  case_5 = '16-501-00-02-037.00 01 & 16-501-00-02-037.02 01'
  case_7 = '16-608-00-04-001.00.01 (50x260 = 0.3 acres); west half of this parcel'

  case_8 = '14H431957 - Florissant Road; 14H431063 - 4122 Lowen Drive'
  case_9 = '$5,000 for 10 acres in T21N R13E S31; $3,500 for 10 acres in T20N, R13E S11'