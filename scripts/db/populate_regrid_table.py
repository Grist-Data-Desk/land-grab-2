import atexit
import concurrent.futures
import json
import logging
import os
import shutil
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


def unzip_to_json(zip_path_local: Path):
    json_path = None
    tmp = None
    try:
        tmpdir = Path('./downloads').resolve()
        shutil.unpack_archive(str(zip_path_local), tmpdir, format='zip')

        json_path = next((j for j in tmpdir.iterdir() if zip_path_local.name.split('.')[-3] in str(j)), None)
        if json_path:
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
    batch_size = 10
    with pysftp.Connection(ftp_url, username=uname, password=pword) as sftp:
        with sftp.cd(geojson_path):
            with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as t_pool:
                zip_paths_local = []
                for zip_name in tqdm(sftp.listdir()):
                    if len(zip_paths_local) == batch_size:
                        futures = []
                        for p in zip_paths_local:
                            futures.append(t_pool.submit(insert_geojson, zip_name, unzip_to_json(p), retry=20))
                        _ = [f.result() for f in concurrent.futures.as_completed(futures)]
                        zip_paths_local = []

                    zip_path_remote = str(Path(geojson_path) / zip_name)
                    zip_path_local = Path(f'./zips/{zip_name}').resolve()
                    sftp.get(zip_path_remote, str(zip_path_local))
                    zip_paths_local.append(zip_path_local)


def write_fails():
    tmp = Path('./zips/county.zip').resolve()
    tmpdir = Path('./downloads').resolve()
    try:
        for f in tmpdir.iterdir():
            os.remove(str(f))
        if tmp:
            os.remove(str(tmp))
    except:
        pass

    if FAILED_ZIP:
        df = pd.DataFrame({'failed_uploads': FAILED_ZIP})
        df.to_csv('failed_zips.csv', index=False)


if __name__ == '__main__':
    atexit.register(write_fails)
    main()
