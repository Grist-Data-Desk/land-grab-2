import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

import geopandas
import pandas as pd
from ratelimiter import RateLimiter

from land_grab_2.stl_dataset.step_2.land_activity_search.activity_match import STL_COMPARISON_BASE_DIR, log, \
    safe_geopandas_load
from land_grab_2.utils import GristCache, in_parallel, fetch_remote, fetch_all_parcel_ids


class StateActivityDataLocation(enum.Enum):
    LOCAL = 'local'
    REMOTE = 'remote'


@dataclass
class StateActivityDataSource:
    name: str
    location: str
    use_name_as_activity: bool = False
    keep_cols: List[str] = field(default_factory=list)
    scheduler: str = None
    use_cache: bool = True

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

    def load_remote(self, scheduler=None):
        cache = GristCache(self.location)
        activity_data_geopandas = cache.cache_read('activity_data_geopandas', '.feather')
        if self.use_cache and activity_data_geopandas is not None:
            return activity_data_geopandas

        cached_ids_resp = cache.cache_read('ids_resp')
        ids_resp = cached_ids_resp or self.fetch_all_parcel_ids()
        if not cached_ids_resp:
            cache.cache_write(ids_resp, 'ids_resp')

        if ids_resp:
            log.info(f'fetching remote activity data for {self.name} from: {self.location}')
            ids = ids_resp.get('objectIds', [])
            cached_activity_data = None
            if self.use_cache:
                cached_activity_data = cache.cache_read('activity_data')
            activity_data_raw = cached_activity_data or in_parallel(ids,
                                                                    self.fetch_remote,
                                                                    batched=False,
                                                                    scheduler=self.scheduler or 'threads')
            if not cached_activity_data:
                cache.cache_write(activity_data_raw, 'activity_data_raw')

            log.info(f'hydrating geodataframes activity data for {self.name} from: {self.location}')
            activity_data = in_parallel(activity_data_raw,
                                        safe_geopandas_load,
                                        batched=False,
                                        scheduler='threads')

            if activity_data:
                try:
                    log.info(f'concat-ing geodataframes activity data for {self.name} from: {self.location}')
                    gdfs = pd.concat(activity_data, ignore_index=True)

                    crs = activity_data[0].crs
                    # if 'spatialReference' in activity_data_raw and 'wkid' in activity_data_raw['spatialReference']:
                    #     crs = activity_data_raw['spatialReference']['wkid']

                    activity_data = geopandas.GeoDataFrame(gdfs, crs=crs).to_crs(crs)
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
    def fetch_remote(self, parcel_id: Optional[str] = None):
        return fetch_remote(self.location, parcel_id)

    def fetch_all_parcel_ids(self):
        return fetch_all_parcel_ids(self.location)


@dataclass
class StateForActivity:
    name: str
    activities: List[StateActivityDataSource]
    scheduler: str = None
    use_cache: bool = True
