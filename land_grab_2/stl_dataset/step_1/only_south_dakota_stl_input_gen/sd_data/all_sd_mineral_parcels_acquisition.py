# This thing will be used to ultimately get spatial data for South Dakota state trust land parcels.
# First, we will import two files: SD Subsurface parcel IDs and SD Surface parcel IDs.
# The first two files are based on the raw data that the SD Public Lands office gave me, and have been adjusted
# in Excel. I have already identified the parcels associated with the trust we are interested in (A), and I have also
# reformatted the PLSS number format to be as close to the official state PLSS number database as possible.
# Surface and subsurface parcels do not include the first four characters or the 0 after the last digit of the SN number
# (it's a two digit number) and before the L or the A.
# The Subsurface parcels do not include directional characters or 0s as spaces. The Surface ones do.
# Then, we will adjust the fixed parcel ID numbers to be split into the QQ format.
# This is based on Cas' python file.
# Then, we will match those adjusted parcel ID numbers (again, which I adjusted from the data supplied by the SD public
# lands office) to the official state PLSS records (a server online).
# We we call the SECDIVID or FRSTDIVID ids from the state PLSS database (SDQQ), we will reformat the value to be like the
# surface and subsurface styles, so we can identify matches.
# We will troubleshoot if there are parcels without a match.
# Once the IDs are matched, we will pull the spatial data. Then we'll have SD state trust land parcel data.

import csv
import functools
import itertools
import json
import logging
import time
from copy import deepcopy
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, ProcessPoolExecutor

# List below is supplied by Cas (UofAZ); PLSS IDs are broken into quarter-quarter segments.
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
ALI_SPLITS = {'N½': ['NWNW', 'NENW', 'SWNW', 'SENW', 'NWNE', 'NENE', 'SWNE', 'SENE'],
              'S½': ['NWSW', 'NESW', 'SWSW', 'SESW', 'NWSE', 'NESE', 'SWSE', 'SESE'],
              'E½': ['NWSE', 'NESE', 'SWSE', 'SESE', 'NWNE', 'NENE', 'SWNE', 'SENE'],
              'W½': ['NWSW', 'NESW', 'SWSW', 'SESW', 'NWNW', 'NENW', 'SWNW', 'SENW'],
              'NW¼': ['NWNW', 'NENW', 'SWNW', 'SENW'], 'NW': ['NWNW', 'NENW', 'SWNW', 'SENW'],
              'NE¼': ['NWNE', 'NENE', 'SWNE', 'SENE'], 'NE': ['NWNE', 'NENE', 'SWNE', 'SENE'],
              'SW¼': ['NWSW', 'NESW', 'SWSW', 'SESW'], 'SW': ['NWSW', 'NESW', 'SWSW', 'SESW'],
              'SE¼': ['NWSE', 'NESE', 'SWSE', 'SESE'], 'SE': ['NWSE', 'NESE', 'SWSE', 'SESE'], 'NENW': ['NENW'],
              'NENE': ['NENE'], 'NESE': ['NESE'], 'NESW': ['NESW'], 'NWNW': ['NWNW'], 'NWNE': ['NWNE'],
              'NWSE': ['NWSE'], 'NWSW': ['NWSW'], 'SWNW': ['SWNW'], 'SENW': ['SENW'], 'SWSW': ['SWSW'],
              'SENE': ['SENE'], 'SESE': ['SESE'], 'SWSE': ['SWSE'], 'SWNE': ['SWNE'], 'N½NE': ['NWNE', 'NENE'],
              'N½SE¼': ['NWSE', 'NESE'], 'N½SE': ['NWSE', 'NESE'], 'N½SW¼': ['NWSW', 'NESW'],
              'N½SW': ['NWSW', 'NESW'], 'N½NW': ['NENW', 'NWNW'], 'N½NW¼': ['NENW', 'NWNW'], 'NE¼SW¼': ['NESW'],
              'NW¼SE¼': ['NWSE'], 'NE¼NE¼': ['NENE'], 'N½S½': ['NWSW', 'NESW', 'NWSE', 'NESE'],
              'N½N½': ['NWNW', 'NENW', 'NWNE', 'NENE'], 'S½S½': ['SWSW', 'SESW', 'SWSE', 'SESE'],
              'S½N½': ['SWNW', 'SENW', 'SWNE', 'SENE'], 'S½NE¼': ['SWNE', 'SENE'], 'S½NE': ['SWNE', 'SENE'],
              'S½SW¼': ['SWSW', 'SESW'], 'S½SW': ['SWSW', 'SESW'], 'S½SE': ['SWSE', 'SESE'],
              'S½NW': ['SWNW', 'SENW'], 'S½NW¼': ['SWNW', 'SENW'], 'SE¼NE¼': ['SENE'], 'SESW': ['SESW'],
              'SW¼NW¼': ['SWNW'], 'SE¼SE¼': ['SESE'], 'SE¼NW¼': ['SENW'], 'SW¼SE¼': ['SWSE'],
              'W½E½': ['NENW', 'SENW', 'NESW', 'SESW', ], 'W½W½': ['NWNW', 'SWNW', 'NWSW', 'SWSW'],
              'W½SE': ['NWSE', 'SWSE'], 'W½SW': ['NWSW', 'SWSW'], 'W½NE': ['NWNE', 'SWNE'],
              'W½NE¼': ['NWNE', 'SWNE'], 'W½NW': ['NWNW', 'SWNW'], 'E½SE': ['NESE', 'SESE'],
              'E½NW': ['NENW', 'SENW'], 'E½NW¼': ['NENW', 'SENW'], 'E½W½': ['NENW', 'SENW', 'NESW', 'SESW'],
              'E½E½': ['NENE', 'SENE', 'NESE', 'SESE'], 'E½NE': ['NENE', 'SENE'], 'E½NE¼': ['NENE', 'SENE'],
              'E½SW': ['NESW', 'SESW'], 'E½SW¼': ['NESW', 'SESW']}


