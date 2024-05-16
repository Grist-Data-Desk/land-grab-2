import pandas as pd
from datetime import time


def get_first_div_id(state_abbrev, prime_meridian, twp_rng, sec):
  first_dot = twp_rng.find(".")
  second_dot = twp_rng.find(".", first_dot + 1)
  dash = twp_rng.find("-")
  twp = twp_rng[:5].replace(".", "")
  twp_dir = twp_rng[5:dash - 1]
  rng = twp_rng[dash + 3:second_dot + 2].replace(".", "")
  rng_dir = twp_rng[second_dot + 2:]
  try:
    section = str(int(sec))
  except:
    print("I don't like this one: {0} {1}".format(twp_rng, sec))

  # to pad a zero at the front of single digit sections
  section = section.zfill(2)

  # create a first division ID with appropriate zeros padding empty space
  first_div_id = state_abbrev + prime_meridian + twp + twp_dir.ljust(2, "0") + rng + rng_dir.ljust(2,
                                                                                                   "0") + "SN" + section.ljust(
    3, "0")

  return first_div_id


def get_second_div_id(state_abbrev, prime_meridian, twp_rng, sec, ali, surv, surv_type):
  # get the first division ID on which the second will be appended
  first_div_id = get_first_div_id(state_abbrev, prime_meridian, twp_rng, sec)

  second_div_list = []

  if surv_type == 'LOTS':
    # create second ID for lot
    second_div_list.append(first_div_id + "L" + str(int(surv)))
  elif surv_type != 'LOTS':

    # for converting half aliquots into subdivisions for use with ArcGIS PLSS SecDiv join
    ali_splits = {'N½': ['NWNW', 'NENW', 'SWNW', 'SENW', 'NWNE', 'NENE', 'SWNE', 'SENE'],
                  'S½': ['NWSW', 'NESW', 'SWSW', 'SESW', 'NWSE', 'NESE', 'SWSE', 'SESE'],
                  'E½': ['NWSE', 'NESE', 'SWSE', 'SESE', 'NWNE', 'NENE', 'SWNE', 'SENE'],
                  'W½': ['NWSW', 'NESW', 'SWSW', 'SESW', 'NWNW', 'NENW', 'SWNW', 'SENW'],
                  'NW¼': ['NWNW', 'NENW', 'SWNW', 'SENW'],
                  'NW': ['NWNW', 'NENW', 'SWNW', 'SENW'],
                  'NE¼': ['NWNE', 'NENE', 'SWNE', 'SENE'],
                  'NE': ['NWNE', 'NENE', 'SWNE', 'SENE'],
                  'SW¼': ['NWSW', 'NESW', 'SWSW', 'SESW'],
                  'SW': ['NWSW', 'NESW', 'SWSW', 'SESW'],
                  'SE¼': ['NWSE', 'NESE', 'SWSE', 'SESE'],
                  'SE': ['NWSE', 'NESE', 'SWSE', 'SESE'],
                  'NENW': ['NENW'],
                  'NENE': ['NENE'],
                  'NESE': ['NESE'],
                  'NESW': ['NESW'],
                  'NWNW': ['NWNW'],
                  'NWNE': ['NWNE'],
                  'NWSE': ['NWSE'],
                  'NWSW': ['NWSW'],
                  'SWNW': ['SWNW'],
                  'SENW': ['SENW'],
                  'SWSW': ['SWSW'],
                  'SENE': ['SENE'],
                  'SESE': ['SESE'],
                  'SWSE': ['SWSE'],
                  'SWNE': ['SWNE'],
                  'N½NE': ['NWNE', 'NENE'],
                  'N½SE¼': ['NWSE', 'NESE'],
                  'N½SE': ['NWSE', 'NESE'],
                  'N½SW¼': ['NWSW', 'NESW'],
                  'N½SW': ['NWSW', 'NESW'],
                  'N½NW': ['NENW', 'NWNW'],
                  'N½NW¼': ['NENW', 'NWNW'],
                  'NE¼SW¼': ['NESW'],
                  'NW¼SE¼': ['NWSE'],
                  'NE¼NE¼': ['NENE'],
                  'N½S½': ['NWSW', 'NESW', 'NWSE', 'NESE'],
                  'N½N½': ['NWNW', 'NENW', 'NWNE', 'NENE'],
                  'S½S½': ['SWSW', 'SESW', 'SWSE', 'SESE'],
                  'S½N½': ['SWNW', 'SENW', 'SWNE', 'SENE'],
                  'S½NE¼': ['SWNE', 'SENE'],
                  'S½NE': ['SWNE', 'SENE'],
                  'S½SW¼': ['SWSW', 'SESW'],
                  'S½SW': ['SWSW', 'SESW'],
                  'S½SE': ['SWSE', 'SESE'],
                  'S½NW': ['SWNW', 'SENW'],
                  'S½NW¼': ['SWNW', 'SENW'],
                  'SE¼NE¼': ['SENE'],
                  'SESW': ['SESW'],
                  'SW¼NW¼': ['SWNW'],
                  'SE¼SE¼': ['SESE'],
                  'SE¼NW¼': ['SENW'],
                  'SW¼SE¼': ['SWSE'],
                  'W½E½': ['NENW', 'SENW', 'NESW', 'SESW', ],
                  'W½W½': ['NWNW', 'SWNW', 'NWSW', 'SWSW'],
                  'W½SE': ['NWSE', 'SWSE'],
                  'W½SW': ['NWSW', 'SWSW'],
                  'W½NE': ['NWNE', 'SWNE'],
                  'W½NE¼': ['NWNE', 'SWNE'],
                  'W½NW': ['NWNW', 'SWNW'],
                  'E½SE': ['NESE', 'SESE'],
                  'E½NW': ['NENW', 'SENW'],
                  'E½NW¼': ['NENW', 'SENW'],
                  'E½W½': ['NENW', 'SENW', 'NESW', 'SESW'],
                  'E½E½': ['NENE', 'SENE', 'NESE', 'SESE'],
                  'E½NE': ['NENE', 'SENE'],
                  'E½NE¼': ['NENE', 'SENE'],
                  'E½SW': ['NESW', 'SESW'],
                  'E½SW¼': ['NESW', 'SESW']}

    # for returning a list of all relevant aliquots once combined in first half and second half
    aliquots = ali_splits[ali]

    for aliquot in aliquots:
      second_div_list.append(first_div_id + "A" + aliquot)

  return second_div_list


