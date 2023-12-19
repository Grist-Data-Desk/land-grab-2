import logging
import os
import sys
import traceback
from collections import defaultdict
from datetime import datetime
from functools import partial
from pathlib import Path

import geopandas
import numpy as np
import pandas as pd

from land_grab_2.stl_dataset.step_1.constants import ACTIVITY, RIGHTS_TYPE, WGS_84
from land_grab_2.stl_dataset.step_2.land_activity_search.state_data_sources import STATE_ACTIVITIES, REWRITE_RULES
from land_grab_2.utilities.overlap import tree_based_proximity, geometric_deduplication
from land_grab_2.utilities.utils import GristCache, in_parallel, combine_delim_list

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)

# MEMORY = cast(Memory, None)
stl_comparison_base_dir = Path('')
CACHE_DIR = Path('')
STATE_OUT_COLS = ['object_id', 'state', 'university', 'Activity', 'Sub-activity', 'Use Purpose',
                  'Lessee or Owner or Manager', 'Lessee Name 2', 'Owner Address or Location', 'Lessor',
                  'Transaction Type', 'Lease Status', 'Lease Start Date', 'Lease End Date', 'Lease Extension Date',
                  'Commodity', 'Source', 'LandClass', 'Rights-Type']
DONT_USE_COLS = ['TypeGroup', 'Type', 'Status', 'DteGranted', 'DteExpires', 'Name', 'ALL_LESSEE']

GRIST_DATA_UPDATE = defaultdict(set)
ACTIVITY_DATA_UPDATE = []

AZ_KEY = {
    '0': 'Unleased Parcels',
    '1': 'Agriculture',
    '3': 'Commercial Lease',
    '5': 'Grazing Lease',
    '8': 'Prospecting Permit',
    '11': 'Mineral Permit',
    '66': 'US Govt Exclusive Use',
    '89': 'Institutional Use',
    '13': 'Oil and Gas Permit',
    '0.0': 'Unleased Parcels',
    '1.0': 'Agriculture',
    '3.0': 'Commercial Lease',
    '5.0': 'Grazing Lease',
    '8.0': 'Prospecting Permit',
    '11.0': 'Mineral Permit',
    '66.0': 'US Govt Exclusive Use',
    '89.0': 'Institutional Use',
    '13.0': 'Oil and Gas Permit',
}

MT_KEY = {
    'LSAG': 'Ag Lease',
    'LSGZ': 'Grazing Lease',
    'LSAGGZ': 'Ag & Grazing Lease',
    'LSAGCB': 'Ag Competitive Bid',
    'LSGZCB': 'Grazing Competitive Bid',
    'LSAGGC': 'Ag & Grazing Competitive Bid',
    'LUL': 'Land Use License',
    'FGL': 'Forest Grazing License',
    'FAL': 'Forest Ag License',
    'FAGL': 'Forest Grazing & Ag License',
    'FGLCB': 'Forest Grazing Competitive Bid',
    'FALCB': 'Forest Ag Competitive Bid',
    'FAGLCB': 'Forest Grazing & Ag Competitive Bid',
}

WA_KEY = {
    '10': 'Grazing Lease',
    '11': 'Permit Range',
    '12': 'Agricultural Lease',
    '32': 'Upland Material Purchase',
    '39': 'Commercial Lease',
    '50': 'Easement/Permit Granted by DNR',
    '52': 'Communications Site Lease',
    '55': 'Easement/Permit Acquired by DNR',
    '59': 'Recreation Sites',
    '60': 'Special Use Permits and Land Use Licenses',
    '64': 'Mining Contract',
    '65': 'Mineral Lease',
    '78': 'Water Rights',
    'T3': 'Land Trespass',
}

WI_KEY = {
    '1111': 'Open to public access',
    '1211': 'Open to passive use, hunting, trapping',
    '1121': 'Open to passive use, fishing, trapping',
    '1112': 'Open to passive use, hunting, fishing',
    '1122': 'Open to passive use and fishing',
    '1222': 'Open to passive use only',
    '2111': 'Open to hunting, fishing, trapping',
    '2211': 'Open to hunting and trapping',
    '2122': 'Open to fishing only',
    '2212': 'Open to hunting only',
}

