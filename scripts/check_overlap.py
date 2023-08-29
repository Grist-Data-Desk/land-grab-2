import logging
from pathlib import Path
from typing import List, Dict, Any

import geopandas
from shapely import Polygon

from land_grab.db.gristdb import GristDB

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def is_shapefile(p):
    return p.suffix in ('.shp', '.kml', '.geojson')


def gather_shapefile_paths(a_dir: Path) -> List[Path]:
    return [p for p in a_dir.iterdir() if is_shapefile(p)]


def state_code_from_filename(p):
    if 'utah' in str(p).lower():
        return 'UT'
    if 'nmsu' in str(p).lower():
        return 'NM'
    if 'minnesota' in str(p).lower():
        return 'MN'
    if 'wa.geojson' in str(p).lower():
        return 'WA'


def overlap_evaluation(row: Dict[str, Any]):
    a_row = row.get('geometry')
    if not a_row:
        log.error('NO GEOMETRY COLUMN')
        return
    # polys1 = geopandas.GeoSeries([Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
    #                               Polygon([(2, 2), (4, 2), (4, 4), (2, 4)])])
    # df1 = geopandas.GeoDataFrame({'geometry': polys1, 'df1': [1, 2]})
    # res = gdf.overlay(df1, how='intersection')
    assert 1


def process(p: Path):
    """
    p: Path to shapefile
    """
    # does shapefile contain county
    # query regrid for county
    # hydrate both regrid geometry field + shapefile
    # select regrid rows where intersection
    try:
        driver = 'KML' if 'kml' in p.name else None
        allow_unsupported_drivers = True if 'kml' in p.name else False
        gdf = geopandas.read_file(str(p), driver=driver, allow_unsupported_drivers=allow_unsupported_drivers)

        state_code = state_code_from_filename(p)
        if not state_code:
            return

        GristDB().search_column_value_in_set('regrid',
                                             'state2',
                                             [state_code],
                                             callback=overlap_evaluation)

    except Exception as err:
        log.error(err)


def main(data_dir: Path):
    # given a set of geometry entries from the regrid database and
    # a set of geometry entries from university primary source,
    # use shapely to gather regrid database entries where there is intersection with university primary source data

    for p in data_dir.iterdir():
        if is_shapefile(p):
            process(p)
        elif p.is_dir():
            for q in p.iterdir():
                if is_shapefile(q):
                    process(q)
        else:
            continue


if __name__ == '__main__':
    data_dir = Path('/Users/marcellebonterre/Downloads/univs_shapes')
    main(data_dir)
