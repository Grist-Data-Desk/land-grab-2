import enum
import json
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union, Any, Dict

import dask
import dask.bag
import geopandas
import numpy as np
import pandas as pd
import requests
from compose import compose
from dask.diagnostics import ProgressBar
from ratelimiter import RateLimiter
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

STL_COMPARISON_BASE_DIR = Path('.')
STATE_OUT_COLS = ['object_id', 'state', 'university', 'Activity', 'Sub-activity', 'Use Purpose',
                  'Lessee or Owner or Manager', 'Lessee Name 2', 'Owner Address or Location', 'Lessor',
                  'Transaction Type', 'Lease Status', 'Lease Start Date', 'Lease End Date', 'Lease Extension Date',
                  'Commodity', 'Source', 'LandClass', 'Rights-Type']
DONT_USE_COLS = ['TypeGroup', 'Type', 'Status', 'DteGranted', 'DteExpires', 'Name', 'ALL_LESSEE']


# TODO: check that PYTHONHASHSEED is set and disallow run otherwise
class GristCache:
    def __init__(self, location):
        self.location = location

    def cache_write(self, obj, name, file_ext='.json'):
        """
        this function requires the ENV var: PYTHONHASHSEED to be set to ensure stable hashing between runs
        """
        here = Path(f'./cache/{hash(self.location)}')
        if not here.exists():
            here.mkdir(exist_ok=True, parents=True)

        cached_file = here / f'{name}{file_ext}'

        log.info(f'writing to cache: {str(cached_file)}')
        if 'json' in file_ext:
            with cached_file.open('w') as fp:
                json.dump(obj, fp)

        try:
            if 'feather' in file_ext:
                obj.to_feather(str(cached_file))
        except Exception as err:
            log.error(f'CacheWriteError during feather WRITE path: {str(cached_file)} err: {err}')

    def cache_read(self, name, file_ext='.json'):
        """
        this function requires the ENV var: PYTHONHASHSEED to be set to ensure stable hashing between runs
        """
        here = Path(f'./cache/{hash(self.location)}')
        if not here.exists():
            here.mkdir(exist_ok=True, parents=True)

        cached_file = here / f'{name}{file_ext}'
        if not cached_file.exists():
            log.info(f'cache-miss for: {str(cached_file)}')
            return None

        log.info(f'reading from cache: {str(cached_file)}')
        if 'json' in file_ext:
            with cached_file.open('r') as fp:
                return json.load(fp)
        try:
            if 'feather' in file_ext:
                return geopandas.read_feather(str(cached_file))
        except Exception as err:
            log.error(f'CacheReadError during feather READ path: {str(cached_file)} err: {err}')


class StateActivityDataLocation(enum.Enum):
    LOCAL = 'local'
    REMOTE = 'remote'


def safe_geopandas_load(p):
    try:
        g = geopandas.read_file(p)
        if g is not None:
            return g
    except Exception as err:
        log.error(f'THIS IS WHERE THE ERROR IS {err}')