MISC_KEY = {
    'Prospecting Permit': 'subsurface',
    'Mineral Permit': 'subsurface',
    'Oil and Gas Permit': 'subsurface',
    'Mining Contract': 'subsurface',
    'Mineral Lease': 'subsurface',
    'Oil and Gas': 'subsurface',
    'Geologic Carbon Storage': 'subsurface',
    'RE - Geothermal': 'subsurface',
    'Solid Mineral': 'subsurface',
    'Exploration Permit': 'subsurface',
    'Riverbed Exploration Location': 'subsurface',
    'Submerged Land Lease': 'subsurface',
    'Geothermal': 'subsurface',
    'Oil & Gas': 'subsurface',
    'Mineral Lease': 'subsurface',
    'Exploration Location': 'subsurface',
    '345 KV ELECTRIC LINE': 'subsurface',
    '8" NATURAL GAS': 'subsurface',
    '12" WATER LINE 2040': 'subsurface',
    '20" CRUDE OIL PIPELINE': 'subsurface',
    '4 1/2" PIPELINE & METER SITE': 'subsurface',
    '12" CRUDE OIL PIPELINE': 'subsurface',
    '12" NATURAL GAS PIPELINE RELOCATION': 'subsurface',
    '16" PIPELINE': 'subsurface',
    '3" OIL AND GAS PIPELINE': 'subsurface',
    '12" PRODUCED SALT WATER PIPELINE': 'subsurface',
    '6" & 2 - 1" NATURAL GAS PIPELINES': 'subsurface',
    '2 - 6" GAS HYDROCARBONS PIPELINES': 'subsurface',
    '18" HYDROCARBONS PIPELINE': 'subsurface',
    '12" CRUDE OIL AND/OR NATURAL GAS LIQUIDS PIPELINE': 'subsurface',
    '345 KV ELECTRIC TRANSMISSION LINE': 'subsurface',
    '1.7" UNDERGROUND 34.5 KV ELECTRIC COLLECTION LINE & DATA FIBER OPTICS - WIND': 'subsurface',
    '36" RAW WATER LINE': 'subsurface',
    '24" CRUDE OIL PIPELINE': 'subsurface',
    '10" NATURAL GAS PIPELINE': 'subsurface',
    'FIBER OPTIC LINE': 'subsurface',
    '2 7/8" NATURAL GAS PIPELINE': 'subsurface',
    'UNDERGROUND WATER, ELECTRIC & TELEPHONE LINES': 'subsurface',
    '12" SEWER LINE': 'subsurface',
    '3" PIPELINE': 'subsurface',
    '2 SEWER LINES': 'subsurface',
    '345 KV ELECTRIC TRANSMISSON LINE': 'subsurface',
    '12" NATURAL GAS PIPELINE': 'subsurface',
    '16" CRUDE OIL PIPELINE': 'subsurface',
    '7.2 KV UNDERGROUND ELECTRIC LINE': 'subsurface',
    '2" CONDUIT BURIED ELECTRIC LINE': 'subsurface',
    '4" CRUDE OIL PIPELINE': 'subsurface',
    '6" FRESH & SALT WATER PIPELINE': 'subsurface',
    'UNDERGROUND ELECTRIC LINE - WIND': 'subsurface',
    '3" POLY NATURAL GAS PIPELINE': 'subsurface',
    '345 KV ELECTRIC TRANSMISSION LINE - WIND': 'subsurface',
    '4" NATURAL GAS PIPELINE': 'subsurface',
    'Pipeline-Natural Gas ; Pipeline-Sewage ; Pipeline-Water': 'subsurface',
    'Pipeline-Brine Disposal ; Pipeline-Inactive': 'subsurface',
    'Jetty ; Pipeline-LPG': 'subsurface',
    'Pipeline-Subsurface Easement': 'subsurface',
    'Pipeline-Gas Lift': 'subsurface',
    'Pipeline-Brine Disposal ; Pipeline-Other': 'subsurface',
    'Communication Line ; Pipeline-Other': 'subsurface',
    'Pipeline-Petroleum Products ; Riprap': 'subsurface',
    'Fiber Optic Cable ; Pipeline-Natural Gas ; Pipeline-Other': 'subsurface',
    'General Easement ; Pipeline-Natural Gas ; Roadway': 'subsurface',
    'Cathodic Protection Unit ; Pipeline-Oil/Natural Gas/Condensate': 'subsurface',
    'Pipeline-Atmospheric Gas ; Pipeline-Hazardous Material (\'enes) ; Pipeline-LPG': 'subsurface',
    'Pipeline-Atmospheric Gas ; Pipeline-Natural Gas ; Pipeline-Oil ; Pipeline-Water': 'subsurface',
    'Electric Line ; Pipeline-Atmospheric Gas ; Pipeline-Other ; Pipeline-Water': 'subsurface',
    'Fiber Optic Cable ; Pipeline-Hazardous Material (\'enes) ; Pipeline-Other': 'subsurface',
    'Communication Line ; Electric Line ; Pipeline-Natural Gas ; Pipeline-Water ; Roadway ; Utility (Publ': 'subsurface',
    'Pipeline-Inactive ; Pipeline-Natural Gas': 'subsurface',
    'Pipeline-Oil/Natural Gas/Condensate ; Roadway ; Surface Site': 'subsurface',
    'Meter Site ; Pipeline-Natural Gas': 'subsurface',
    'Pipeline-Hazardous Material ; Pipeline-Petroleum Products': 'subsurface',
    'Pipeline-LPG ; Pipeline-Petroleum Products': 'subsurface',
    'Communication Line ; Pipeline-Atmospheric Gas ; Pipeline-Brine Disposal ; Pipeline-Hazardous Materia': 'subsurface',
    'Pipeline-Oil ; Pipeline-Other': 'subsurface',
    'Pipeline-Other ; Pipeline-Water': 'subsurface',
    'Fiber Optic Cable ; Pipeline-Inactive': 'subsurface',
    'Pipeline-Oil ; Pipeline-Petroleum Products': 'subsurface',
    'Pipeline-Brine Disposal ; Pipeline-Water': 'subsurface',
    'Pipeline-Water': 'subsurface',
    'Pipeline-Atmospheric Gas ; Pipeline-Water ; Water Intake': 'subsurface',
    'Pipeline-Natural Gas ; Pipeline-Oil/Natural Gas/Condensate': 'subsurface',
    'Pipeline-Brine Disposal ; Pipeline-Natural Gas': 'subsurface',
    'Fiber Optic Cable ; Pipeline-Natural Gas': 'subsurface',
    'Pipeline-Natural Gas ; Roadway': 'subsurface',
    'Pipeline-Oil': 'subsurface',
    'Pipeline-Oil ; Pipeline-Water': 'subsurface',
    'Pipeline-Other': 'subsurface',
    'Pipeline-Natural Gas ; Pump Station': 'subsurface',
    'Electric Line ; Pipeline-Oil/Natural Gas/Condensate': 'subsurface',
    'Pipeline-LPG': 'subsurface',
    'Pipeline-Hazardous Material (\'enes) ; Pipeline-Natural Gas': 'subsurface',
    'Pipeline-Hazardous Material (\'enes)': 'subsurface',
    'Pipeline-Water ; Roadway': 'subsurface',
    'Electric Line ; Pipeline-Water ; Water Intake': 'subsurface',
    'Electric Line ; Pipeline-Other': 'subsurface',
    'Brine Disposal': 'subsurface',
    'Pipeline-Water ; Water Intake': 'subsurface',
    'Pipeline-Oil/Natural Gas/Condensate ; Pipeline-Petroleum Products': 'subsurface',
    'Electric Line ; Pipeline-Natural Gas ; Pipeline-Water': 'subsurface',
    'Fiber Optic Cable ; Pipeline-Natural Gas ; Pipeline-Water': 'subsurface',
    'Pipeline-Gasoline': 'subsurface',
    'Pipeline-Natural Gas ; Surface Site': 'subsurface',
    'General Easement ; Pipeline-Water ; Roadway': 'subsurface',
    'Fiber Optic Cable ; Pipeline-Subsurface Easement': 'subsurface',
    'Pipeline-Oil/Natural Gas/Condensate': 'subsurface',
    'Electric Line ; Pipeline-Water ; Roadway': 'subsurface',
    'Communication Line ; Pipeline-Inactive ; Pipeline-Petroleum Products': 'subsurface',
    'Electric Line ; Fiber Optic Cable ; Pipeline-Other': 'subsurface',
    'Bulkhead ; Pipeline-Natural Gas': 'subsurface',
    'Electric Line ; Fiber Optic Cable ; Pipeline-Natural Gas ; Pipeline-Other': 'subsurface',
    'Pipeline-Sewage ; Staging Area': 'subsurface',
    'Pipeline-Hazardous Material': 'subsurface',
    'Electric Line ; Pipeline-Water': 'subsurface',
    'Pipeline-Hazardous Material (\'enes) ; Pipeline-Other': 'subsurface',
    'Pipeline-Crude Oil': 'subsurface',
    'Electric Line ; Pipeline-Oil': 'subsurface',
    'Pipeline-Natural Gas ; Pipeline-Oil': 'subsurface',
    'Pipeline-Sewage': 'subsurface',
    'Pipeline-Natural Gas': 'subsurface',
    'Pipeline-Petroleum Products': 'subsurface',
    'Drill site Location for Oil and Gas Well': 'subsurface',
    'Water Supply Well, Pipeline and Access Road': 'subsurface',
    'Saltwater Disposal Well and Access Road': 'subsurface',
    'Nine Offset Well Pads, Facilities and Access Roads': 'subsurface',
    'Pressure Reducing Valve Building and Access Road': 'subsurface',
    'Two Offset Well Pads, Facilities and Access Roads': 'subsurface',
    'Methane and Helium Recovery Facility, one water disposal well, and one gas disposal wells, together with connecting pipelines and associated access roads': 'subsurface',
    'Three Offset Well Pads and Access Road': 'subsurface',
    'Off-set well pad access road': 'subsurface',
    'Four Off-Set Well Sites with Tank Batteries and Access Roads': 'subsurface',
    'Meter Station & Access Road': 'subsurface',
    'Equipment. Site for Madison Formation CO₂ Flood': 'subsurface',
    'Offset Gas Well Pad': 'subsurface',
    'Well pad and access road for three well bores. Includes tanks, heater treaters, telemetry equipment, flare stacks/lines, flow lines': 'subsurface',
    'Oil Handling Facilities': 'subsurface',
    'Water Injection Well and Facilities': 'subsurface',
    'Water Disposal Well and Access Road': 'subsurface',
    'Natural Gas Storage Operations': 'subsurface',
    'Pump Station, Electrical Substation, and Electrical Line': 'subsurface',
    'Truck Offloading Station for Crude Oil and Natural Gas': 'subsurface',
    'Production facilities including wells, tank battery facilities, storage buildings, two trailers - split estate': 'subsurface',
    'Disposal Well & Access Road': 'subsurface',
    'Disposal Well': 'subsurface',
    'Off-Set Well Pad, hydraulic stimulation pit, production pad and Access Road': 'subsurface',
    'Block Valve and Access Road': 'subsurface',
    'Offset Well and Access Road': 'subsurface',
    'Private Microwave Communication Site and Access Road': 'subsurface',
    'Tank Battery and Production Facility': 'subsurface',
    'Off-Set Well Pad and Facilities': 'subsurface',
    'Water Disposal Facility': 'subsurface',
    'Fire Department Substation and Access Road': 'subsurface',
    'Sweetwater Measuring Station': 'subsurface',
    'Water Well and Frac Pond': 'subsurface',
    'Off set well pad': 'subsurface',
    'Well and Tank Battery': 'subsurface',
    'Off-set well pad and access road': 'subsurface',
    'Off-set well and Access Road': 'subsurface',
    'Gas Metering Facility': 'subsurface',
    'Off-Set Well Pads and Access Roads': 'subsurface',
    'Water Disposal Pit and Access Road': 'subsurface',
    'Well and Tank Battery and Access Road': 'subsurface',
    'Off set well and access road': 'subsurface',
    'Natural Gas Pump Station': 'subsurface',
    'Water Disposal Well and Tank Battery': 'subsurface',
    'Offset Well Pad and Access Road': 'subsurface',
    'Water Injection Well': 'subsurface',
    'Off Set Well Pad and Access Road': 'subsurface',
    'Water Well, Pipeline and Access Road': 'subsurface',
    'Evaporation Pond and Associated Equipment, Equipment Storage Buildings and Access Road': 'subsurface',
    'Offset Well Pad, Facilities and Access Road': 'subsurface',
    'Water Treatment Plant and Pit': 'subsurface',
    'Offset Well Pad, and powerline': 'subsurface',
    'Off-set Well Pad and Access Road': 'subsurface',
    'Compressor Site, tank Battery and Access Road': 'subsurface',
    'Off-set Well pad and Access Road': 'subsurface',
    'Disposal Well and Oil Treatment Facility': 'subsurface',
    'Tank Battery and Access Road': 'subsurface',
    'Produced Water Re-Use Facility and Access Road': 'subsurface',
    'Land Farm for treatment of crude oil contaminated soils, tank bottoms and sludges': 'subsurface',
    'Off-set well pad, pipeline, and access road': 'subsurface',
    'Water Disposal Well and Facilities': 'subsurface',
    'Off-set Well Pad': 'subsurface',
    'Offset well pad and access road': 'subsurface',
    'Tank Battery, Offset Well Pad, Flow Lines and Access Roads': 'subsurface',
    'Centralized Production Facility, Outflow Water Pipeline and Access Road': 'subsurface',
    'Well Pad and Access Road': 'subsurface',
    'Oil and Gas Well Pad': 'subsurface',
    'Tank Battery Site and Access Road': 'subsurface',
    'Communication Site for Television Translator': 'subsurface',
    'Spring Development and Pipeline': 'subsurface',
    'Water Supply Well and Access Road for use in drilling on- and off-lease oil wells': 'subsurface',
    'Well Pad for Offset Gas Well': 'subsurface',
    'Off-set well pad': 'subsurface',
    'Pig receiver, Valve Appurtenance and Access Road': 'subsurface',
    'Storage Yard and Equipment Staging Area': 'subsurface',
    'Five (5) Off-Set Wells and Access Roads': 'subsurface',
    'Oil Handling Facility': 'subsurface',
    'Temporary Living Quarters and Access Road': 'subsurface',
    'Off-Set Well and Access Road': 'subsurface',
    'Off-Set Wells': 'subsurface',
    'Tank Battery Site and Access Road': 'subsurface',
    'Water Disposal Well, Associated Facilities and Communication Site': 'subsurface',
    'Pipeline receiver and launcher site': 'subsurface',
    'Field Office and Central Tank Battery': 'subsurface',
    'Off-Set Well Pad and Access Road': 'subsurface',
    'off-set well pad and access road': 'subsurface',
    'Cellular Telephone Communication Site and Access Road': 'subsurface',
    'Receiver and Meter Site and Access Road': 'subsurface',
    'Offset Well Pad and Microwave Communication Site': 'subsurface',
    'Evaporation Water Treatment Facility': 'subsurface',
    'Control Cabinet for Fiber Optic Lines': 'subsurface',
    'Off-Set Well and Facilities': 'subsurface',
}


