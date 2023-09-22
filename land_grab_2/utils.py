import json
import logging
import os
import time
from pathlib import Path
from typing import Optional

import dask
import dask.bag
import geopandas
import requests
from compose import compose
from dask.diagnostics import ProgressBar
from tqdm import tqdm

log = logging.getLogger(__name__)


def in_parallel(work_items, a_callable, scheduler='processes', postprocess=None, batched=True, batch_size=10):
    debug_parallelism = os.environ.get('DEBUG_PARALLEL')
    if debug_parallelism:
        scheduler = 'synchronous' if len(debug_parallelism) <= 5 else debug_parallelism

    if postprocess:
        a_callable = compose(postprocess, a_callable)

    if scheduler == 'synchronous':
        log.info('Using Dask synchronous scheduler')

    all_results = []
    if not batched:
        with dask.config.set(scheduler=scheduler):
            with ProgressBar():
                all_results = dask.bag.from_sequence(work_items).map(a_callable).compute()
                return all_results

    partition_size = batch_size // 4
    partition_size = partition_size if partition_size > 0 else None
    batches = batch_iterable(work_items, batch_size)
    for batch in tqdm(batches):
        with dask.config.set(scheduler=scheduler):
            with ProgressBar():
                results = dask.bag.from_sequence(batch, partition_size=partition_size).map(a_callable).compute()
                all_results += results

    return all_results


def batch_iterable(work_items, batch_size):
    return [work_items[i:i + batch_size] for i in range(0, len(work_items), batch_size)]


def read_json(p: Path):
    with p.open('r') as fh:
        return json.load(fh)


class GristCache:
    def __init__(self, location, cache_dir=None):
        self.location = location
        self.base_dir = cache_dir

    def cache_write(self, obj, name, file_ext='.json'):
        """
        this function requires the ENV var: PYTHONHASHSEED to be set to ensure stable hashing between runs
        """
        here = self.base_dir / f'{hash(self.location)}'
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
        here = self.base_dir / f'{hash(self.location)}'

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


# ==============================


def fetch_remote(url_base, parcel_id: Optional[str] = None, retries=10, response_type='text'):
    """
    response_type: str - either `json` or `text`
    """
    url_base = f'{url_base}?'

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
            return fetch_remote(url_base, parcel_id=parcel_id, retries=retries - 1, response_type=response_type)
        else:
            log.error(err)
            return None


# Here, we want to call on the SD PLSS quarter-quarter server.
def fetch_all_parcel_ids(url_base, retries=10):
    url_base = f'{url_base}?'

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
            return fetch_all_parcel_ids(url_base, retries=retries - 1)
        else:
            log.error(err)
            return None


def geodf_overlap_cmp_keep_left(left, right):
    try:
        if not 'joinidx_1' in left.index:
            left["joinidx_1"] = np.arange(0, left.shape[0]).astype(int).astype(str)

        right = right.drop_duplicates([
            c
            for c in right.columns
            if 'object' not in c
        ])
        right["joinidx_0"] = np.arange(0, right.shape[0]).astype(int)

        right = right.to_crs(left.crs)
        overlapping_regions = geopandas.sjoin(right[['joinidx_0', 'geometry']],
                                              left[['joinidx_1', 'geometry']],
                                              how="left",
                                              predicate='intersects').dropna()
        return overlapping_regions
    except Exception as err:
        try:
            right = right.set_crs(left.crs).to_crs(left.crs)
            return geodf_overlap_cmp_keep_left(left, right)
        except Exception as err:
            print(f'failing on mysterious except')
            assert 1
