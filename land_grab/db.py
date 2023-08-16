import enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

import psycopg2

from local_config.db_cred import DB_CREDS


# TODO add bulk insert
@dataclass
class GristDbField:
    name: str
    constraints: str


class GristDbResults(enum.Enum):
    ONE = 'one'
    ALL = 'all'


@dataclass
class GristTable:
    name: str
    fields: List[GristDbField] = field(default_factory=list)


class GristDB:
    def __init__(self):
        self.db = psycopg2.connect(**DB_CREDS)

    def execute(self, statement: str, results_type: Optional[GristDbResults] = None):
        result = None


        with self.db:
            with self.db.cursor() as cursor:
                cursor.execute(statement)

                if results_type and results_type == GristDbResults.ONE:
                    result = cursor.fetchone()

                if results_type and results_type == GristDbResults.ALL:
                    result = cursor.fetchall()

        return result

    def update_table(self, table: GristTable, data: Dict[str, Any]):
        if not self.table_exists(table.name):
            raise Exception('UnknownTableError: Must create table before attempting to fill it with data.')

        raw_field_names = [f.name for f in table.fields if f.name in data.keys()]

        values_raw = []
        for k in raw_field_names:
            if k in data:
                raw_val = data[k]
                if not raw_val:
                    val = 'NULL'
                else:
                    val = f"'{data[k]}'" if isinstance(data[k], str) else f'{data[k]}'
                values_raw.append(val)

        values = ', '.join(values_raw)
        field_names = ', '.join(raw_field_names)

        insert_sql = f'INSERT INTO {table.name}({field_names}) VALUES ({values})'

        return self.execute(insert_sql)

    def fetch_all_data(self, table_name: str):
        fetch_sql = f'SELECT * FROM {table_name};'
        return self.execute(fetch_sql, results_type=GristDbResults.ALL)

    def table_exists(self, table_name: str):
        exists_sql = f'''
            SELECT EXISTS ( SELECT * FROM pg_tables WHERE schemaname = 'public' AND tablename  = '{table_name}');
        '''
        return bool(self.execute(exists_sql, results_type=GristDbResults.ONE))

    def list_columns(self, table_name: str):
        list_sql = f"""
        SELECT column_name, data_type FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name   = '{table_name}';"""
        return self.execute(list_sql, results_type=GristDbResults.ALL)

    def create_table(self, table: GristTable):
        fields_sql = ',\n'.join([f"{f.name}\t{f.constraints}" for f in table.fields])
        create_table_sql = f'CREATE TABLE {table.name} (id  INT GENERATED ALWAYS AS IDENTITY, {fields_sql});'
        return self.execute(create_table_sql)

    def delete_table(self, table_name: str):
        del_table_sql = f'DROP TABLE {table_name};'
        return self.execute(del_table_sql)

    def create_index(self, table_name: str, column: str):
        index_sql = f'CREATE UNIQUE INDEX {column}_idx ON {table_name} ({column});'
        return self.execute(index_sql)

    def delete_index(self, column: str):
        index_sql = f'DROP INDEX {column}_idx;'
        return self.execute(index_sql)

    def list_indexes(self):
        list_sql = f'''
        SELECT
            tablename,
            indexname,
            indexdef
        FROM
            pg_indexes
        WHERE
            schemaname = 'public'
        ORDER BY
            tablename,
            indexname;
        '''
        return self.execute(list_sql, results_type=GristDbResults.ALL)