def get_activity_column(activity, state):
    # which col in the rewrite rules is the one that becomes activity
    activity_rewrite_rules = REWRITE_RULES.get(state.lower()).get(activity.name.lower())
    if not activity_rewrite_rules:
        activity_rewrite_rules = REWRITE_RULES.get(state.lower()).get(activity.name)
        if not activity_rewrite_rules:
            return

    return [
        original_col
        for original_col, output_column, in activity_rewrite_rules.items()
        if output_column.lower() == 'activity'
    ]


def translate_state_activity_code(activity_name):
    if isinstance(activity_name, float):
        activity_name = int(activity_name)
    if isinstance(activity_name, int):
        activity_name = str(activity_name)    

    if activity_name in AZ_KEY:
        return AZ_KEY[activity_name]

    if activity_name in MT_KEY:
        return MT_KEY[activity_name]

    if activity_name in WI_KEY:
        return WI_KEY[activity_name]

    if activity_name in WA_KEY:
        return WA_KEY[activity_name]

    return activity_name

def aggregate_misc(activity_name):
    if activity_name in MISC_KEY:
        return MISC_KEY[activity_name]

    return activity_name


def get_activity_name(state, activity, activity_row):
    activity_name = None

    if activity.use_name_as_activity and activity.activity_name_appendage_col:
        col_val = activity_row[activity.activity_name_appendage_col]
        if col_val.values[0]:
            activity_name = col_val.values[0]

    if activity_name is None:
        possible_activity_cols = get_activity_column(activity, state)
        if possible_activity_cols is not None:
            for activity_col in possible_activity_cols:
                if activity_col and activity_col in activity_row.keys():
                    activity_name_row = activity_row[activity_col].tolist()
                    if activity_name_row is not None and isinstance(activity_name_row, list):
                        activity_name = str(activity_name_row[0])
                        if 'None' in activity_name:
                            activity_name = None
                            continue
                        break

    if activity_name and activity_name is not np.nan:
        activity_name = translate_state_activity_code(activity_name)

    return activity_name if activity_name else activity.name

