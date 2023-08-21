import atexit
import concurrent.futures
import json
import logging
import os
import shutil
from pathlib import Path

import pandas as pd

logging.getLogger('pysftp').setLevel(logging.WARNING)
logging.getLogger('paramiko').setLevel(logging.WARNING)
logging.getLogger('__mp_main__').setLevel(logging.WARNING)
logging.getLogger('land_grab').setLevel(logging.WARNING)
try:
    logging.getLogger('gristdb').setLevel(logging.WARNING)
    logging.getLogger('land_grab.db.gristdb').setLevel(logging.WARNING)
except:
    pass
import pysftp
from tqdm import tqdm

from land_grab.db.gristdb import GristDB, GristDbIndexType
from land_grab.db.tables import REGRID_TABLE

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

FAILED_ZIP = []


def insert_geojson(zip_name, zip_path_local, retry=20):
    try:
        geojson = unzip_to_json(zip_path_local)
    except Exception as err:
        FAILED_ZIP.append(zip_name)
        return

    try:
        records = []
        for feature in geojson['features']:
            record = feature['properties']
            record['geometry'] = json.dumps(feature['geometry']['coordinates'])
            records.append(record)

        GristDB().copy_to(REGRID_TABLE, records)
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
            os.remove(str(zip_path_local))
        except:
            pass


def upload(zip_remote_path: str):
    log.info('Worker working')

    ftp_url = 'sftp.regrid.com'
    uname = 'grist'
    pword = 'sweeping-clamour-beheld-mesmeric'

    geojson_path = Path('/download/geoJSON')
    zip_remote_path = geojson_path / zip_remote_path
    with pysftp.Connection(ftp_url, username=uname, password=pword) as sftp:
        zip_path_local = Path(
            f'/Users/marcellebonterre/Projects/land-grab-2/scripts/zips/{zip_remote_path.name}'
        ).resolve()
        sftp.get(str(zip_remote_path), str(zip_path_local))
        insert_geojson(zip_remote_path.name, zip_path_local)

    return True


def main():
    ziplist = Path('/Users/marcellebonterre/Projects/land-grab-2/scripts/db/zip_remote_paths.csv')
    df = pd.read_csv(ziplist)
    zipnames = df.zip_remote_path.tolist()

    batch_size = 10
    batches = [zipnames[i:i + batch_size] for i in range(0, len(zipnames), batch_size)]
    for batch in tqdm(batches):
        with concurrent.futures.ProcessPoolExecutor(max_workers=batch_size) as t_pool:
            fs = [t_pool.submit(upload, z) for z in batch]
            for f in concurrent.futures.as_completed(fs):
                f.result()

    try:
        log.info('preparing to create database indexes')
        db = GristDB()

        log.info('Creating database index on id column')
        db.create_index('regrid', 'id')

        log.info('Creating database index on parcelnumb column')
        db.create_index('regrid', 'parcelnumb')

        log.info('Creating database index on parcelnumb_no_formatting column')
        db.create_index('regrid', 'parcelnumb_no_formatting')

        log.info('Creating database index on owner column')
        db.create_index('regrid', 'owner', type=GristDbIndexType.TEXT)

        log.info('Creating database index on mailadd column')
        db.create_index('regrid', 'mailadd', type=GristDbIndexType.TEXT)

        log.info('done creating database indexes')
        log.info('Current database indexes listing:')
        log.info(db.list_indexes())
    except Exception as err:
        log.error(err)


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
