import functools
import itertools
import json
import logging
import os
import shutil
import smtplib
import time
import uuid
from email.message import EmailMessage
from pathlib import Path
from typing import Optional

import dask
import dask.bag
import geopandas
import requests
from compose import compose
from dask.diagnostics import ProgressBar
# from joblib import Memory
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
from tqdm.dask import TqdmCallback

from land_grab_2.stl_dataset.step_1.constants import STATE_TRUST_DIRECTORY, QUERIED_DIRECTORY, CLEANED_DIRECTORY, \
    MERGED_DIRECTORY, CESSIONS_DIRECTORY, SUMMARY_STATISTICS_DIRECTORY, STL_OUTPUT_DIRECTORY

log = logging.getLogger(__name__)


# memory = Memory(str(Path(os.environ.get('DATA')) / 'cache'))


def send_email(to, subject, message):
    email_address = os.environ.get("EMAIL_ADDRESS")
    email_password = os.environ.get("EMAIL_PASSWORD")

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to
    msg.set_content(message)

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


def in_parallel_fake(work_items,
                     a_callable,
                     postprocess=None,
                     batched=True,
                     show_progress=False,
                     batch_size=10,
                     **kwargs):
    if postprocess:
        a_callable = compose(postprocess, a_callable)

    log.info('Using for-loop as scheduler')

    batches = [[w] for w in work_items]
    if batched:
        batches = batch_iterable(work_items, batch_size)

    if show_progress:
        batches = tqdm(batches)

    return list(itertools.chain.from_iterable([[a_callable(work_item) for work_item in batch] for batch in batches]))


def in_parallel_exp(work_items,
                    a_callable,
                    scheduler='processes',
                    postprocess=None,
                    batched=True,
                    show_progress=False,
                    batch_size=10):
    debug_parallelism = os.environ.get('DEBUG_PARALLEL')
    if debug_parallelism:
        scheduler = 'synchronous' if len(debug_parallelism) <= 5 else debug_parallelism

    if postprocess:
        a_callable = compose(postprocess, a_callable)

    if scheduler == 'synchronous':
        log.info('Using Dask synchronous scheduler')

    all_results = process_map(a_callable, work_items)
    return all_results


def in_parallel(work_items,
                a_callable,
                scheduler='processes',
                postprocess=None,
                batched=True,
                show_progress=False,
                batch_size=10):
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
            if show_progress:
                # with ProgressBar():
                with TqdmCallback(desc="compute"):
                    all_results = dask.bag.from_sequence(work_items).map(a_callable).compute()
                    return all_results
            else:
                all_results = dask.bag.from_sequence(work_items).map(a_callable).compute()
                return all_results

    partition_size = batch_size // 4
    partition_size = partition_size if partition_size > 0 else None
    batches = batch_iterable(work_items, batch_size)
    for batch in tqdm(batches):
        with dask.config.set(scheduler=scheduler):
            if show_progress:
                # with ProgressBar():
                with TqdmCallback(desc="compute"):
                    results = dask.bag.from_sequence(batch, partition_size=partition_size).map(a_callable).compute()
                    all_results += results
            else:
                results = dask.bag.from_sequence(batch, partition_size=partition_size).map(a_callable).compute()
                all_results += results

    return all_results


def batch_iterable(work_items, batch_size, generator=False):
    return (
        [work_items[i:i + batch_size] for i in range(0, len(work_items), batch_size)]
        if not generator else
        (work_items[i:i + batch_size] for i in range(0, len(work_items), batch_size))
    )


def read_json(p: Path):
    with p.open('r') as fh:
        return json.load(fh)


class GristCache:
    CACHE_DIR = None

    def __init__(self, location, cache_dir=None):
        self.location = location
        if not GristCache.CACHE_DIR:
            GristCache.CACHE_DIR = cache_dir
        self.base_dir = GristCache.CACHE_DIR

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


def _to_kebab_case(string):
    """convert string to kebab case"""
    if '_' in string:
        return "-".join(string.lower().split('_'))
    else:
        return "-".join(string.lower().split())


def _get_filename(state, label, alias, filetype):
    """return a filename in kebabcase"""
    if alias:
        return f'{_to_kebab_case(state)}-{_to_kebab_case(label)}-{_to_kebab_case(alias)}{filetype}'
    else:
        return f'{_to_kebab_case(state)}-{_to_kebab_case(label)}{filetype}'


@functools.lru_cache()
def extend_with_uuid(*args):
    v_uniq = '-'.join(
        [str(a) for a in args] + [str(uuid.uuid4())]
    )
    return v_uniq


def get_uuid():
    return str(uuid.uuid4())


def delete_files_and_subdirectories_in_directory(directory_path):
    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_file():
                    os.unlink(entry.path)
                else:
                    shutil.rmtree(entry.path)
        print("All files and subdirectories deleted successfully.")
    except OSError:
        print("Error occurred while deleting files and subdirectories.")


def prettyify_list_of_strings(row):
    for col in row.keys():
        if 'geometry' in col:
            if len(row[col]) == 0:
                pass
            else:
                row[col] = row[col][0]

            continue

        if isinstance(row[col], list):
            row[col] = ', '.join([str(i) for i in list(set(row[col]))])
    return row


def state_specific_directory(directory, state=None):
    if state:
        return directory + f'{state}/'
    else:
        return directory


def _queried_data_directory(state=None):
    return state_specific_directory(STATE_TRUST_DIRECTORY + QUERIED_DIRECTORY,
                                    state)


def _cleaned_data_directory(state=None):
    return state_specific_directory(STL_OUTPUT_DIRECTORY + CLEANED_DIRECTORY,
                                    state)


def _merged_data_directory(state=None):
    return state_specific_directory(STL_OUTPUT_DIRECTORY + MERGED_DIRECTORY,
                                    state)


def _cessions_data_directory(state=None):
    return state_specific_directory(STATE_TRUST_DIRECTORY + CESSIONS_DIRECTORY,
                                    state)


def _summary_statistics_data_directory(state=None):
    return state_specific_directory(
        STATE_TRUST_DIRECTORY + SUMMARY_STATISTICS_DIRECTORY, state)


def combine_delim_list(old_val, update_val, sep='+', do_sort=True):
    old_val = str(old_val)
    if old_val == 'nan':
        old_val = ''

    update_val = str(update_val)
    if update_val == 'nan':
        update_val = ''

    update_vals = [v.strip() for v in update_val.split(sep) if v.strip()]
    old_vals = [v.strip() for v in old_val.split(sep) if v.strip()]

    new_val = (sep.join(sorted(list(set(update_vals + old_vals))))
               if do_sort
               else sep.join(list(set(update_vals + old_vals))))

    return new_val


def index_of(it, f, default=-1):
    return next((i for i, e in enumerate(it) if f(e)), default)
