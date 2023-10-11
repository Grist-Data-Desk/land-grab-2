import itertools
import json
import logging
import traceback
from functools import partial
from typing import Optional

import geopandas
import numpy as np
import pandas as pd
from shapely import Polygon, MultiPolygon

from land_grab_2.utilities.utils import in_parallel

log = logging.getLogger(__name__)


def add_idx_col(df, idx_name: str):
    if idx_name not in df.index:
        df[idx_name] = np.arange(0, df.shape[0]).astype(int).astype(str)
    df = df.drop_duplicates([
        c
        for c in df.columns
        if 'object' not in c
    ])
    return df


def stringify_df(df):
    stringcols = [c for c in df.columns if 'geometry' not in c]
    df[stringcols] = df[stringcols].fillna('').astype(str)
    return df


def eval_overlap_keep_left(left, right, crs_list=None, return_inputs=False):
    left = add_idx_col(left, 'joinidx_0')
    right = add_idx_col(right, 'joinidx_1')

    left_original = left.copy(deep=True)
    right_original = right.copy(deep=True)

    crs_list = crs_list or [left.crs]
    overlapping_regions = None
    for crs in crs_list:
        try:
            left = stringify_df(left)
            right = stringify_df(right)

            left = left.set_crs(crs, allow_override=True).to_crs(crs)
            right = right.set_crs(crs, allow_override=True).to_crs(crs)
        except Exception as err:
            print(traceback.format_exc())
            print(f'crs conversion error: {err}')

        overlapping_regions = geopandas.sjoin(left[['joinidx_0', 'geometry']],
                                              right[['joinidx_1', 'geometry']],
                                              how="left",
                                              predicate='intersects').dropna()
        if overlapping_regions.shape[0] > 0:
            if return_inputs:
                return overlapping_regions, left_original, right_original
            else:
                return overlapping_regions

    if return_inputs:
        return overlapping_regions, left_original, right_original
    else:
        return overlapping_regions


def is_polygon_def(arr, multi=True):
    if multi:
        return all(len(item) > 2 for item in arr)
    return all(len(item) == 2 and not (isinstance(item[0], list) or isinstance(item[0], list)) for item in arr)


def strs_to_floats(obj, hydrate_points=False):
    if isinstance(obj, str):
        return float(obj)

    if isinstance(obj, list):
        if len(obj) == 2:
            x, y = obj
            return strs_to_floats(x, hydrate_points), strs_to_floats(y, hydrate_points)

        if hydrate_points and is_polygon_def(obj, multi=False):
            polygon_shell = tuple([strs_to_floats(item, hydrate_points) for item in obj])
            polygon_holes = None
            return Polygon(polygon_shell, polygon_holes)

        return [strs_to_floats(item, hydrate_points) for item in obj]

    return obj


def dict_to_geodataframe(crs, parcel) -> Optional[geopandas.GeoSeries]:
    geometry_json = parcel.get('geometry')
    if not geometry_json:
        return

    try:
        geojson_0 = strs_to_floats(json.loads(geometry_json), hydrate_points=True)
        geojson = ([MultiPolygon(geojson_0)]
                   if all(isinstance(obj, Polygon) for obj in geojson_0)
                   else [MultiPolygon(p) for p in geojson_0])

        gdfs = []
        df = pd.DataFrame([parcel], dtype=str, columns=parcel.keys())
        for poly in geojson:
            gdf = geopandas.GeoDataFrame(df, crs=crs, geometry=[poly])
            gdfs.append(gdf)
        return gdfs
    except Exception as err:
        print(traceback.format_exc())
        log.error(err)


def dictlist_to_geodataframe(count_parcels, crs=None):
    gdfs = itertools.chain.from_iterable(
        in_parallel(count_parcels, partial(dict_to_geodataframe, crs), batched=False)
    )
    # gdfs = itertools.chain.from_iterable([dict_to_geodataframe(crs, p) for p in count_parcels])
    gdf = geopandas.GeoDataFrame(
        pd.concat(gdfs, ignore_index=True),
        crs=crs
    )
    return gdf