def import_csv(loc):
    the_csv = pd.read_csv(loc)
    return the_csv


def _fix_sdstl_lists(row, plssnum_column_idx):
    item = row[plssnum_column_idx]
    if not 'A' in item:
        return [row]

    # Split Fixed PLSS Number into what comes after A (call it ali_variable) - this refers to a quarter-quarter section.
    before, after = item.split('A')

    # Look up ali_variable in ali_splits table
    corrected_items = ALI_SPLITS.get(after)
    if not corrected_items:
        return [row]

    # For corrected_item in the list of corrected items, we want to create a new row [new_row] where the value is
    # changed to before + A + corrected_item.
    # The new row is a copy of the row in all fields except for this change.
    corrected_rows = []
    for corrected_item in corrected_items:
        new_row = row.copy()
        new_row[plssnum_column_idx] = before + "A" + corrected_item
        corrected_rows.append(new_row)
    return corrected_rows


def fix_sdstl_lists(subsurface_list, plssnum_column_idx):
    plssnum_list = subsurface_list.values.tolist()
    correct_plssnums = list(itertools.chain.from_iterable([
        _fix_sdstl_lists(row, plssnum_column_idx) for row in plssnum_list
    ]))
    corrected_df = pd.DataFrame(data=correct_plssnums, columns=subsurface_list.columns)

    return corrected_df


# Here, we want to call on the SD PLSS quarter-quarter server.
@functools.lru_cache
def get_all_ids(retries=5):
    url_base = r'https://sdgis.sd.gov/arcgis1/rest/services/SD_All/Boundary_PLSS_QuarterQuarter/MapServer/0/query?'
    # url_base = r'https://arcgis.sd.gov/arcgis/rest/services/SD_All/Boundary_PLSS_QuarterQuarter/MapServer/0/query?'

    url_query = {'where': '1=1',
                 'objectIds': '',
                 'time': '',
                 'geometry': '',
                 'geometryType': 'esriGeometryEnvelope',
                 'inSR': '',
                 'spatialRel': 'esriSpatialRelIntersects',
                 'resultType': 'none',
                 'distance': 0.0,
                 'units': 'esriSRUnit_Meter',
                 'relationParam': '',
                 'returnGeodetic': 'false',
                 'outFields': '*',
                 'returnGeometry': 'true',
                 'returnCentroid': 'false',
                 'featureEncoding': 'esriDefault',
                 'multipatchOption': 'xyFootprint',
                 'maxAllowableOffset': '',
                 'geometryPrecision': '',
                 'outSR': '',
                 'defaultSR': '',
                 'datumTransformation': '',
                 'applyVCSProjection': 'false',
                 'returnIdsOnly': 'true',
                 'returnUniqueIdsOnly': 'false',
                 'returnCountOnly': 'false',
                 'returnExtentOnly': 'false',
                 'returnQueryGeometry': 'false',
                 'returnDistinctValues': 'false',
                 'cacheHint': 'false',
                 'orderByFields': '',
                 'groupByFieldsForStatistics': '',
                 'outStatistics': '',
                 'having': '',
                 'resultOffset': '',
                 'resultRecordCount': '',
                 'returnZ': 'false',
                 'returnM': 'false',
                 'returnExceededLimitFeatures': 'true',
                 'quantizationParameters': '',
                 'sqlFormat': 'none',
                 'f': 'json',
                 'token': ''
                 }

    # If there is a failure while calling the server for a row, we wait 5 seconds, then check again. Repeat 5 times.
    try:
        response = requests.get(url=url_base, params=url_query)
        data = response.json()
        return data
    except Exception as err:
        if retries > 0:
            time.sleep(5)
            return get_all_ids(retries=retries - 1)
        else:
            log.error(err)
            return None