def is_subsurface_activity(activity_name):
        return MISC_KEY.get(activity_name, 'surface') == 'subsurface'

def is_incompatible_activity(grist_row, activity, activity_name):
    
    restricted_rights_types_for_subsurface = ['subsurface']
    restricted_rights_types_for_surface = ['surface']

    if activity.is_misc:
        if is_subsurface_activity(activity_name):
            if grist_row[RIGHTS_TYPE] in restricted_rights_types_for_surface:
                return True
        else:
            if grist_row[RIGHTS_TYPE] in restricted_rights_types_for_subsurface:
                return True

    restricted_rights_types = ['subsurface']
    if grist_row[RIGHTS_TYPE] in restricted_rights_types and activity.is_restricted_activity:
        return True

    restricted_rights_types = ['surface']
    if grist_row[RIGHTS_TYPE] in restricted_rights_types and activity.is_restricted_subsurface_activity:
        return True

    return False


def exclude_inactive(state, activity_row):
    if 'MT' in state or 'ID' in state:
        status_col = next((c for c in activity_row.keys() if 'stat' in c), None)
        if status_col and activity_row[status_col] != 'Active':
            return True

    return False


def capture_matches(matches, state, activity):
    rewrite_list = {'OtherMin': 'Other Minerals', 'OilGas': 'Oil & Gas', 'OilAndGas': 'Oil & Gas'}
    total = 0

    does_contain = 0
    grist_data_update = defaultdict(set)
    activity_data_update = []
    for match_score, grist_idx, grist_row, activity_row, contains, _ in matches:
        activity_name = get_activity_name(state, activity, pd.DataFrame([activity_row]))

        if activity_name is None or 'None' in activity_name:
            # N.B. for debugging purposes only, otherwise essentially a no-op.
            activity_name = get_activity_name(state, activity, pd.DataFrame([activity_row]))

        if activity_name in rewrite_list:
            activity_name = rewrite_list[activity_name]

        total += 1
        if contains and not is_incompatible_activity(grist_row, activity, activity_name):
            does_contain += 1
            if exclude_inactive(state, activity_row):
                continue

            grist_data_update[grist_idx].add(activity_name)
            activity_data_update.append(activity_row)

    return grist_data_update, activity_data_update


