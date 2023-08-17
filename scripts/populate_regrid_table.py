import concurrent.futures
import json
import logging
import shutil
import tempfile
from pathlib import Path

import pysftp
from tqdm import tqdm

from land_grab.db import GristDB, GristTable, GristDbField

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

REGRID_TABLE = GristTable(name='Regrid',
                          fields=[GristDbField(name='geoid', constraints='text'),
                                  GristDbField(name='parcelnumb', constraints='text'),
                                  GristDbField(name='usecode', constraints='text'),
                                  GristDbField(name='usedesc', constraints='text'),
                                  GristDbField(name='zoning', constraints='text'),
                                  GristDbField(name='zoning_description', constraints='text'),
                                  GristDbField(name='struct', constraints='bool'),
                                  GristDbField(name='multistruct', constraints='bool'),
                                  GristDbField(name='structno', constraints='integer'),
                                  GristDbField(name='yearbuilt', constraints='integer'),
                                  GristDbField(name='structstyle', constraints='text'),
                                  GristDbField(name='parvaltype', constraints='text'),
                                  GristDbField(name='improvval', constraints='double precision'),
                                  GristDbField(name='landval', constraints='double precision'),
                                  GristDbField(name='parval', constraints='double precision'),
                                  GristDbField(name='agval', constraints='double precision'),
                                  GristDbField(name='saleprice', constraints='double precision'),
                                  GristDbField(name='saledate', constraints='date'),
                                  GristDbField(name='taxamt', constraints='double precision'),
                                  GristDbField(name='owntype', constraints='text'),
                                  GristDbField(name='owner', constraints='text'),
                                  GristDbField(name='ownfrst', constraints='text'),
                                  GristDbField(name='ownlast', constraints='text'),
                                  GristDbField(name='owner2', constraints='text'),
                                  GristDbField(name='owner3', constraints='text'),
                                  GristDbField(name='owner4', constraints='text'),
                                  GristDbField(name='subsurfown', constraints='text'),
                                  GristDbField(name='subowntype', constraints='text'),
                                  GristDbField(name='mailadd', constraints='text'),
                                  GristDbField(name='address_source', constraints='text'),
                                  GristDbField(name='legaldesc', constraints='text'),
                                  GristDbField(name='plat', constraints='text'),
                                  GristDbField(name='book', constraints='text'),
                                  GristDbField(name='page', constraints='text'),
                                  GristDbField(name='block', constraints='text'),
                                  GristDbField(name='lot', constraints='text'),
                                  GristDbField(name='neighborhood', constraints='text'),
                                  GristDbField(name='subdivision', constraints='text'),
                                  GristDbField(name='qoz', constraints='text'),
                                  GristDbField(name='census_block', constraints='text'),
                                  GristDbField(name='census_blockgroup', constraints='text'),
                                  GristDbField(name='census_tract', constraints='text'),
                                  GristDbField(name='sourceurl', constraints='text'),
                                  GristDbField(name='recrdareano', constraints='double precision'),
                                  GristDbField(name='gisacre', constraints='double precision'),
                                  GristDbField(name='ll_gisacre', constraints='double precision'),
                                  GristDbField(name='sqft', constraints='double precision'),
                                  GristDbField(name='ll_gissqft', constraints='double precision'),
                                  GristDbField(name='reviseddate', constraints='date'),
                                  GristDbField(name='ll_uuid', constraints='text'),
                                  GristDbField(name='padus_public_access', constraints='text'),
                                  GristDbField(name='lbcs_activity', constraints='integer'),
                                  GristDbField(name='lbcs_activity_desc', constraints='text'),
                                  GristDbField(name='lbcs_function', constraints='integer'),
                                  GristDbField(name='lbcs_function_desc', constraints='text'),
                                  GristDbField(name='lbcs_structure', constraints='integer'),
                                  GristDbField(name='lbcs_structure_desc', constraints='text'),
                                  GristDbField(name='lbcs_site', constraints='integer'),
                                  GristDbField(name='lbcs_site_desc', constraints='text'),
                                  GristDbField(name='lbcs_ownership', constraints='integer'),
                                  GristDbField(name='lbcs_ownership_desc', constraints='text'),
                                  GristDbField(name='lat', constraints='text'),
                                  GristDbField(name='lon', constraints='text'),
                                  GristDbField(name='taxyear', constraints='text'),
                                  GristDbField(name='ll_address_count', constraints='integer'),
                                  GristDbField(name='homestead_exemption', constraints='text'),
                                  GristDbField(name='alt_parcelnumb1', constraints='text'),
                                  GristDbField(name='alt_parcelnumb2', constraints='text'),
                                  GristDbField(name='alt_parcelnumb3', constraints='text'),
                                  GristDbField(name='parcelnumb_no_formatting', constraints='text'),
                                  GristDbField(name='plss_township', constraints='text'),
                                  GristDbField(name='plss_section', constraints='text'),
                                  GristDbField(name='plss_range', constraints='text'),
                                  GristDbField(name='geometry', constraints='json'),
                                  GristDbField(name='geometryType', constraints='text'),
                                  GristDbField(name='isRegrid', constraints='bool')])


def insert_geojson(geojson):
    try:
        db = GristDB()
        records = []
        for feature in geojson['features']:
            record = feature['properties']
            record['geometry'] = json.dumps(feature['geometry']['coordinates'])
            records.append(record)
        db.update_table(REGRID_TABLE, records)
    except Exception as err:
        log.error('Failed while attempting to insert geojson to regrid table')
        log.error(err)


def fetch_and_upload_regrid_geojsons():
    ftp_url = 'sftp.regrid.com'
    uname = 'grist'
    pword = 'sweeping-clamour-beheld-mesmeric'

    geojson_path = '/download/geoJSON'
    with pysftp.Connection(ftp_url, username=uname, password=pword) as sftp:
        with sftp.cd(geojson_path):
            zip_paths = sftp.listdir()
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
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
                                futures.append(executor.submit(insert_geojson, hydrated_json))

                done, incomplete = concurrent.futures.wait(futures)
                log.info(f'All records inserted done: {done}, incomplete:{incomplete}')


def main():
    log.info('Attempting to create Regrid table')
    GristDB().create_table(REGRID_TABLE)

    # indexes = [i[1] for i in db.list_indexes()]
    # index_col = 'parcelnumb'
    # if f'{index_col}_idx' not in indexes:
    #     log.info(f'Attempting to create index on {index_col}')
    #     db.create_index(REGRID_TABLE.name, index_col)

    fetch_and_upload_regrid_geojsons()


if __name__ == '__main__':
    main()
