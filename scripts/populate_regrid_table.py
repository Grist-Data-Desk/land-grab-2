import json
import logging
import shutil
import tempfile
from pathlib import Path
from typing import Optional

import pysftp

from land_grab.db import GristDB, GristTable, GristDbField
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

REGRID_TABLE = GristTable(name='Regrid',
                          fields=[GristDbField(name='geoid', constraints='varchar(200)'),
                                  GristDbField(name='parcelnumb', constraints='varchar(200)'),
                                  GristDbField(name='usecode', constraints='varchar(200)'),
                                  GristDbField(name='usedesc', constraints='varchar(200)'),
                                  GristDbField(name='zoning', constraints='varchar(200)'),
                                  GristDbField(name='zoning_description', constraints='varchar(200)'),
                                  GristDbField(name='struct', constraints='bool'),
                                  GristDbField(name='multistruct', constraints='bool'),
                                  GristDbField(name='structno', constraints='integer'),
                                  GristDbField(name='yearbuilt', constraints='integer'),
                                  GristDbField(name='structstyle', constraints='varchar(200)'),
                                  GristDbField(name='parvaltype', constraints='varchar(200)'),
                                  GristDbField(name='improvval', constraints='double precision'),
                                  GristDbField(name='landval', constraints='double precision'),
                                  GristDbField(name='parval', constraints='double precision'),
                                  GristDbField(name='agval', constraints='double precision'),
                                  GristDbField(name='saleprice', constraints='double precision'),
                                  GristDbField(name='saledate', constraints='date'),
                                  GristDbField(name='taxamt', constraints='double precision'),
                                  GristDbField(name='owntype', constraints='varchar(200)'),
                                  GristDbField(name='owner', constraints='varchar(200)'),
                                  GristDbField(name='ownfrst', constraints='varchar(200)'),
                                  GristDbField(name='ownlast', constraints='varchar(200)'),
                                  GristDbField(name='owner2', constraints='varchar(200)'),
                                  GristDbField(name='owner3', constraints='varchar(200)'),
                                  GristDbField(name='owner4', constraints='varchar(200)'),
                                  GristDbField(name='subsurfown', constraints='varchar(200)'),
                                  GristDbField(name='subowntype', constraints='varchar(200)'),
                                  GristDbField(name='mailadd', constraints='varchar(200)'),
                                  GristDbField(name='address_source', constraints='varchar(200)'),
                                  GristDbField(name='legaldesc', constraints='varchar(200)'),
                                  GristDbField(name='plat', constraints='varchar(200)'),
                                  GristDbField(name='book', constraints='varchar(200)'),
                                  GristDbField(name='page', constraints='varchar(200)'),
                                  GristDbField(name='block', constraints='varchar(200)'),
                                  GristDbField(name='lot', constraints='varchar(200)'),
                                  GristDbField(name='neighborhood', constraints='varchar(200)'),
                                  GristDbField(name='subdivision', constraints='varchar(200)'),
                                  GristDbField(name='qoz', constraints='varchar(200)'),
                                  GristDbField(name='census_block', constraints='varchar(200)'),
                                  GristDbField(name='census_blockgroup', constraints='varchar(200)'),
                                  GristDbField(name='census_tract', constraints='varchar(200)'),
                                  GristDbField(name='sourceurl', constraints='varchar(200)'),
                                  GristDbField(name='recrdareano', constraints='double precision'),
                                  GristDbField(name='gisacre', constraints='double precision'),
                                  GristDbField(name='ll_gisacre', constraints='double precision'),
                                  GristDbField(name='sqft', constraints='double precision'),
                                  GristDbField(name='ll_gissqft', constraints='double precision'),
                                  GristDbField(name='reviseddate', constraints='date'),
                                  GristDbField(name='ll_uuid', constraints='varchar(200)'),
                                  GristDbField(name='padus_public_access', constraints='varchar(200)'),
                                  GristDbField(name='lbcs_activity', constraints='integer'),
                                  GristDbField(name='lbcs_activity_desc', constraints='varchar(200)'),
                                  GristDbField(name='lbcs_function', constraints='integer'),
                                  GristDbField(name='lbcs_function_desc', constraints='varchar(200)'),
                                  GristDbField(name='lbcs_structure', constraints='integer'),
                                  GristDbField(name='lbcs_structure_desc', constraints='varchar(200)'),
                                  GristDbField(name='lbcs_site', constraints='integer'),
                                  GristDbField(name='lbcs_site_desc', constraints='varchar(200)'),
                                  GristDbField(name='lbcs_ownership', constraints='integer'),
                                  GristDbField(name='lbcs_ownership_desc', constraints='varchar(200)'),
                                  GristDbField(name='lat', constraints='varchar(200)'),
                                  GristDbField(name='lon', constraints='varchar(200)'),
                                  GristDbField(name='taxyear', constraints='varchar(200)'),
                                  GristDbField(name='ll_address_count', constraints='integer'),
                                  GristDbField(name='homestead_exemption', constraints='varchar(200)'),
                                  GristDbField(name='alt_parcelnumb1', constraints='varchar(200)'),
                                  GristDbField(name='alt_parcelnumb2', constraints='varchar(200)'),
                                  GristDbField(name='alt_parcelnumb3', constraints='varchar(200)'),
                                  GristDbField(name='parcelnumb_no_formatting', constraints='varchar(200)'),
                                  GristDbField(name='plss_township', constraints='varchar(200)'),
                                  GristDbField(name='plss_section', constraints='varchar(200)'),
                                  GristDbField(name='plss_range', constraints='varchar(200)'),
                                  GristDbField(name='geometry', constraints='json'),
                                  GristDbField(name='geometryType', constraints='varchar(50)'),
                                  GristDbField(name='isRegrid', constraints='bool')])


def fetch_regrid_geojsons():
    ftp_url = 'sftp.regrid.com'
    uname = 'grist'
    pword = 'sweeping-clamour-beheld-mesmeric'

    geojson_path = '/download/geoJSON'
    with pysftp.Connection(ftp_url, username=uname, password=pword) as sftp:
        with sftp.cd(geojson_path):
            zip_paths = sftp.listdir()
            for zip_name in tqdm(zip_paths):
                zip_path = str(Path(geojson_path) / zip_name)
                with tempfile.NamedTemporaryFile(mode='w+b') as tmp:
                    sftp.get(zip_path, tmp.name)
                    with tempfile.TemporaryDirectory() as tmpdir:
                        shutil.unpack_archive(tmp.name, tmpdir, format='zip')
                        json_path = next(Path(tmpdir).iterdir(), None)
                        if json_path:
                            hydrated_json = json.load(Path(json_path).open())
                            yield hydrated_json


def main():
    db = GristDB()

    log.info('Attempting to create Regrid table')
    db.create_table(REGRID_TABLE)

    # indexes = [i[1] for i in db.list_indexes()]
    # index_col = 'parcelnumb'
    # if f'{index_col}_idx' not in indexes:
    #     log.info(f'Attempting to create index on {index_col}')
    #     db.create_index(REGRID_TABLE.name, index_col)

    for geojson in fetch_regrid_geojsons():
        try:
            for feature in geojson['features']:
                record = feature['properties']
                record['geometry'] = json.dumps(feature['geometry']['coordinates'])
                db.update_table(REGRID_TABLE, record)
        except Exception as err:
            log.error('Failed while attempting to insert geojson to regrid table')
            log.error(err)


if __name__ == '__main__':
    main()