def find_overlaps(state, activity, activity_data, grist_data):
    try:
        matches = tree_based_proximity(grist_data.to_dict(orient='records'), activity_data, grist_data.crs)
        grist_update_thus_far, activity_update_thus_far = capture_matches(matches, state, activity)
        return grist_update_thus_far, activity_update_thus_far
    except Exception as err:
        print(traceback.format_exc())
        print(f'failing on mysterious except in find_overlaps()')


def process_state_activity(stl_comparison_base_dir, grist_data, activity_state, activity_info, cache_dir, activity):
    GristCache('', cache_dir)  # DO NOT REMOVE unless willing to hunt & remove all transitive uses of GristCache
    if activity_info.scheduler:
        activity.scheduler = activity_info.scheduler

    if not activity_info.use_cache:
        activity.use_cache = activity_info.use_cache

    try:
        activity_data = activity.query_data(stl_comparison_base_dir)
        if activity_data is None or len(activity_data) == 0:
            log.error(f'NO ACTIVITY DATA FOR {activity_state} {activity.name}')
            return

        return find_overlaps(activity_state, activity, activity_data, grist_data)
    except Exception as err:
        print(traceback.format_exc())
        print(f'random err: {err}')


def match_all_activities(stl_comparison_base_dir, states_data=None, grist_data=None):
    log.info(f'processing states {states_data.keys()}')
    global GRIST_DATA_UPDATE, ACTIVITY_DATA_UPDATE, MEMORY

    # process_stated_cached = MEMORY.cache(process_state_activity)

    for activity_state, activity_info in states_data.items():

        print(f'state: {activity_state} activity: {activity_info.name}')
        if not activity_info:
            log.error(f'NO ACTIVITY CONFIG FOR {activity_state}')
            continue
        st = datetime.now()
        grist_results = in_parallel(activity_info.activities,
                                    partial(
                                        process_state_activity,
                                        stl_comparison_base_dir,
                                        grist_data,
                                        activity_state,
                                        activity_info,
                                        CACHE_DIR
                                    ),
                                    show_progress=True,
                                    # scheduler='synchronous',  # TODO debug only
                                    batched=False)
        print(f'activity_state {activity_state} took: {datetime.now() - st}')

        for r in grist_results:
            if r is not None and len(r) > 0:
                r, act = r
                ACTIVITY_DATA_UPDATE += act
                for k, v in r.items():
                    if any(i is None for i in v):
                        print(f'Activity is None for state: {activity_state}')
                        sys.exit(1)
                    GRIST_DATA_UPDATE[k].update(v)