@functools.lru_cache
def get_single_object(oid, retries=5):
    url_base = r'https://sdgis.sd.gov/arcgis1/rest/services/SD_All/Boundary_PLSS_QuarterQuarter/MapServer/0/query?'

    url_query = {'where': '1=1',
                 'objectIds': f'{oid}',
                 'time': '',
                 'geometry': '',
                 'geometryType': 'esriGeometryEnvelope',
                 'inSR': '',
                 'spatialRel': 'esriSpatialRelIntersects',
                 'resultType': 'none',
                 'distance': 0.0,
                 'units': 'esriSRUnit_Meter',
                 'relationParam': '',
                 'returnGeodetic': 'false',
                 'outFields': '*',
                 'returnGeometry': 'true',
                 'returnCentroid': 'false',
                 'featureEncoding': 'esriDefault',
                 'multipatchOption': 'xyFootprint',
                 'maxAllowableOffset': '',
                 'geometryPrecision': '',
                 'outSR': '',
                 'defaultSR': '',
                 'datumTransformation': '',
                 'applyVCSProjection': 'false',
                 'returnIdsOnly': 'false',
                 'returnUniqueIdsOnly': 'false',
                 'returnCountOnly': 'false',
                 'returnExtentOnly': 'false',
                 'returnQueryGeometry': 'false',
                 'returnDistinctValues': 'false',
                 'cacheHint': 'false',
                 'orderByFields': '',
                 'groupByFieldsForStatistics': '',
                 'outStatistics': '',
                 'having': '',
                 'resultOffset': '',
                 'resultRecordCount': '',
                 'returnZ': 'false',
                 'returnM': 'false',
                 'returnExceededLimitFeatures': 'true',
                 'quantizationParameters': '',
                 'sqlFormat': 'none',
                 'f': 'pjson',
                 'token': ''
                 }

    # Respose, call on the server; data is the info if response returns something.
    try:
        response = requests.get(url=url_base, params=url_query)
        data = response.json()
        return data
    except Exception as err:
        if retries > 0:
            time.sleep(5)
            return get_single_object(oid, retries=retries - 1)
        else:
            log.error(err)
            return None


# Call on the specific field that we want (second divider)
def extract_secdivid_data(raw_data):
    if not raw_data['features']:
        return None
    return raw_data['features'][0]['attributes']['SECDIVID']


# Remove the 0 that acts as a "space" between last SN digit and before the aliquot or lot character (A or L).
def remove_0beforeAorL(s):
    location = s.find("SN")
    if location != -1:
        return s[:location + 4] + s[location + 5:]
    return s


def reformat_secdivid(s, cut_list):
    # This function will take the secdivid field from the South Dakota QQ server and make the necessary changes
    for pattern_group in cut_list:
        for pattern in pattern_group:
            location = s.find(pattern)
            if location != -1:
                s = s[:location] + s[location + len(pattern):]
                break
    return s


def surface_sdqq_parceladjust(secdivid):
    # take out first four characters of the SECDIVID number (typically SD05)
    # take out the 0 before the A character
    # take out the 0 before the L character
    return remove_0beforeAorL(secdivid[4:])


def subsurface_sdqq_parceladjust(secdivid):
    # take out first four characters of the SECDIVID number (typically SD05) - why we start on the 5th character
    # replace 'OWO' and 'OE0' with "" (no character)
    # replace 'ON' and 'OS' with "" (no character)
    # take out the 0 before the A character
    # take out the 0 before the L character
    subsurfaceadjust1 = reformat_secdivid(secdivid[4:],
                                          [["0W0", "0E0"], ["0N", "0S"]], )
    subtest = remove_0beforeAorL(subsurfaceadjust1)
    return subtest


# For speed, use parallel_get to make it run faster and return matches as they appear.
# Does parallel function (getting details) and then doing the done function, which writes row to appropriate file and
# removes matching ID from all-adjustedstl list.
def parallel_get(oids, p_func, done_func):
    complete = 0
    with ThreadPoolExecutor(max_workers=50) as executor:
        for f in as_completed([executor.submit(p_func, oid) for oid in oids]):
            try:
                complete += 1
                print(f'fetch complete: {complete}', end='\r')
                done_func(f.result())
            except Exception as err:
                log.error(err)


