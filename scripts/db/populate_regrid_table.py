import atexit
import concurrent.futures
import json
import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

import pandas as pd
import pysftp
from tqdm import tqdm

from land_grab.db.gristdb import GristDB
from land_grab.db.tables import REGRID_TABLE

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

FAILED_ZIP = []


def insert_geojson(zip_name, geojson, retry=20):
    try:
        records = []
        for feature in geojson['features']:
            record = feature['properties']
            record['geometry'] = json.dumps(feature['geometry']['coordinates'])
            records.append(record)

        GristDB().update_table(REGRID_TABLE, records)
    except Exception as err:
        log.error(f'Failed while attempting to insert geojson to regrid table: retry={retry}')
        log.error(err)
        if retry > 0:
            insert_geojson(zip_name, geojson, retry=retry - 1)
        else:
            log.error(f'No more tries. Zip name: {zip_name} retry={retry}')
            log.error(err)
            FAILED_ZIP.append(zip_name)


def remote_zip_path_to_db(sftp: Any, zip_path: Any):
    json_path = None
    tmp = None
    try:
        tmp = Path('./zips/county.zip').resolve()
        log.info('fetch zip file')
        sftp.get(zip_path, str(tmp))

        tmpdir = Path('./downloads').resolve()
        log.info('unzip to json on disk')
        shutil.unpack_archive(str(tmp), tmpdir, format='zip')

        json_path = next(tmpdir.iterdir(), None)
        if json_path:
            log.info('hydrate json')
            hydrated_json = json.load(Path(json_path).open())
            return hydrated_json
    except Exception as err:
        log.error(f'error while remote_zip_path_to_db err: {err}')
    finally:
        try:
            if json_path:
                os.remove(json_path)
            if tmp:
                os.remove(str(tmp))
        except:
            pass


def main():
    ftp_url = 'sftp.regrid.com'
    uname = 'grist'
    pword = 'sweeping-clamour-beheld-mesmeric'

    geojson_path = '/download/geoJSON'

    with pysftp.Connection(ftp_url, username=uname, password=pword) as sftp:
        with sftp.cd(geojson_path):
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for zip_name in tqdm(sftp.listdir()):
                    zip_path = str(Path(geojson_path) / zip_name)
                    hydrated_json = remote_zip_path_to_db(sftp, zip_path)
                    futures.append(executor.submit(insert_geojson, zip_name, hydrated_json, retry=20))
                done, incomplete = concurrent.futures.wait(futures)
                log.info(f'done: {len(done)} incomplete: {incomplete}')


def write_fails():
    if FAILED_ZIP:
        df = pd.DataFrame({'failed_uploads': FAILED_ZIP})
        df.to_csv('failed_zips.csv', index=False)


if __name__ == '__main__':
    atexit.register(write_fails)
    main()
