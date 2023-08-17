import concurrent.futures
import json
import logging
import shutil
import tempfile
from pathlib import Path

import pandas as pd
import pysftp
from tqdm import tqdm

from land_grab.db.gristdb import GristDB
from land_grab.db.tables import REGRID_TABLE

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

FAILED_ZIP = []


def insert_geojson(zip_name, geojson, retry=5) -> bool:
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
            insert_geojson(geojson, retry=retry - 1)
        else:
            log.error(f'No more tries. Failed while attempting to insert geojson to regrid table: retry={retry}')
            log.error(err)
            FAILED_ZIP.append(zip_name)


def main():
    ftp_url = 'sftp.regrid.com'
    uname = 'grist'
    pword = 'sweeping-clamour-beheld-mesmeric'

    geojson_path = '/download/geoJSON'

    with pysftp.Connection(ftp_url, username=uname, password=pword) as sftp:
        with sftp.cd(geojson_path):
            zip_paths = sftp.listdir()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for zip_name in tqdm(zip_paths):
                    zip_path = str(Path(geojson_path) / zip_name)
                    with tempfile.NamedTemporaryFile(mode='w+b') as tmp:
                        sftp.get(zip_path, tmp.name)
                        with tempfile.TemporaryDirectory() as tmpdir:
                            shutil.unpack_archive(tmp.name, tmpdir, format='zip')
                            json_path = next(Path(tmpdir).iterdir(), None)
                            if json_path:
                                hydrated_json = json.load(Path(json_path).open())
                                futures.append(executor.submit(insert_geojson, zip_name, hydrated_json))
                done, incomplete = concurrent.futures.wait(futures)
                log.info(f'done: {len(done)} incomplete: {incomplete}')

    df = pd.DataFrame({
        'failed_uploads': FAILED_ZIP
    })
    df.to_csv('failed_zips.csv', index=False)


if __name__ == '__main__':
    main()
