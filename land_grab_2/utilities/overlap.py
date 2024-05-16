import itertools
import json
import logging
import traceback
from collections import Counter
from functools import partial
from typing import Optional, Any, Dict, Iterable

import geopandas
import numpy as np
import pandas as pd
from shapely import Polygon, MultiPolygon, make_valid, STRtree

from land_grab_2.stl_dataset.step_1.constants import GIS_ACRES, FINAL_DATASET_COLUMNS, RIGHTS_TYPE, ACTIVITY, ACRES, \
    GEOMETRY, OBJECT_ID, DATA_SOURCE
from land_grab_2.utilities.utils import in_parallel, combine_delim_list, batch_iterable

log = logging.getLogger(__name__)
STATE_LONG_NAME = {
    'AZ': 'arizona',
    'CO': 'colorado',
    'IA': 'iowa',
    'ID': 'idaho',
    'OR': 'oregon',
    'OK': 'oklahoma',
    'ND': 'north dakota',
    'NE': 'nebraska',
    'WI': 'wisconsin',
    'WA': 'washington',
    'MN': 'minnesota',
    'NC': 'north carolina',
    'VT': 'vermont',
    'WV': 'west virginia',
    'UT': 'utah',
    'NM': 'new mexico',
    'SD': 'south dakota',
    'TX': 'texas',
    'WY': 'wyoming',
    'MT': 'montana',
}


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


def is_much_bigger(feature_1, feature_2, tolerance: float = 0.15) -> bool:
    # if feature_1 area is bigger
    bigger = np.argmax([feature_1.area, feature_2.area])
    area_difference = abs(feature_1.area - feature_2.area)
    area_tolerance = tolerance * max(feature_1.area, feature_2.area)
    return bigger == 0 and area_difference > area_tolerance


def is_same_geo_feature(feature_1, feature_2, crs=None, tolerance: float = 0.15) -> bool:
    # if area is same
    area_difference = abs(feature_1.area - feature_2.area)
    area_tolerance = tolerance * max(feature_1.area, feature_2.area)
    if area_difference > area_tolerance:
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
    stop_list = [GEOMETRY, RIGHTS_TYPE, ACTIVITY, OBJECT_ID, 'OBJECTID', DATA_SOURCE, GIS_ACRES]
    acres_col = next((c for c in gdf.columns.tolist() if GIS_ACRES in c), None)
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
            if not all(last_row[k] == current_row[k] for k, v in last_row.items()
                       if k not in stop_list and not pd.isna(v)):
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
    missing_final_cols = list(set([c for c in FINAL_DATASET_COLUMNS if c not in common_cols]))
    common_cols += missing_final_cols

    # select intersected cols from all
    consistent_cols_df_list = [df[[c for c in common_cols if c in df.columns]] for df in df_list]

    # concat all
    df_crs = Counter([df.crs for df in df_list]).most_common(1)[0][0]
    consistent_cols_df_list = [df.to_crs(df_crs) for df in consistent_cols_df_list]
    merged = pd.concat(consistent_cols_df_list, ignore_index=True)
    merged_uniq = merged.drop([c for c in merged.columns if c not in FINAL_DATASET_COLUMNS], axis=1)

    # geometric rollup dedup
    # merged_uniq = geometric_deduplication(merged, df_crs, tolerance=tolerance)

    # drop unwanted columns
    # merged_uniq = merged_uniq.drop([c for c in merged_uniq.columns if c not in FINAL_DATASET_COLUMNS], axis=1)

    return merged_uniq


def fix_geometries(gdf):
    crs = gdf.crs
    gdf['geometry'] = gdf.geometry.map(lambda g: make_valid(g))
    gdf.set_crs(crs, inplace=True, allow_override=True).to_crs(crs)
    return gdf


