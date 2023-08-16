import enum
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

import psycopg2

from local_config.db_cred import DB_CREDS


@dataclass
class GristDbField:
    name: str
    constraints: str


class GristDbResults(enum.Enum):
    ONE = 'one'
    ALL = 'all'


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

    def update_table(self, table_name: str, data):
        # TODO TODO TODO
        if not self.table_exists(table_name):
            fields = {}  # TODO: get schema from data
            self.create_table(table_name, fields=fields)
        self.update_table(table_name, data)

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

    def create_table(self, table_name: str, fields: List[GristDbField]):
        fields_sql = ',\n'.join([f"{f.name}\t{f.constraints}" for f in fields])
        create_table_sql = f'CREATE TABLE {table_name} (id  INT GENERATED ALWAYS AS IDENTITY, {fields_sql});'
        return self.execute(create_table_sql)

    def delete_table(self, table_name: str):
        del_table_sql = f'DROP TABLE {table_name};'
        return self.execute(del_table_sql)
