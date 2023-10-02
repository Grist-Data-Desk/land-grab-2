import traceback

import geopandas
import numpy as np


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
