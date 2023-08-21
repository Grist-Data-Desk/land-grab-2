import enum
import itertools
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

import psycopg

from local_config.db_cred import DB_CREDS

log = logging.getLogger(__name__)


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


class GristDbIndexType(enum.Enum):
    TEXT = 'text'


class GristDB:

    def execute(self,
                statement: str,
                results_type: Optional[GristDbResults] = None,
                data: Optional[Any] = None):
        result = None
        try:
            with psycopg.connect(connect_timeout=60, **DB_CREDS) as conn:
                with conn.cursor() as ps_cursor:
                    if data:
                        ps_cursor.execute(statement, data)
                    else:
                        ps_cursor.execute(statement)

                    if results_type and results_type == GristDbResults.ONE:
                        result = ps_cursor.fetchone()
                        if ps_cursor.description:
                            columns = ps_cursor.description
                            result = {col.name: result[i] for i, col in enumerate(columns)}

                    if results_type and results_type == GristDbResults.ALL:
                        result = ps_cursor.fetchall()
                        if ps_cursor.description:
                            columns = ps_cursor.description
                            result = [{col.name: row[i] for i, col in enumerate(columns)} for row in result]
        except Exception as err:
            log.info(f'db error during write NOT IGNORING: {err}')
            raise err

        try:
            conn.close()
        except Exception as err:
            log.info(f'failed while closing db conn with {err}')

        return result

    @staticmethod
    def _data_values_to_sql(table_fields: List[str], data: Dict[str, Any]) -> List[Any]:
        return [None if not data[k] else data[k] for k in table_fields if k in data]

    def update_table(self, table: GristTable, data: List[Dict[str, Any]]):
        if not data:
            return

        if not self.table_exists(table.name):
            raise Exception('UnknownTableError: Must create table before attempting to fill it with data.')

        raw_field_names = [f.name for f in table.fields if f.name in data[0].keys()]
        field_names = ', '.join(raw_field_names)
        row_width_sub_vars = '(' + ', '.join(['%s'] * len(raw_field_names)) + ')'
        data_len_insertion_rows = ', '.join([row_width_sub_vars] * len(data))
        insert_sql = f'INSERT INTO {table.name}({field_names}) VALUES {data_len_insertion_rows}'

        all_values = tuple(itertools.chain.from_iterable([self._data_values_to_sql(raw_field_names, d) for d in data]))

        return self.execute(insert_sql, data=all_values)

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

    def create_index(self, table_name: str, column: str, type: Optional[GristDbIndexType] = None):
        index_sql = f'CREATE INDEX {column}_idx ON {table_name} ({column});'
        if type == GristDbIndexType.TEXT:
            index_sql = f"CREATE INDEX {column}_idx ON {table_name} USING GIN (to_tsvector('english', {column}));"
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

    def copy_to(self, table: GristTable, data: List[Dict[str, Any]]):
        raw_field_names = [f.name for f in table.fields if f.name in data[0].keys()]
        rows = [tuple([d[f] for f in raw_field_names]) for d in data]

        field_names = ', '.join(raw_field_names)

        try:
            with psycopg.connect(connect_timeout=60, **DB_CREDS) as conn:
                with conn.cursor() as ps_cursor:
                    with ps_cursor.copy(f"COPY {table.name} ({field_names}) FROM STDIN;") as copy:
                        for row in rows:
                            copy.write_row(row)

            log.info('Txn Success')
        except Exception as err:
            log.info(f'db error during write NOT IGNORING: {err}')
            raise err

        try:
            conn.close()
        except Exception as err:
            log.info(f'failed while closing db conn with {err}')

    def search_indexed_text_column(self, table_name, column_name, query):
        search_sql = f"""
            SELECT * 
            FROM {table_name} 
            WHERE to_tsvector('english', {column_name}) @@ plainto_tsquery('english', '{query}');
        """

        return self.execute(search_sql, results_type=GristDbResults.ALL)

    def search_column_by_values(self, table_name: str, column_name: str, search_items: List[str]):
        formatted_search_items = search_items
        row_width_sub_vars = ', '.join([f"'{i}'" for i in formatted_search_items])

        search_sql = f"""
        SELECT * FROM {table_name} WHERE {column_name} IN ({row_width_sub_vars});
        """
        return self.execute(search_sql, results_type=GristDbResults.ALL)
