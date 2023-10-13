import itertools
import json
import logging
import traceback
from collections import Counter
from functools import partial
from typing import Optional, Any

import geopandas
import numpy as np
import pandas as pd
from shapely import Polygon, MultiPolygon

from land_grab_2.stl_dataset.step_1.constants import GIS_ACRES, FINAL_DATASET_COLUMNS, RIGHTS_TYPE, ACTIVITY
from land_grab_2.utilities.utils import in_parallel, combine_delim_list

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


def is_same_geo_feature(feature_1, feature_2, crs=None, tolerance: float = 0.15) -> bool:
    # if area is same
    area_difference = abs(feature_1.area - feature_2.area)
    tolerance = tolerance * max(feature_1.area, feature_2.area)
    if area_difference > tolerance:
        return False

    percent_diff = 100 * (area_difference / max(feature_1.area, feature_2.area))
    if area_difference > 0.0:
        assert 1

    # if shape is same
    is_same_shape = feature_1.equals_exact(feature_2, tolerance)
    if not is_same_shape:
        return False

    # if geo has overlap
    feature_1_geo = geopandas.GeoSeries([feature_1], crs=crs)
    feature_2_geo = geopandas.GeoSeries([feature_2], crs=crs)
    is_intersecting = feature_1_geo.intersects(feature_2_geo)
    if is_intersecting is None or not is_intersecting.bool():
        return False

    return True


def geometric_deduplication(gdf: pd.DataFrame, crs: Any, tolerance: float = 0.15) -> pd.DataFrame:
    stop_list = ['geometry', RIGHTS_TYPE, ACTIVITY]
    acres_col = next((c for c in gdf.columns.tolist() if GIS_ACRES in c or 'acre' in c), None)
    if not acres_col:
        return gdf

    smallest_area_first_gdf = gdf.sort_values(by=[acres_col])

    dup_rows = []
    uniq_rows = []
    last_row = None
    for i, current_row in enumerate(smallest_area_first_gdf.to_dict(orient='records')):
        if last_row is None:
            uniq_rows.append(current_row)
            last_row = current_row
            continue

        if not is_same_geo_feature(last_row['geometry'], current_row['geometry'], crs=crs, tolerance=tolerance):
            uniq_rows.append(current_row)
            last_row = current_row
            continue
        else:
            if not all(last_row[k] == current_row[k] for k in last_row.keys() if k not in stop_list):
                uniq_rows.append(current_row)
                last_row = current_row
                continue

            if (RIGHTS_TYPE in last_row and
                    RIGHTS_TYPE in current_row and
                    last_row[RIGHTS_TYPE] != current_row[RIGHTS_TYPE]):
                last_row[RIGHTS_TYPE] = combine_delim_list(last_row[RIGHTS_TYPE], current_row[RIGHTS_TYPE])

            if (ACTIVITY in last_row and
                    ACTIVITY in current_row and
                    last_row[ACTIVITY] != current_row[ACTIVITY]):
                last_row[ACTIVITY] = combine_delim_list(last_row[ACTIVITY], current_row[ACTIVITY])

            dup_rows.append(current_row)

    if dup_rows:
        dup_df = pd.DataFrame(dup_rows)
        dup_geodf = geopandas.GeoDataFrame(dup_df, geometry=dup_df.geometry, crs=smallest_area_first_gdf.crs)
        assert 1

    uniq_df = pd.DataFrame(uniq_rows)
    uniq_geodf = geopandas.GeoDataFrame(uniq_df, geometry=uniq_df.geometry, crs=smallest_area_first_gdf.crs)

    return uniq_geodf


def combine_dfs(df_list, tolerance: float = 0.15):
    # find col intersection of all
    common_cols = list(set.intersection(*[set(df.columns.tolist()) for df in df_list]))

    # select intersected cols from all
    consistent_cols_df_list = [df[common_cols] for df in df_list]

    # concat all
    df_crs = Counter([df.crs for df in df_list]).most_common(1)[0][0]
    consistent_cols_df_list = [df.to_crs(df_crs) for df in consistent_cols_df_list]
    merged = pd.concat(consistent_cols_df_list, ignore_index=True)

    # geometric rollup dedup
    merged_uniq = geometric_deduplication(merged, df_crs, tolerance=tolerance)

    # drop unwanted columns
    merged_uniq = merged_uniq.drop([c for c in merged_uniq.columns if c not in FINAL_DATASET_COLUMNS], axis=1)

    return merged_uniq
