from land_grab.db import GristDB, GristDbField, GristTable


# TODO: move to mocked unit-test eventually....

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
                               GristDbField(name='bar', constraints='varchar(10)')])

    db = GristDB()
    db.create_table(table)

    exists_res = db.table_exists(table.name)
    assert exists_res

    columns = db.list_columns(table.name)
    col_names = [col[0] for col in columns]
    assert all(f.name in col_names for f in table.fields)

    db.create_index(table.name, table.fields[0].name)
    indexes = db.list_indexes()
    assert len(indexes) == 1
    db.delete_index(table.fields[0].name)

    indexes = db.list_indexes()
    assert len(indexes) == 0

    db.delete_table(table.name)