from pathlib import Path

import pandas as pd

from land_grab.db import GristDB

import typer

app = typer.Typer()


def upload_csv(csv: Path, table_name):
    csv_df = pd.read_csv(csv)
    db = GristDB()

    data = None
    if not db.table_exists(table_name):
        fields = {}  # TODO: columns of csv
        db.create_table(table_name, fields)
    else:
        data = None  # TODO: subset columns of the csv to only those of table columns
        pass

    data = data or {}  # TODO: extract data from csv
    db.update_table(table_name, data)


@app.command()
def main(csv: Path, table_name: str):
    upload_csv(csv, table_name)


if __name__ == '__main__':
    main()