@dataclass
class StateActivityDataSource:
    name: str
    location: str
    use_name_as_activity: bool = False
    keep_cols: List[str] = field(default_factory=list)

    @property
    def loc_type(self) -> StateActivityDataLocation:
        return StateActivityDataLocation.REMOTE if 'http' in self.location else StateActivityDataLocation.LOCAL

    def load_local(self):
        loc_path = Path(self.location)
        if loc_path.name.endswith('.shp'):
            if loc_path.name.startswith('/'):
                shapefile = self.location
                gdf = geopandas.read_file(str(shapefile))
            else:
                shapefile = STL_COMPARISON_BASE_DIR / self.location
                gdf = geopandas.read_file(str(shapefile))
        else:
            shapefile = next(
                (f for f in (STL_COMPARISON_BASE_DIR / self.location).iterdir() if f.name.endswith('.shp')), None)
            gdf = geopandas.read_file(str(shapefile))

        return gdf

    def load_remote(self):
        cache = GristCache(self.location)
        activity_data_geopandas = cache.cache_read('activity_data_geopandas', '.feather')
        if activity_data_geopandas is not None:
            return activity_data_geopandas

        cached_ids_resp = cache.cache_read('ids_resp')
        ids_resp = cached_ids_resp or self.fetch_all_parcel_ids()
        if not cached_ids_resp:
            cache.cache_write(ids_resp, 'ids_resp')

        if ids_resp:
            ids = ids_resp.get('objectIds', [])
            log.info(f'fetching remote activity data for {self.name} from: {self.location}')
            cached_activity_data = cache.cache_read('activity_data')
            activity_data = cached_activity_data or in_parallel(ids,
                                                                self.fetch_remote,
                                                                batched=False,
                                                                scheduler='threads')
            if not cached_activity_data:
                cache.cache_write(activity_data, 'activity_data')

            log.info(f'hydrating geodataframes activity data for {self.name} from: {self.location}')
            activity_data = in_parallel(activity_data,
                                        safe_geopandas_load,
                                        batched=False,
                                        scheduler='threads')

            if activity_data:
                try:
                    log.info(f'concat-ing geodataframes activity data for {self.name} from: {self.location}')
                    activity_data = geopandas.GeoDataFrame(pd.concat(activity_data, ignore_index=True),
                                                           crs=activity_data[0].crs)
                    cache.cache_write(activity_data, 'activity_data_geopandas', '.feather')

                    return activity_data
                except Exception as err:
                    log.error(f'Failed with {err} initing geodf for {self.name} from: {self.location}')
                    print(f'Failed with {err} initing geodf for {self.name} from: {self.location}')
                    return

    def query_data(self) -> Optional[Union[geopandas.GeoDataFrame, List[geopandas.GeoDataFrame]]]:
        if not self.location:
            return

        if self.loc_type == StateActivityDataLocation.LOCAL:
            activity_data = self.load_local()
            return activity_data

        if self.loc_type == StateActivityDataLocation.REMOTE:
            activity_data = self.load_remote()
            return activity_data

    @RateLimiter(max_calls=5000, period=60)
    def fetch_remote(self, parcel_id: Optional[str] = None, retries=10, response_type='text'):
        """
        response_type: str - either `json` or `text`
        """
        url_base = f'{self.location}?'

        url_query = {'where': '1=1',
                     'objectIds': f'{parcel_id}',
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
            if response_type == 'json':
                data = response.json()
            else:
                data = response.text
            return data
        except Exception as err:
            if retries > 0:
                time.sleep(5)
                return self.fetch_remote(parcel_id=parcel_id, retries=retries - 1, response_type=response_type)
            else:
                log.error(err)
                return None

    # Here, we want to call on the SD PLSS quarter-quarter server.
    def fetch_all_parcel_ids(self, retries=10):
        url_base = f'{self.location}?'

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
                return self.fetch_all_parcel_ids(retries=retries - 1)
            else:
                log.error(err)
                return None


@dataclass
class StateForActivity:
    name: str
    activities: List[StateActivityDataSource]


state_activities = {
    'AZ': StateForActivity(name='arizona', activities=[
        StateActivityDataSource(name='misc',
                                location='http://gis.azland.gov/arcgis/rest/services/StateTrust/SurfaceParcels/MapServer/0/query',
                                keep_cols=['leased', 'ke', 'effdate', 'expdate', 'full_name'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Minerals',
                                location='http://gis.azland.gov/arcgis/rest/services/StateTrust/MineralParcels/MapServer/0/query',
                                keep_cols=['leased', 'ke', 'effdate', 'expdate', 'full_name'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas',
                                location='http://gis.azland.gov/arcgis/rest/services/StateTrust/OilGasParcels/MapServer/0/query',
                                keep_cols=['type', 'leased', 'effdate',
                                           'expdate',
                                           'full_name'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Agriculture',
                                location='http://gis.azland.gov/arcgis/rest/services/StateTrust/GrazingAllotments/MapServer/0/query',
                                keep_cols=['name'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Solar',
                                location='http://gis.azland.gov/arcgis/rest/services/Renewable/SolarProjects/MapServer/0/query',
                                keep_cols=['technology', 'projectnam', 'status'],
                                use_name_as_activity=True),
    ]),
    'CO': StateForActivity(name='colorado', activities=[
        StateActivityDataSource(name='misc',
                                location='https://services5.arcgis.com/rqsYvPKZmvSrSWbw/ArcGIS/rest/services/Leases_ALL_USE/FeatureServer/query',
                                keep_cols=['Transaction Type', 'Lease Type', 'Lease Subtype', 'Lessee Name',
                                           'Lease State Date',
                                           'Lease End Date', 'Lease Status'],
                                use_name_as_activity=False)

    ]),
    'ID': StateForActivity(name='idaho', activities=[
        StateActivityDataSource(name='misc',
                                location='http://gis1.idl.idaho.gov/arcgis/rest/services/Portal/Landfolio_Data_Layers/MapServer/4/query',
                                keep_cols=['TypeGroup', 'Type', 'Status', 'DteGranted', 'DteExpires', 'Name',
                                           'Commodities'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='roads',
                                location='http://gis1.idl.idaho.gov/arcgis/rest/services/Portal/Landfolio_Data_Layers/MapServer/6/query',
                                keep_cols=['TypeGroup', 'Status', 'DteGranted', 'DteExpires', 'Parties',
                                           'Easement Right', 'EasementPurpose'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Water',
                                location='http://gis1.idl.idaho.gov/arcgis/rest/services/Portal/Landfolio_Data_Layers/MapServer/5/query',
                                keep_cols=['TypeGroup', 'Status', 'WaterUse', 'Source'],
                                use_name_as_activity=True),

    ]),
    'MN': StateForActivity(name='minnesota', activities=[
        StateActivityDataSource(name='Peat',
                                location='Minnesota_All/shp_plan_state_peatleases',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Recreation',
                                location='Minnesota_All/shp_bdry_dnr_managed_areas/dnr_stat_plan_areas.shp',
                                keep_cols=['AREA_NAME', 'AREA_TYPE'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation-DNR Managed',
                                location='Minnesota_All/shp_bdry_dnr_managed_areas/dnr_management_units.shp',
                                keep_cols=['UNIT_NAME', 'UNIT_TYPE', 'ADMINISTRA'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Aggregate Minerals',
                                location='Minnesota_All/shp_geos_aggregate_mapping',
                                keep_cols=['Type', 'Status_1', 'Status_2'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active Minerals',
                                location='Minnesota_All/shp_plan_state_minleases/active_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic Mineral Leases',
                                location='Minnesota_All/shp_plan_state_minleases/historic_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                use_name_as_activity=True)

    ]),
    'ND': StateForActivity(name='north dakota', activities=[
        StateActivityDataSource(name='Minerals',
                                location='https://ndgishub.nd.gov/arcgis/rest/services/All_GovtLands_State/MapServer/2/query',
                                keep_cols=['LEASE_STATUS', 'LEASE_EFFECTIVE', 'LEASE_EXPIRATION', 'LEASE_EXTENDED',
                                           'LESSEE'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation',
                                location='https://ndgishub.nd.gov/arcgis/rest/services/All_GovtLands_State/MapServer/4/query',
                                keep_cols=['UNIT_NAME'],
                                use_name_as_activity=True),

    ]),
    'NE': StateForActivity(name='nebraska', activities=[
        StateActivityDataSource(name='Water',
                                location='Nebraska_All/LOC_SurfaceWaterRightsDiversionsExternal_DNR.shp',
                                keep_cols=['RightStatu', 'RightUse', 'FirstName', 'LastName'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation',
                                location='Nebraska_All/Park_Areas.shp',
                                keep_cols=['AreaName', 'StartDate', 'Status'],
                                use_name_as_activity=True),

    ]),
    'NM': StateForActivity(name='new mexico', activities=[
        StateActivityDataSource(name='Agriculture',
                                location='NewMexico_All/Ag_Leases',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM']),
        StateActivityDataSource(name='Commercial Leases',
                                location='NewMexico_All/Commercial_Leases',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM', 'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Energy',
                                location='NewMexico_All/Energy_Leases',
                                use_name_as_activity=False,
                                keep_cols=['STATUS', 'LEASE_TYPE',
                                           'OGRID_NAM']),
        StateActivityDataSource(name='Minerals',
                                location='NewMexico_All/Mineral_Leases',
                                use_name_as_activity=False,
                                keep_cols=['STATUS', 'LEASE_TYPE', 'OGRID_NAM', 'SUB_TYPE',
                                           'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Oil and gas',
                                location='NewMexico_All/OilGas_Leases',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'VEREFF_DTE', 'VERTRM_DTE', 'OGRID_NAM']),
        StateActivityDataSource(name='Roads',
                                location='NewMexico_All/slo_rwleased',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM']),

    ]),
    'OK': StateForActivity(name='oklahoma', activities=[
        StateActivityDataSource(name='misc',
                                location='https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/21/query',
                                keep_cols=['Purpose', 'Grantee',
                                           'EasementType'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Minerals',
                                location='https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/1/query',
                                keep_cols=['BeginDate', 'EndDate', 'OwnerName', 'Address2'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Agriculture',
                                location='https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/0/query',
                                keep_cols=['LeaseType', 'BeginDate', 'EndDate', 'OwnerName',
                                           'Address2'],
                                use_name_as_activity=False),

    ]),
    'SD': StateForActivity(name='south dakota', activities=[
        StateActivityDataSource(name='Recreation',
                                location='SouthDakota_All',
                                keep_cols=['ParkName'],
                                use_name_as_activity=True),

    ]),
    'TX': StateForActivity(name='texas', activities=[
        StateActivityDataSource(name='Coastal',
                                location='Texas_All/NonMineralPoly',
                                keep_cols=['PROJECT_NA', 'GRANTEE', 'ACTIVITY_T'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='misc',
                                location='Texas_All/ME',
                                keep_cols=['LEASE_STAT', 'PRIMARY_LE',
                                           'ALL_LESSEE', 'Purpose'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Hard Minerals',
                                location='Texas_All/HardMinerals',
                                keep_cols=['LEASE_STAT', 'ORIGINAL_L', 'EFFECTIVE_'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Texas_All/ActiveLeases',
                                keep_cols=['LEASE_STAT', 'EFFECTIVE_', 'ORIGINAL_L', 'LESSOR'],
                                use_name_as_activity=True),

    ]),
    'UT': StateForActivity(name='utah', activities=[
        StateActivityDataSource(name='Water',
                                location='Utah_All/Utah_Water_Related_Land_Use',
                                keep_cols=['Descriptio',
                                           'LU_Group'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Geothermal',
                                location='Utah_All/Utah_UREZ_Phase_2_Geothermal',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Wind Zones',
                                location='Utah_All/Utah_UREZ_Phase_1_Wind_Zones',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Solar Zones',
                                location='Utah_All/Utah_UREZ_Phase_1_Solar_Zones',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation',
                                location='Utah_All/Utah_Parks_Local',
                                keep_cols=['NAME', 'TYPE', 'STATUS'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas wells',
                                location='Utah_All/Utah_Oil_and_Gas_Well_Locations',
                                keep_cols=['Operator'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas fields',
                                location='Utah_All/Utah_Oil_and_Gas_Fields-shp',
                                keep_cols=['STATUS'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Grazing',
                                location='Utah_All/Utah_Grazing_Allotments',
                                keep_cols=['Manager', 'AllotName'],
                                use_name_as_activity=True)

    ]),
    'WA': StateForActivity(name='washington', activities=[
        StateActivityDataSource(name='Agriculture',
                                location='https://fortress.wa.gov/agr/gis/wsdagis/rest/services/NRAS/SectionsWithCrops2022/MapServer/0/query',
                                keep_cols=['CropType', 'CropGroup'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Non-Metallic Minerals',
                                location='Washington_All',
                                keep_cols=['MINERAL'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Metallic Minerals',
                                location='Washington_All',
                                keep_cols=['COMMODITIE', 'PRODUCTION', 'ORE_MINERA'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Mining',
                                location='Washington_All',
                                keep_cols=['APPLICANT_', 'MINE_NAME', 'COMMODITY_'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Washington_All',
                                keep_cols=['COMPANY_NA', 'WELL_STATU'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Coal',
                                location='Washington_All',
                                keep_cols=[],
                                use_name_as_activity=True),

    ]),
    'WI': StateForActivity(name='wisconsin', activities=[
        StateActivityDataSource(name='misc',
                                location='https://dnrmaps.wi.gov/arcgis/rest/services/LF_DML/LF_DNR_PARCEL_DETAIL_WTM_Ext/MapServer/2/query',
                                keep_cols=['PROP_NAME'],
                                use_name_as_activity=False),

    ]),
    'WY': StateForActivity(name='wyoming', activities=[
        StateActivityDataSource(name='Metallic and Nonmetallic Minerals',
                                location='https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/14/query',
                                keep_cols=['MetallicNonMetallicLeaseSubType',
                                           'LeaseIssueDate',
                                           'LeaseExpirationDate', 'CompanyName', 'LeaseStatusLabel', 'CompanyZipCode',
                                           'MineralTypeLabel'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas',
                                location='https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/12/query',
                                keep_cols=['LeaseIssueDate',
                                           'LeaseExpirationDate', 'CompanyName', 'LeaseStatusLabel', 'CompanyZipCode',
                                           'MineralTypeLabel'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Easements',
                                location='https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/7/query',
                                keep_cols=['Leaseholder_LU', 'Issue_Date_LU', 'Expiration_Date_LU', 'Status_LU',
                                           'Sub_Group_LU',
                                           'Use_Type_LU'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Grazing',
                                location='https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/10/query',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Special',
                                location='https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/8/query',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU',
                                           'Type_LU', 'Purpose_LU'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Wind',
                                location='https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/9/query',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU'],
                                use_name_as_activity=True)
    ]),

    'MT': StateForActivity(name='Montana', activities=[
        StateActivityDataSource(name='Oil and gas',
                                location='https://services2.arcgis.com/DRQySz3VhPgOv7Bo/ArcGIS/rest/services/MMB_Oil_and_Gas/FeatureServer/1/query',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='misc',
                                location='https://gisservicemt.gov/arcgis/rest/services/MSDI_Framework/ManagedAreas/MapServer/0/query',
                                keep_cols=['MANAME', 'INST', 'UNITTYPE'],
                                use_name_as_activity=False),

    ])
}


def in_parallel(work_items, a_callable, scheduler='processes', postprocess=None, batched=True):
    if postprocess:
        a_callable = compose(postprocess, a_callable)

    all_results = []
    if not batched:
        with dask.config.set(scheduler=scheduler):
            with ProgressBar():
                all_results = dask.bag.from_sequence(work_items).map(a_callable).compute()
                return all_results

    batch_size = 100
    batches = [work_items[i:i + batch_size] for i in range(0, len(work_items), batch_size)]

    for batch in tqdm(batches):
        with dask.config.set(scheduler=scheduler):
            with ProgressBar():
                results = dask.bag.from_sequence(batch, partition_size=batch_size // 4).map(a_callable).compute()
                all_results += results
    return all_results


@dataclass
class GristOverlapMatch:
    grist_rows: Any
    activity_row: Any

    @staticmethod
    def extract_matches(activity_data, grist_data, overlap_report) -> List['GristOverlapMatch']:
        matches = []
        for name, group in overlap_report.groupby("joinidx_0")[["joinidx_1"]]:
            grist_row_idxs = group['joinidx_1'].tolist()
            grist_rows = grist_data[grist_data['joinidx_1'].isin(grist_row_idxs)]
            grist_rows.drop('joinidx_1', inplace=True, axis=1)

            intersecting_activity = activity_data[activity_data['joinidx_0'] == name]
            intersecting_activity.drop('joinidx_0', inplace=True, axis=1)

            matches.append(GristOverlapMatch(grist_rows=grist_rows, activity_row=intersecting_activity))

        return matches


def find_overlaps(activity_data, grist_data):
    try:
        activity_data["joinidx_0"] = np.arange(0, activity_data.shape[0]).astype(int)
        grist_data["joinidx_1"] = np.arange(0, grist_data.shape[0]).astype(int).astype(str)

        activity_data_cmp = activity_data.to_crs(grist_data.crs)
        overlapping_regions = geopandas.sjoin(activity_data_cmp[['joinidx_0', 'geometry']],
                                              grist_data[['joinidx_1', 'geometry']],
                                              how="left",
                                              op='intersects').dropna()

        if overlapping_regions.shape[0] > 0:
            return GristOverlapMatch.extract_matches(activity_data, grist_data, overlapping_regions)
    except Exception as err:
        print(f'BIG SCARY {err}')


def single_activity_match(state=None, grist_data=None, activity=None):
    activity_data = activity.query_data()
    if activity_data is None or len(activity_data) == 0:
        log.error(f'NO ACTIVITY DATA FOR {state}')
        return

    matches = find_overlaps(activity_data, grist_data)

    if matches:
        log.info(f'found {len(matches)} matches for state: {state} for activity: {activity.name}')
        return matches
    else:
        log.info(f'found NO matches for state: {state} for activity: {activity.name}')


def maybe_rename_column(col, activity_state=None, column_rename_rules=None, activity=None):
    state = activity_state.lower()
    name = activity.name.lower()
    if state in column_rename_rules and name in column_rename_rules[state] and col in column_rename_rules[state][name]:
        return column_rename_rules[state][name][col]
    return col


def capture_state_data(activity_state: str,
                       activity: StateActivityDataSource,
                       matches: List[GristOverlapMatch],
                       column_rename_rules: Dict[str, Any]):
    missing_cols = set([])
    expected_cols = set([])
    activity_records = []
    for m in matches:
        if m is None:
            continue

        activity_col_names = [c for c in m.activity_row.keys().tolist()]
        for grist_match in m.grist_rows.iterrows():
            grist_match = grist_match[1]

            activity_record = {}
            if activity.use_name_as_activity:
                activity_record['Activity'] = activity.name

            activity_record['object_id'] = grist_match['object_id']
            activity_record['state'] = grist_match['state']
            activity_record['university'] = grist_match['university']
            # TODO where is county?

            for col in activity.keep_cols:
                if col in activity_col_names:
                    renamed_col = maybe_rename_column(col, activity_state, column_rename_rules, activity)
                    activity_record[renamed_col] = m.activity_row[col].tolist()[0]
                else:
                    missing_cols.add(col)
                    expected_cols.update(list(m.activity_row.keys()))

            activity_records.append(activity_record)

    if missing_cols:
        log.error(f'missing col in state-data. expected {missing_cols}'
                  f' for state: {activity_state} activity: {activity.name} '
                  f'which had cols: {expected_cols}')

    return activity_records


def get_activity_column(activity, state, column_rename_rules):
    # which col in the rewrite rules is the one that becomes activity
    activity_rewrite_rules = column_rename_rules.get(state.lower()).get(activity.name.lower())
    if not activity_rewrite_rules:
        activity_rewrite_rules = column_rename_rules.get(state.lower()).get(activity.name)
        if not activity_rewrite_rules:
            return

    for original_col, output_column, in activity_rewrite_rules.items():
        if output_column.lower() == 'activity':
            return original_col


def update_grist_rows(grist_data_0, activity, state, matches, column_rename_rules):
    rename_rules = {'Coal': 'coal',
                    'OilAndGas': 'oilgas',
                    'OtherMin': 'othermin',
                    'OtherMinerals': 'othermin',
                    'Oil & Gas': 'oilgas'}

    obj_id_to_activities = defaultdict(set)
    for m in matches:
        if m is None:
            continue

        for grist_match in m.grist_rows.iterrows():
            grist_match = grist_match[1]

            row_loc = grist_data_0.loc[grist_data_0['object_id'] == grist_match['object_id']].index.tolist()
            if row_loc:
                update_row = row_loc[0]
                incumbent_activity_val = grist_data_0.loc[update_row, 'activity']

                if isinstance(incumbent_activity_val, str) and len(incumbent_activity_val) > 0:
                    for rename_trigger, new_name in rename_rules.items():
                        if rename_trigger in incumbent_activity_val:
                            obj_id_to_activities[update_row].add(new_name)

                if len(obj_id_to_activities[update_row]) == 0:
                    if isinstance(incumbent_activity_val, str) and len(incumbent_activity_val) > 0:
                        obj_id_to_activities[update_row].add(incumbent_activity_val)

                    if isinstance(incumbent_activity_val, list) and len(incumbent_activity_val) > 0:
                        obj_id_to_activities[update_row].update(incumbent_activity_val)

                if activity.use_name_as_activity:
                    obj_id_to_activities[update_row].add(activity.name)
                else:
                    activity_col = get_activity_column(activity, state, column_rename_rules)
                    if activity_col and activity_col in m.activity_row.keys():
                        activity_name = m.activity_row[activity_col].tolist()
                        if activity_name and isinstance(activity_name, str):
                            activity_name = activity_name[0]
                            obj_id_to_activities[update_row].add(activity_name)
                    else:
                        obj_id_to_activities[update_row].add(activity.name)

    for update_row, activities in obj_id_to_activities.items():
        grist_data_0.at[update_row, 'activity'] = list(activities)

    return grist_data_0


def simple_activity_rename(row):
    rename_rules = {'Coal': 'coal',
                    'OilAndGas': 'oilgas',
                    'OtherMin': 'othermin',
                    'OtherMinerals': 'othermin',
                    'Oil & Gas': 'oilgas'}

    incumbent_activity_val = row['activity']
    if isinstance(incumbent_activity_val, str) and len(incumbent_activity_val) > 0:
        for rename_trigger, new_name in rename_rules.items():
            if rename_trigger in incumbent_activity_val:
                row['activity'] = new_name

    return row


def match_all_activities(states_data=None, grist_data=None, column_rename_rules=None):
    log.info(f'processing states {states_data.keys()}')

    grist_data_original = grist_data.copy(deep=True)
    grist_data = []
    state_data = []
    for activity_state, activity_info in states_data.items():
        if not activity_info:
            log.error(f'NO ACTIVITY CONFIG FOR {activity_state}')
            continue

        grist_data_0 = grist_data_original[grist_data_original.state.isin([activity_state, activity_state.lower()])]

        for activity in activity_info.activities:
            matches = single_activity_match(activity_state, grist_data_0, activity)
            if matches is not None:
                updated_grist = update_grist_rows(grist_data_0, activity, activity_state, matches, column_rename_rules)
                grist_data.append(updated_grist)
                state_data += capture_state_data(activity_state, activity, matches, column_rename_rules)
            else:
                grist_data.append(grist_data_0.apply(simple_activity_rename, axis=1))

    grist_data_gdf = pd.concat(grist_data)
    state_data_gdf = geopandas.GeoDataFrame(data=state_data)

    return grist_data_gdf, state_data_gdf


def read_json(p: Path):
    with p.open('r') as fh:
        return json.load(fh)


def activity_to_str(row):
    activity = row['activity']
    if isinstance(activity, list):
        row['activity'] = ','.join(row['activity'])
    return row


def find_missing_cols(rewrite_rules, current_cols, the_out_dir):
    missing_cols = set(STATE_OUT_COLS) - set(current_cols)

    locs = []
    for state, acts in rewrite_rules.items():
        state_dict = defaultdict(list)
        for act, cols in acts.items():
            for in_col, out_col in cols.items():
                if out_col in missing_cols:
                    state_dict[out_col].append([state, act, in_col])
        if len(state_dict.keys()) > 0:
            locs.append(state_dict)

    with (the_out_dir / 'missing_col_info.json').open('w') as fh:
        json.dump(locs, fh)


def main(stl_path: Path, the_column_rename_rules_path: Path, the_out_dir: Path):
    if not the_out_dir.exists():
        the_out_dir.mkdir(parents=True, exist_ok=True)

    log.info(f'reading {stl_path}')
    column_rename_rules = read_json(the_column_rename_rules_path)

    gdf = GristCache(f'{stl_path}').cache_read('stl_file', '.feather')
    if gdf is None:
        gdf = geopandas.read_file(str(stl_path))
        GristCache(f'{stl_path}').cache_write(gdf, 'stl_file', '.feather')

    # debug_acts = {
    #     'AZ': state_activities['AZ'],
    #     'TX': state_activities['TX'],
    #     'MN': state_activities['MN'],
    # }
    # updated_grist_stl, state_data = match_all_activities(debug_acts, gdf, column_rename_rules)

    updated_grist_stl, state_data = match_all_activities(state_activities, gdf, column_rename_rules)

    state_data = state_data.drop_duplicates([c for c in state_data.columns if 'object_id' not in c], ignore_index=True)
    state_data.to_csv(str(the_out_dir / 'state_data_all_cols.csv'), index=False)
    state_data = state_data[[col for col in STATE_OUT_COLS if col in state_data.columns]]
    state_data.to_csv(str(the_out_dir / 'state_data.csv'), index=False)
    find_missing_cols(column_rename_rules, state_data.columns.tolist(), the_out_dir)

    updated_grist_stl.drop('joinidx_1', inplace=True, axis=1)
    updated_grist_stl = updated_grist_stl.apply(activity_to_str, axis=1)
    grist_data_cols = [c for c in updated_grist_stl.columns if 'object_id' not in c]
    updated_grist_stl = updated_grist_stl.drop_duplicates(grist_data_cols, ignore_index=True)
    updated_grist_stl.to_csv(str(the_out_dir / 'updated_grist_stl.csv'), index=False)


if __name__ == '__main__':
    stl = Path('/Users/marcellebonterre/Downloads/230815_nationals_STLs/0815_national_stls_deduplicated.geojson')
    STL_COMPARISON_BASE_DIR = Path('/Users/marcellebonterre/Downloads/STL_Activity_Layers')
    column_rename_rules_path = Path(
        '/Users/marcellebonterre/Projects/land-grab-2/scripts/activity_match_extras/rewrite_rules.json')
    out_dir = Path('/Users/marcellebonterre/Projects/land-grab-2/tests/foo')
    main(stl, column_rename_rules_path, out_dir)
