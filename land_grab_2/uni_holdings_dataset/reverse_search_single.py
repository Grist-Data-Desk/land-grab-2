import logging
import os
import traceback
from datetime import datetime
from pathlib import Path

import pandas as pd
import typer

from land_grab_2.uni_holdings_dataset.reverse_search import process_university

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def run():
    print('running combine_reverse_search_results')
    data_tld = os.environ.get('DATA')
    data_directory = Path(f'{data_tld}/uni_holdings/reverse_search')

    try:
        out_dir = data_directory / 'output'
        if not out_dir.exists():
            out_dir.mkdir(parents=True, exist_ok=True)
        csv_path = data_directory / 'input/2308_LGU UNIS HACKATHON - UNIVERSITY QUERY TERMS.csv'
        df = pd.read_csv(csv_path, index_col=False, dtype=str)

        univs = df[df['University'].str.contains('Montana')].to_dict(orient='records')
        montana = univs[0]
        should_secondary_search = False

        st = datetime.now()
        process_university(should_secondary_search, out_dir, montana)
        print(f'processing took {datetime.now() - st}')

    except Exception as err:
        print(traceback.format_exc())
        log.error(err)


if __name__ == '__main__':
    run()