def process_single_obj(done_csv_writer, all_adjustedstls, secdivid_data):
    if not secdivid_data:
        return

    # secdivid is a singular string; reformatted_secdivids are the list of all adjusted secdivids from the server
    # for a particular server object, extract just value of SECDIVID field, change it in two ways, then check if it exists in
    # surface and/or subsurface data.
    secdivid = extract_secdivid_data(secdivid_data)
    sub_reformatted_secdivids = subsurface_sdqq_parceladjust(secdivid)
    # surf_reformatted_secdivids = surface_sdqq_parceladjust(secdivid)

    geo = json.dumps(secdivid_data['features'][0]['geometry']['rings'][0])

    # Now we compare the list of reformatted secdivids called from the server
    secdivid_col = next((c for c in all_adjustedstls[0].keys() if c != 'Beneficiary'), None)
    match_row_raw = next(((i, r) for i, r in enumerate(all_adjustedstls)
                          if sub_reformatted_secdivids == r[secdivid_col]), None)
    if not match_row_raw:
        return

    match_index, match_row = match_row_raw
    log.info(f'writing done-row for original: {secdivid} '
             f'secdividsub_reformatted_secdivids: {sub_reformatted_secdivids}')
    secdivid_data['features'][0]['attributes']['geometry'] = geo
    row_for_writing = {**secdivid_data['features'][0]['attributes'], 'Beneficiary': match_row['Beneficiary']}
    done_csv_writer.writerow(row_for_writing)
    all_adjustedstls.pop(match_index)
    return


def match_adjusted_sdstllist_with_sdqq_server(adjusted_subsurface,
                                              adjustedsubsurface_column_name,
                                              starting_record=None):
    # We need to call on the SDQQ server
    # We will call on the SECDIVID column and reformat it in two ways - one to match subsurface and another to match
    # surface PLSS number format
    # Then we see if either of the reformatted numbers matches the corrected_item in the adjusted sdstl lists
    # If it matches, download. If not, pass.

    # This function gets all the OBJECTIDS and creates the output files and starts the parallel/concurrent hydration
    # surface = adjusted_surface[adjustedsurface_column_name].to_list()
    adjusted_subsurface_for_proc = deepcopy(adjusted_subsurface)

    print(f'original adjusted_subsurface size: {adjusted_subsurface_for_proc.shape[0]}')
    adjusted_subsurface_for_proc.drop_duplicates(subset=[adjustedsubsurface_column_name], inplace=True)
    print(f'dropped duplicates, adjusted_subsurface size: {adjusted_subsurface_for_proc.shape[0]}')

    adjusted_subsurface_for_proc = adjusted_subsurface_for_proc[[adjustedsubsurface_column_name, 'Beneficiary']]
    all_adjustedstls = adjusted_subsurface_for_proc.to_dict(orient='records')
    # subsurface = adjusted_subsurface[adjustedsubsurface_column_name].to_list()
    # all_adjustedstls = set(subsurface)

    log.info('fetch all objectids')
    objectids = get_all_ids()['objectIds']
    if starting_record:
        try:
            restart_obj_idx = objectids.index(starting_record)
            if restart_obj_idx != -1:
                objectids = objectids[restart_obj_idx:]
        except:
            pass
    sample_obj = get_single_object(objectids[0])
    fieldsname = list(sample_obj['features'][0]['attributes'].keys()) + ['geometry']

    fieldsname = fieldsname + ['Beneficiary']

    with open(Path('~/Desktop/done.csv').expanduser().resolve(), 'w') as done_csv_writer_fh:
        done_csv_writer = csv.DictWriter(done_csv_writer_fh, fieldnames=fieldsname)
        log.info('writing done-csv header')
        done_csv_writer.writeheader()

        process_single_obj_with_writer = functools.partial(process_single_obj,
                                                           done_csv_writer,
                                                           all_adjustedstls)

        log.info('beginning parallel-fetching oids')
        parallel_get(objectids, get_single_object, process_single_obj_with_writer)

    with open(Path('~/Desktop/unmatched.csv').expanduser().resolve(), 'w') as unmatched_csv_writer_fh:
        log.info('writing unmatched-csv header')
        unmatched_csv_writer = csv.DictWriter(unmatched_csv_writer_fh, fieldnames=['original_secdivid'])
        unmatched_csv_writer.writeheader()

        for row in all_adjustedstls:
            unmatched_csv_writer.writerow({k: v for k, v in row.items() if k != 'Beneficiary'})


def main():
    log.info('importing subsurface list')
    subsurface_list = import_csv('/Users/mpr/Desktop/QUERYTERMS.csv')

    log.info('fix_sdstl_lists subsurface ')
    adjusted_subsurface = fix_sdstl_lists(subsurface_list, 11)
    adjusted_subsurface.to_csv(r'/Users/mpr/Desktop/sd_subsurface.csv')

    log.info('match_adjusted_sdstllist_with_sdqq_server')
    match_adjusted_sdstllist_with_sdqq_server(
        adjusted_subsurface,
        'MATCH_TERM',
        starting_record=1)  # 152261 - first objID that matched # 368987)
    # 1131459 - last objID that matched
    log.info('done')


if __name__ == '__main__':
    main()