def is_possibly_same_feature(feature_1, feature_2, crs=None, tolerance: float = 0.15) -> bool:
    return (
            feature_1.contains(feature_2) or
            feature_2.contains(feature_1) or
            feature_1.overlaps(feature_2) or
            feature_2.overlaps(feature_1) or
            feature_1.within(feature_2) or
            feature_2.within(feature_1) or
            feature_1.covers(feature_2) or
            feature_2.covers(feature_1) or
            # feature_1.intersects(feature_2) or
            # feature_2.intersects(feature_1) or
            # feature_1.crosses(feature_2) or
            # feature_2.crosses(feature_1) or

            # feature_1.touches(feature_2) or
            # feature_2.touches(feature_1) or

            feature_1.boundary.contains(feature_2.envelope) or
            feature_2.envelope.contains(feature_1.boundary) or
            feature_1.boundary.overlaps(feature_2.envelope) or
            feature_2.envelope.overlaps(feature_1.boundary) or
            feature_1.boundary.within(feature_2.envelope) or
            feature_2.envelope.within(feature_1.boundary) or
            feature_1.boundary.covers(feature_2.envelope) or
            feature_2.envelope.covers(feature_1.boundary) or
            # feature_1.boundary.intersects(feature_2.envelope) or
            # feature_2.envelope.intersects(feature_1.boundary) or
            # feature_1.boundary.crosses(feature_2.envelope) or
            # feature_2.envelope.crosses(feature_1.boundary) or

            # feature_1.boundary.touches(feature_2.envelope) or
            # feature_2.envelope.touches(feature_1.boundary) or

            # is_same_geo_feature(feature_1, feature_2, crs=crs, tolerance=tolerance) or
            False
    )


def smart_distance(g, batch, i):
    dists = []
    try:
        d = g['geometry'].envelope.distance(batch[i]['geometry'].envelope)
        dists.append(d)
    except:
        pass

    try:
        d = g['geometry'].boundary.distance(batch[i]['geometry'].boundary)
        dists.append(d)
    except:
        pass

    try:
        d = g['geometry'].boundary.distance(batch[i]['geometry'].envelope)
        dists.append(d)
    except:
        pass

    try:
        dists = [d for d in dists if not np.isnan(d)]
    except:
        pass

    return min(dists)


def _tree_based_proximity_batch(grist_bounds=None, grist_data=None, crs=None, match_dist_threshold=None, batch=None):
    other_envelopes = [None if g['geometry'] is None else g['geometry'].envelope for g in batch]
    indices = STRtree(other_envelopes).nearest(grist_bounds)

    pairs = sorted([
        (
            g['geometry'].boundary.distance(batch[i]['geometry'].envelope),
            grist_idx,
            g,
            batch[i],
            is_possibly_same_feature(g['geometry'], batch[i]['geometry'], crs=crs),
            i
        )
        for grist_idx, (g, i) in enumerate(zip(grist_data, indices))
        if smart_distance(g, batch, i) <= match_dist_threshold
    ], key=lambda p: p[0])

    return pairs
    # return itertools.takewhile(lambda x: x[0] <= match_dist_threshold, pairs)


def tree_based_proximity(grist_data: Iterable[Dict[str, Any]], other_data, crs, match_dist_threshold: float = 2.0,
                         too_many_records=10_000):
    grist_bounds = [g['geometry'].boundary for g in grist_data if g['geometry'] is not None]

    other_data = (
        other_data.set_crs(crs, allow_override=True).to_crs(crs) if not other_data.crs else other_data.to_crs(crs)
    )
    other_data_dicts = other_data.to_dict(orient='records')

    batches = [other_data_dicts]
    if len(other_data_dicts) > too_many_records:
        batches = batch_iterable(other_data_dicts, too_many_records)

    all_sorted_and_filtered_pairs = in_parallel(batches,
                                                partial(_tree_based_proximity_batch,
                                                        grist_bounds,
                                                        grist_data,
                                                        crs,
                                                        match_dist_threshold),
                                                scheduler='threads',
                                                batched=False)

    sorted_and_filtered_pairs_final = itertools.chain.from_iterable(all_sorted_and_filtered_pairs)

    return sorted_and_filtered_pairs_final
