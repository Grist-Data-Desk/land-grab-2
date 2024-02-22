import functools
import logging
import os
import traceback
from datetime import datetime
from functools import partial
from pathlib import Path

import geopandas
import pandas as pd
import typer
from tqdm import tqdm

from land_grab_2.utilities.overlap import combine_dfs
from land_grab_2.utilities.utils import in_parallel

app = typer.Typer()


def hydrate_datafile(ext, f):
    if 'csv' in ext:
        return pd.read_csv(f, index_col=False, dtype=str)
    else:
        try:
            return geopandas.read_file(f)
        except Exception as err:
            print(f)
            print(err)


def should_read(f, ext=None, a_filter=None, prefer_feather: bool = False):
    if prefer_feather:
        return f.name.endswith('feather') and a_filter in f.name and 'results' in f.name
    else:
        return f.name.endswith(ext) and a_filter in f.name and 'results' in f.name


@functools.lru_cache
def has_feather(d: Path):
    return any('feather' in f.name for f in d.iterdir())


def make_all_feather(out_dir: Path, a_filter='owner', ext='geojson'):
    datafiles = [
        f
        for d in tqdm(list(out_dir.iterdir()))
        if d.is_dir() and not has_feather(d)
        for f in d.iterdir()
        if should_read(f, ext, a_filter, prefer_feather=has_feather(d))
    ]

    print('parallel featherizing datafiles')
    st = datetime.now()
    in_parallel(
        datafiles,
        lambda f: hydrate_datafile(ext, f).to_feather(f'{f.stem}.feather', index=False),
        show_progress=True,
        scheduler='synchronous',
        batched=False,
    )
    print(f'featherization took {datetime.now() - st}')


def main(out_dir: Path, a_filter='owner', ext='geojson'):
    print('gather datafile paths')
    datafiles = [
        f
        for d in tqdm(list(out_dir.iterdir()))
        if d.is_dir()
        for f in d.iterdir()
        if should_read(f, ext, a_filter, prefer_feather=has_feather(d))
    ]

    print('parallel hydrating datafiles')
    st = datetime.now()
    all_geojsons_f = in_parallel(
        datafiles,
        partial(hydrate_datafile, ext),
        show_progress=True,
        scheduler='threads',
        batched=False,
    )
    print(f'hydration took {datetime.now() - st}')

    if not all_geojsons_f:
        return

    if 'csv' in ext:
        gdf = pd.concat(all_geojsons_f)
        gdf.to_csv(out_dir / f'{a_filter}_reverse_search_combined_results.csv', index=False)
    else:
        gdf = pd.concat(all_geojsons_f)
        gdf = geopandas.GeoDataFrame(gdf, geometry=gdf.geometry, crs=all_geojsons_f[0].crs)
        gdf.to_csv(out_dir / f'{a_filter}_reverse_search_combined_results.csv', index=False)
        gdf.to_file(str(out_dir / f'{a_filter}_reverse_search_combined_results.geojson'), driver='GeoJSON')


@app.command()
def run():
    print('running combine_reverse_search_results')
    data_tld = os.environ.get('DATA')
    data_directory = Path(f'{data_tld}/uni_holdings/reverse_search')

    try:
        out_dir = data_directory / 'output'
        if not out_dir.exists():
            out_dir.mkdir(parents=True, exist_ok=True)
        # main(out_dir, 'owner', 'geojson')
        make_all_feather(out_dir, 'owner', 'geojson')
    except Exception as err:
        print(traceback.format_exc())


if __name__ == '__main__':
    run()
