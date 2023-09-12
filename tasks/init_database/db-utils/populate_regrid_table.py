import atexit
import json
import logging
import os
import shutil
from pathlib import Path

import dask
import dask.bag
import pandas as pd
from dask.diagnostics import ProgressBar
from tqdm import tqdm

from tasks.init_database.db.gen_regrid_table_def import regrid_schema_to_grist_table

logging.getLogger('pysftp').setLevel(logging.WARNING)
logging.getLogger('paramiko').setLevel(logging.WARNING)
logging.getLogger('__mp_main__').setLevel(logging.WARNING)
logging.getLogger('land_grab').setLevel(logging.WARNING)
try:
    logging.getLogger('gristdb').setLevel(logging.WARNING)
    logging.getLogger('land_grab.db-utils.gristdb').setLevel(logging.WARNING)
except:
    pass
import pysftp

from tasks.init_database.db.gristdb import GristDB

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)
FAILED_ZIP = []

REGRID_TABLE = regrid_schema_to_grist_table(Path('~/Downloads/regrid_parcel_schema.csv').expanduser())


def custom_obj_parse(o):
    if isinstance(o, list):
        return json.dumps(o)

    if 'geometry' in o and 'properties' in o:
        o['properties']['geometry'] = json.dumps(o['geometry']['coordinates'])
        return o['properties']

    if 'coordinates' in o:
        o['coordinates'] = json.dumps(o['coordinates'])

    if 'geometry' not in o and 'coordinates' not in o and 'geoid' not in o:
        return json.dumps(o)

    return o


def insert_geojson(zip_name, zip_path_local, retry=20):
    try:
        geojson = unzip_to_json(zip_path_local)
    except Exception as err:
        FAILED_ZIP.append(zip_name)
        return

    try:
        features_as_json = json.dumps(geojson['features'])
        records = json.loads(features_as_json,
                             object_hook=custom_obj_parse,
                             parse_float=str,
                             parse_int=str,
                             parse_constant=str)

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


def upload(zip_remote_path: Path):
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

    # MUST be outside sftp connection
    insert_geojson(zip_remote_path.name, zip_path_local)

    return True


def in_dask(batch, batch_size):
    with dask.config.set(scheduler='processes'):
        with ProgressBar():
            dask.bag.from_sequence(batch, partition_size=batch_size).map(upload).compute(scheduler='processes')


def main():
    ziplist = Path('/tasks/init_database/db-utils/zip_remote_paths.csv')
    df = pd.read_csv(ziplist)
    zipnames = df.zip_remote_path.tolist()

    zips_dir = Path(f'/Users/marcellebonterre/Projects/land-grab-2/scripts/zips')
    if not zips_dir.exists():
        zips_dir.mkdir(parents=True, exist_ok=True)

    batch_size = 25
    batches = [zipnames[i:i + batch_size] for i in range(0, len(zipnames), batch_size)]
    for batch in tqdm(batches):
        in_dask(batch, batch_size=5)

    # for batch in tqdm(batches):
    #     with concurrent.futures.ProcessPoolExecutor(max_workers=batch_size) as t_pool:
    #         fs = [t_pool.submit(upload, z) for z in batch]
    #         for f in concurrent.futures.as_completed(fs):
    #             f.result()
    # for z in batches[0]: upload(z)  # DEBUG ONLY


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
