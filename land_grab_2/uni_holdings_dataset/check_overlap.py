import functools
import itertools
import json
import logging
import traceback
from pathlib import Path
from typing import List, Optional

import geopandas
from shapely import Polygon

from tasks.init_database.db import GristDB

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


def db_list_counties(state_code):
    return GristDB().fetch_from_col_where_val('county', 'state2', state_code, distinct=True)


def db_get_county_all(county, cb=None):
    return GristDB().fetch_from_col_where_val('*', 'county', county, callback=cb)


def db_info_to_geoseries(parcel) -> Optional[geopandas.GeoSeries]:
    geometry_json = parcel.get('geometry')
    if not geometry_json:
        return

    try:
        geojson = json.loads(geometry_json)
        all_polys = [Polygon([[float(x), float(y)] for x, y in points]) for points in geojson]
        return geopandas.GeoSeries(all_polys).set_crs(epsg=4326)
    except Exception as err:
        log.error(err)


def db_info_to_geoseries_2(parcel) -> Optional[geopandas.GeoSeries]:
    geometry = parcel.get('geometry')
    if not geometry:
        return

    coordinates = geometry.get('coordinates')
    if not coordinates:
        return

    if isinstance(coordinates, tuple):
        coordinates = [coordinates]

    try:
        all_polys_0 = [[Polygon([[float(x), float(y)] for x, y in points]) for points in p] for p in coordinates]
        all_polys = list(itertools.chain.from_iterable(all_polys_0))
        return geopandas.GeoSeries(all_polys).set_crs(epsg=3742)  # 4326)
    except Exception as err:
        log.error(err)




def check_parcel_overlap(overlapping_parcels, gdf, parcel):
    parcel_geoseries = db_info_to_geoseries(parcel)
    if parcel_geoseries is None:
        return
    intersection = parcel_geoseries.intersects(gdf.geometry)
    has_intersection = any(intersection.to_list())
    if has_intersection:
        overlapping_parcels.append(parcel)


def find_overlapping_parcels(gdf, state_code):
    overlapping_parcels = []
    counties = db_list_counties(state_code)
    for county_raw in counties:
        county = county_raw.get('county')
        if not county:
            continue

        check_overlap = functools.partial(check_parcel_overlap, overlapping_parcels, gdf)
        db_get_county_all(county, cb=check_overlap)

    return overlapping_parcels


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

        overlapping_parcels = find_overlapping_parcels(gdf, state_code)
        print(overlapping_parcels)
    except Exception as err:
        print(traceback.format_exc())
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
    # hydrate_geometry(None)
