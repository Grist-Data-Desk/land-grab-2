import logging
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def remove_0beforeAorL(s):
    location = s.find("SN")
    if location != -1:
        return s[:location + 4] + s[location + 5:]
    return s


def reformat_secdivid(s, cut_list):
    for pattern_group in cut_list:
        for pattern in pattern_group:
            location = s.find(pattern)
            if location != -1:
                s = s[:location] + s[location + len(pattern):]
                break
    return s


def surface_sdqq_parceladjust(secdivid):
    return remove_0beforeAorL(secdivid[4:])


def subsurface_sdqq_parceladjust(secdivid):
    subsurfaceadjust1 = reformat_secdivid(secdivid[4:], [["0W0", "0E0"], ["0N", "0S"]], )
    subtest = remove_0beforeAorL(subsurfaceadjust1)
    return subtest


def find_item(needle, haystack, haystack_name):
    try:
        location = haystack.index(needle)
        if location != -1:
            return location
    except ValueError as err:
        log.error(f'NotFoundError: Could not find {needle} in {haystack_name}')

    return None


def main():
    match_parcels_info_path = Path('data/csv/matched_parcels_info/DONE_ORIGIAL_Table_1.csv').resolve() #
                                    # this file refers to the done.csv, aka, list of downloaded rows from the server
    surface_parcels_path = Path('data/csv/sd_surface.csv').resolve() # for this file and below, use sub/surf generated csvs
    subsurface_parcels_path = Path('data/csv/sd_subsurface.csv').resolve()

    matched_parcels_info_df = pd.read_csv(match_parcels_info_path)
    surface_parcels_df = pd.read_csv(surface_parcels_path)
    subsurface_parcels_df = pd.read_csv(subsurface_parcels_path, skiprows=1)

    matched_secdivids = matched_parcels_info_df.SECDIVID.to_list()
    surface_secdivids = [item.replace(' ', '') for item in surface_parcels_df['FIXED PLSS ID'].to_list()]
    subsurface_secdivids = [item.replace(' ', '') for item in subsurface_parcels_df['FIXED PLSS NUMBER'].to_list()]

    match_reports = []
    matched_surface_items = []
    matched_subsurface_items = []

    for secdivid_from_sd_server in matched_secdivids:
        surface_fmt = surface_sdqq_parceladjust(secdivid_from_sd_server)
        surface_match_row = find_item(surface_fmt, surface_secdivids, 'surface secdivids')
        surface_match_value = surface_match_row and surface_secdivids[surface_match_row] or None
        matched_surface_items.append(surface_fmt)

        subsurface_fmt = subsurface_sdqq_parceladjust(secdivid_from_sd_server)
        subsurface_match_row = find_item(subsurface_fmt, subsurface_secdivids, 'subsurface secdivids')
        subsurface_match_value = subsurface_match_row and subsurface_secdivids[subsurface_match_row] or None
        matched_subsurface_items.append(subsurface_fmt)

        match_type = ((surface_match_value and subsurface_match_value and 'both') or
                      (surface_match_value and 'surface') or
                      (subsurface_match_value and 'SUBsurface'))

        single_item_report = {
            'has_match': bool(surface_match_row or subsurface_match_row),
            'matched_both': bool(surface_match_row and subsurface_match_row),
            'match_type': match_type,
            'secdivid_from_sd_server': secdivid_from_sd_server,
            'surface_match_value': surface_match_value,
            'surface_match_row': surface_match_row,
            'surface_source_data': str(surface_parcels_path),
            'subsurface_match_value': subsurface_match_value,
            'subsurface_match_row': subsurface_match_row,
            'subsurface_source_data': str(subsurface_parcels_path),
        }

        match_reports.append(single_item_report)

    # matched
    out_dir = Path('data/csv/out').resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(data=match_reports).to_csv(out_dir / 'match_report.csv', index=False)

    # unmatched
    unmatched_surface_items = set(surface_secdivids) - set(matched_surface_items)
    unmatch_surface_df = pd.DataFrame(data=[{'type': 'surface', 'secdivid': s} for s in unmatched_surface_items])
    unmatch_surface_df.to_csv(out_dir / 'unmatch_surface.csv', index=False)

    unmatched_subsurface_items = set(subsurface_secdivids) - set(matched_subsurface_items)
    unmatch_subsurface_df = pd.DataFrame(data=[{'type': 'subsurface', 'secdivid': s} for s in unmatched_subsurface_items])
    unmatch_subsurface_df.to_csv(out_dir / 'unmatch_subsurface.csv', index=False)


if __name__ == '__main__':
    main()
