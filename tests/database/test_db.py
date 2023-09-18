from datetime import datetime

from tasks.init_database.db import GristTable, GristDbField, GristDB, GristDbIndexType


# TODO: move to mocked unit-test eventually....
def test_copy_insert_syntax():
    table = GristTable(name='testcase_table',
                       fields=[GristDbField(name='foo', constraints='integer'),
                               GristDbField(name='bar', constraints='varchar(10)')])

    db = GristDB()
    db.create_table(table)

    exists_res = db.table_exists(table.name)
    assert exists_res

    columns = db.list_columns(table.name)
    col_names = [col[0] for col in columns]
    assert all(f.name in col_names for f in table.fields)

    s0 = datetime.now()
    db.update_table(table, [{'foo': 123, 'bar': 'abc'}, {'foo': 987, 'bar': 'xyz'}])
    s1 = datetime.now() - s0

    t0 = datetime.now()
    db.copy_to(table, [{'foo': 123, 'bar': 'abc'}, {'foo': 987, 'bar': 'xyz'}])
    t1 = datetime.now() - t0

    assert t1 < s1

    db.delete_table(table.name)


def test_multi_row_insert_syntax():
    table = GristTable(name='testcase_table',
                       fields=[GristDbField(name='foo', constraints='integer'),
                               GristDbField(name='bar', constraints='varchar(10)')])

    db = GristDB()
    db.create_table(table)

    exists_res = db.table_exists(table.name)
    assert exists_res

    columns = db.list_columns(table.name)
    # col_names = [col[0] for col in columns]
    # assert all(f.name in col_names for f in table.fields)

    db.update_table(table, [{'foo': 123, 'bar': 'abc'}, {'foo': 987, 'bar': 'xyz'}])

    contents = db.fetch_all_data(table.name)
    assert len(contents) == 2

    db.delete_table(table.name)


def test_can_update_table():
    table = GristTable(name='testcase_table',
                       fields=[GristDbField(name='foo', constraints='integer'),
                               GristDbField(name='bar', constraints='varchar(10)')])

    db = GristDB()
    db.create_table(table)

    exists_res = db.table_exists(table.name)
    assert exists_res

    columns = db.list_columns(table.name)
    col_names = [col[0] for col in columns]
    assert all(f.name in col_names for f in table.fields)

    db.update_table(table, {'foo': 123, 'bar': 'abc'})
    contents = db.fetch_all_data(table.name)
    assert len(contents) == 1

    db.delete_table(table.name)


def test_can_create_table():
    table = GristTable(name='testcase_table',
                       fields=[GristDbField(name='foo', constraints='integer'),
                               GristDbField(name='bar', constraints='varchar(10)')])

    db = GristDB()
    db.create_table(table)

    exists_res = db.table_exists(table.name)
    assert exists_res

    columns = db.list_columns(table.name)
    col_names = [col[0] for col in columns]
    assert all(f.name in col_names for f in table.fields)

    db.delete_table(table.name)


def test_index_creation_deletion():
    table = GristTable(name='testcase_table',
                       fields=[GristDbField(name='foo', constraints='integer'),
                               GristDbField(name='bar', constraints='varchar(10)'),
                               GristDbField(name='baz', constraints='text')])

    db = GristDB()
    db.create_table(table)

    exists_res = db.table_exists(table.name)
    assert exists_res

    columns = db.list_columns(table.name)
    col_names = [col[0] for col in columns]
    assert all(f.name in col_names for f in table.fields)

    db.create_index(table.name, table.fields[0].name)
    db.create_index(table.name, table.fields[2].name, type=GristDbIndexType.TEXT)
    indexes = db.list_indexes()
    db.delete_index(table.fields[0].name)
    db.delete_index(table.fields[2].name)

    indexes = db.list_indexes()
    assert len(indexes) == 0

    db.delete_table(table.name)


def test_reverse_search():
    db = GristDB()
    res = db.search_text_column_has_query('regrid', 'owner', 'ArKaNsAs')
    assert len(res) > 0