print("-" * 50)
parcel_csv = "Land Grab/Data Tables/UpdatedAZParcels.csv"
print("Opening csv file: {0}".format(parcel_csv))
parcel_df = pd.read_csv(parcel_csv)
print(parcel_df.head())

parcel_df = parcel_df.fillna("")
parcel_df = parcel_df[parcel_df["Survey_Type"] != "RSDL"]
parcel_df = parcel_df[parcel_df["Survey_Type"] != "FF"]

print("-" * 50)
print("Resulting dataframe had {0} rows.".format(len(parcel_df)))
print(parcel_df.head())

print("-" * 50)
print('')
print("-" * 50)
print("Creating dataframes for full sections and subdivisions of sections")

section_parcel_df = parcel_df[parcel_df['Aliquots'] == '']
subsection_parcel_df = parcel_df[parcel_df['Aliquots'] != '']

# attempt to ID all aliquots in the data set for ali_splits
# aliquots = subdivision_df.Aliquots.unique()
# print(aliquots)

print("The section dataframe has {0} rows. The subdivision dataframe has {1}".format(len(section_parcel_df),
                                                                                     len(subsection_parcel_df)))
print("-" * 50)
print('')
print("-" * 50)
print("Generating First Division IDs for both dataframes and Second Division IDS for subdivisions dataframe")
# get_first_div_id(state_abbrev, prime_meridian, twp_rng, sec)
section_parcel_df['First_Div_ID'] = section_parcel_df.apply(
  lambda row: get_first_div_id("AZ", "14", row['Twp_Rng'], row['Section']), axis=1)

# get_second_div_id(state_abbrev, prime_meridian, twp_rng, sec, ali, surv, surv_type)
subsection_parcel_df['First_Div_ID'] = subsection_parcel_df.apply(
  lambda row: get_first_div_id("AZ", "14", row['Twp_Rng'], row['Section']), axis=1)
subsection_parcel_df['Second_Div_ID'] = subsection_parcel_df.apply(
  lambda row: get_second_div_id("AZ", "14", row['Twp_Rng'], row['Section'], row['Aliquots'], row['Survey_Number'],
                                row['Survey_Type']), axis=1)
subsection_parcel_df = subsection_parcel_df.explode('Second_Div_ID', ignore_index=True)

org_len_section = len(section_parcel_df)
org_len_subsection = len(subsection_parcel_df)

section_parcel_df.drop_duplicates(subset=['First_Div_ID'], inplace=True)
subsection_parcel_df.drop_duplicates(subset=['Second_Div_ID'], inplace=True)

unq_len_section = len(section_parcel_df)
unq_len_subsection = len(subsection_parcel_df)

print("Section dataframe generated {0} unique values for {1} entries.".format(unq_len_section, org_len_section))
print(section_parcel_df.head())
print(
  "Subdivision dataframe generated {0} unique values for {1} entries.".format(unq_len_subsection, org_len_subsection))
print(subsection_parcel_df.head())
print("-" * 50)

print('')
print("-" * 50)

print("Exporting dataframes to csv.")

section_parcel_df.to_csv('Land Grab/section_parcels.csv')
subsection_parcel_df.to_csv('Land Grab/subsection_parcels.csv')
print("-" * 50)
