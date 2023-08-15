from land_grab.db import GristDB, GristDbField


# TODO: move to mocked unit-test eventually....

def test_can_update_table(existing_table):
    pass


def test_can_fetch_all_data(existing_table):
    pass


def test_can_create_table():
    table_name = 'testcase_table'
    fields = [GristDbField(name='foo', constraints='integer'),
              GristDbField(name='bar', constraints='varchar(10)')]

    db = GristDB()
    db.create_table(table_name=table_name, fields=fields)

    exists_res = db.table_exists(table_name)
    assert exists_res

    columns = db.list_columns(table_name)
    col_names = [col[0] for col in columns]
    assert all(f.name in col_names for f in fields)

    db.delete_table(table_name)
