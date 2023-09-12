import logging
from pathlib import Path

import pandas as pd

from tasks.init_database.db.gristdb import GristTable, GristDbField, GristDB, GristDbIndexType

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
# TODO: INJECT GEOMETRY COLUMN
TYPES_MAP_REGRID_TO_GRIST = {
    'uuid': 'char(36)',
    'numeric': 'varchar(100)',
    'integer': 'varchar(100)',
    'bigint': 'varchar(200)',
    'double precision': 'varchar(100)',
    'serial primary key': 'integer',
    'timestamp with time zone': 'char(36)',
    'boolean': 'varchar(200)',
    'date': 'varchar(200)',
}


def as_grist_field(row):
    regrid_type = row['Type']
    grist_type = regrid_type
    if regrid_type in TYPES_MAP_REGRID_TO_GRIST:
        grist_type = TYPES_MAP_REGRID_TO_GRIST[regrid_type]

    name = row['Column Name']

    row['field'] = GristDbField(name=name, constraints=grist_type)

    return row


def regrid_schema_to_grist_table(csv_path: Path):
    log.info('hydrating regrid fields csv')
    df = pd.read_csv(csv_path, index_col=False, dtype=str)

    log.info('extracting regrid field information')
    df = df.apply(as_grist_field, axis=1)

    fields = df.field.tolist()
    fields.append(GristDbField(name='geometry', constraints='json'), )
    grist_table = GristTable(name='regrid', fields=fields)
    return grist_table


def create_indexes(regrid_table):
    log.info('preparing to create database indexes')
    db = GristDB()

    log.info('Creating database index on id column')
    db.create_index(regrid_table.name, 'id')

    log.info('Creating database index on parcelnumb column')
    db.create_index(regrid_table.name, 'parcelnumb')
    db.create_index(regrid_table.name, 'parcelnumb', type=GristDbIndexType.TEXT)

    log.info('Creating database index on parcelnumb_no_formatting column')
    db.create_index(regrid_table.name, 'parcelnumb_no_formatting')
    db.create_index(regrid_table.name, 'parcelnumb_no_formatting', type=GristDbIndexType.TEXT)

    log.info('Creating database index on alt_parcelnumb1 column')
    db.create_index(regrid_table.name, 'alt_parcelnumb1')
    db.create_index(regrid_table.name, 'alt_parcelnumb1', type=GristDbIndexType.TEXT)

    log.info('Creating database index on alt_parcelnumb2 column')
    db.create_index(regrid_table.name, 'alt_parcelnumb2')
    db.create_index(regrid_table.name, 'alt_parcelnumb2', type=GristDbIndexType.TEXT)

    log.info('Creating database index on state2 column')
    db.create_index(regrid_table.name, 'state2')
    db.create_index(regrid_table.name, 'state2', type=GristDbIndexType.TEXT)

    log.info('Creating database index on county column')
    db.create_index(regrid_table.name, 'county')
    db.create_index(regrid_table.name, 'county', type=GristDbIndexType.TEXT)

    log.info('Creating database index on owner column')
    db.create_index(regrid_table.name, 'owner', type=GristDbIndexType.TEXT)

    log.info('Creating database index on mailadd column')
    db.create_index(regrid_table.name, 'mailadd', type=GristDbIndexType.TEXT)

    log.info('done creating database indexes')
    log.info('Current database indexes listing:')
    log.info(db.list_indexes())


def main(csv_path: Path):
    grist_table = regrid_schema_to_grist_table(csv_path)

    db = GristDB()
    log.info('Attempting to create Regrid table')
    db.create_table(grist_table)
    create_indexes(grist_table)


if __name__ == '__main__':
    main(Path('~/Downloads/regrid_parcel_schema.csv').expanduser())