def main(stl_comparison_base_dir, stl_path: Path, the_out_dir: Path):
    if not the_out_dir.exists():
        the_out_dir.mkdir(parents=True, exist_ok=True)

    log.info(f'reading {stl_path}')
    gdf = geopandas.read_file(str(stl_path))

    cols = gdf.columns.tolist()
    if ACTIVITY not in cols:
        rights_type_idx = cols.index(RIGHTS_TYPE)
        cols.insert(rights_type_idx + 1, ACTIVITY)

    match_all_activities(stl_comparison_base_dir, STATE_ACTIVITIES, gdf)
    for row_idx, activity_list in GRIST_DATA_UPDATE.items():
        new_vals = ','.join([x for x in activity_list if x is not None])
        existing = gdf.loc[row_idx, ACTIVITY] or ''
        gdf.loc[row_idx, ACTIVITY] = combine_delim_list(existing, new_vals, sep=',')

    # reorder cols
    gdf = gdf[cols]

    log.info(f'final grist_data row_count: {gdf.shape[0]}')
    gdf.to_csv(str(the_out_dir / 'stl_dataset_extra_activities.csv'), index=False)
    gdf.to_file(str(the_out_dir / 'stl_dataset_extra_activities.geojson'), driver='GeoJSON')

    # Additionally, create a version of the dataset in WGS84 for visualization.
    gdf_wgs84 = gdf.to_crs(WGS_84)
    gdf_wgs84.to_file(str(the_out_dir / 'stl_dataset_extra_activities_wgs84.geojson'), driver='GeoJSON')

    log.info(f'original grist_data row_count: {gdf.shape[0]}')

    # if ACTIVITY_DATA_UPDATE:
    #     activity_df = pd.DataFrame(ACTIVITY_DATA_UPDATE)
    #     date_cols = [col for col in activity_df.columns if 'datetime' in str(activity_df.dtypes[col])]
    #     for col in date_cols:
    #         activity_df[col] = activity_df[col].map(str)
    #     did_it_work = str(activity_df.dtypes[col])
    #     assert 1
    #
    #     activity_gdf = geopandas.GeoDataFrame(activity_df, geometry=activity_df.geometry)
    #     activity_gdf = geometric_deduplication(activity_gdf, gdf.crs)
    #
    #     activity_gdf.to_csv(str(the_out_dir / 'activity_match_deep_dive.csv'), index=False)
    #     activity_gdf.to_file(str(the_out_dir / 'activity_match_deep_dive.geojson'), driver='GeoJSON')
    #     log.info(f'activity_df row_count: {activity_df.shape[0]}')
    # else:
    #     print('No activity matches whatsoever. recommend investigation/debugging.')


def run():
    print('running stl_activity_match')
    required_envs = ['DATA', 'PYTHONHASHSEED']
    missing_envs = [env for env in required_envs if os.environ.get(env) is None]
    if any(missing_envs):
        raise Exception(f'RequiredEnvVar: The following ENV vars must be set. {missing_envs}')

    data_tld = os.environ.get('DATA')
    base_data_dir = Path(f'{data_tld}/stl_dataset/step_2').resolve()

    global CACHE_DIR, MEMORY
    CACHE_DIR = base_data_dir / 'input/cache'
    # MEMORY = Memory(CACHE_DIR, verbose=0)

    stl_comparison_base_dir = base_data_dir / 'input/stl_activity_layers'
    GristCache('', CACHE_DIR)  # DO NOT REMOVE unless willing to hunt & remove all transitive uses of GristCache

    step_1_data_directory = Path(f'{data_tld}/stl_dataset/step_1').resolve()
    stl = step_1_data_directory / 'output/merged/all-states.geojson'

    out_dir = base_data_dir / 'output'

    main(stl_comparison_base_dir, stl, out_dir)

    sys.exit(0)


if __name__ == '__main__':
    run()
