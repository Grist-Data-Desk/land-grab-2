import re
from typing import List, Union

from land_grab_2.uni_holdings_dataset.also_old_stuff_figure_out.parcel_enrichment.entities import Parcel


def basic_clean(parcel_number) -> str:
    if '-' in parcel_number:
        parcel_number = ''.join(parcel_number.split('-'))

    if '.' in parcel_number:
        parcel_number = ''.join(parcel_number.split('.'))

    if ' ' in parcel_number:
        parcel_number = ''.join(parcel_number.split(' '))

    return parcel_number


def parse_case_1(case_1) -> List[str]:
    # case_1 = '8121 Evarts: 14H430334 & 8112 Oxeye: 14H431021'
    try:
        parts = case_1.split('&')
        colon_parts = [p.split(':') for p in parts]
        pids = [p[-1].strip() for p in colon_parts]
        return pids
    except:
        pass


def parse_case_2(case_2) -> List[str]:
    # case_2 = '71-09-1.0-02-004-019-001.000 (07280.00)'
    try:
        clean_pids = []
        first, second = case_2.split('(')
        clean_pids.append(basic_clean(first))
        second_group = basic_clean(second.replace(')', ''))

        if second_group and all(d.isdigit() for d in second_group):
            clean_pids.append(second_group)
        return clean_pids
    except:
        pass


def parse_case_3(case_3) -> List[str]:
    # '30-810-13-05-00-0-00-000;143427 (City), JA30810130500000000 (County); Resurvey of Mulkey Park'
    # '125285 (City); JA29540160100000000 (County)'
    try:
        if 'City' in case_3 and 'County' in case_3:
            pids = []

            city_idx = case_3.find('City')
            county_idx = case_3.find('County')
            pid_region = case_3[city_idx:county_idx]
            pid_region_parts = pid_region.split(' ')
            if pid_region_parts:
                pid_with_county_code = list(sorted(pid_region_parts, key=len, reverse=True))[0]
                pid_start = next((i for i, c in enumerate(pid_with_county_code) if c.isdigit()), None)
                pid = pid_with_county_code[pid_start:]
                pids.append(pid)

            beginning_half = case_3[:city_idx]
            if ';' in beginning_half:
                delim_idx = beginning_half.find(';')
                clean_extra_info = case_3[delim_idx + 1:]
                pids.append(clean_extra_info)
            else:
                pids.append(case_3)

            return pids
    except:
        pass


def parse_case_4(case_4) -> List[str]:
    # '25-400-20-00-002.00 (part of this parcel - NW to Hwy Y, south to edge, west to edge)'
    # '16-608-00-04-001.00.01 (50x260 = 0.3 acres); west half of this parcel'
    try:
        pids = []
        if 'parcel' in case_4 and '(' in case_4:
            first_paren = case_4.find('(')
            pid = basic_clean(case_4[:first_paren])
            pids.append(pid)

            remainder = case_4[first_paren:]
            pids.append(remainder)
            return pids
    except:
        pass


def parse_case_5(case_7) -> List[str]:
    # '16-501-00-02-037.00 01 & 16-501-00-02-037.02 01'
    try:
        pids = [basic_clean(p) for p in case_7.split('&')]
        return pids
    except:
        pass


def parse_case_6(case_6) -> List[str]:
    # '14H431957 - Florissant Road; 14H431063 - 4122 Lowen Drive'

    try:
        if '-' in case_6 and ';' in case_6:
            parts = case_6.split(';')
            pids = []
            for p in parts:
                bwd_p = ''.join(reversed(p))
                hyphen_idx = bwd_p.find('-')
                bwd_p_with_pid = bwd_p[hyphen_idx:]
                pid = basic_clean(''.join(reversed(bwd_p_with_pid)))
                pids.append(pid)
            return pids
    except:
        pass


def parse_case_7(case_7) -> List[str]:
    #  '$5,000 for 10 acres in T21N R13E S31; $3,500 for 10 acres in T20N, R13E S11'
    try:
        regexp = re.compile(r'for\s+\d+\s+acres\s+in')
        if regexp.search(case_7):
            parts = [p.strip() for p in case_7.split(';')]
            return parts
    except:
        pass


def has_words(s) -> bool:
    def is_word(w) -> bool:
        letters = [1 for c in w if c.isalpha()]
        word_classification_threshold = 0.75
        percent_letters = len(letters) / len(w)
        return percent_letters >= word_classification_threshold

    return any(is_word(w) for w in s.split())


def pidlist_to_parcels(parcel: Parcel, pids: List[str]) -> List[Parcel]:
    parcels = []
    for p in pids:
        p_clone = Parcel(**parcel.to_dict())
        p_clone.normalized_number = p
        parcels.append(p_clone)

    return parcels


def moum_parser(l) -> Union[List[Parcel], Parcel]:
    parcel_number = l[7]
    p = Parcel(original_number=parcel_number, county=l[5])

    if not (has_words(parcel_number) or any(c in parcel_number for c in [';', '(', ')', '&'])):
        clean_number = basic_clean(parcel_number)
        p.normalized_number = clean_number
        return p

    if not has_words(parcel_number) and any(c in parcel_number for c in ['(', ')']):
        pids = parse_case_2(parcel_number)
        return pidlist_to_parcels(p, pids)

    if not has_words(parcel_number) and any(c in parcel_number for c in [';', '&']):
        pids = parse_case_5(parcel_number)
        return pidlist_to_parcels(p, pids)

    if 'City' in parcel_number and 'County' in parcel_number:
        pids = parse_case_3(parcel_number)
        return pidlist_to_parcels(p, pids)

    if all(c in parcel_number for c in [':', '&']):
        pids = parse_case_1(parcel_number)
        return pidlist_to_parcels(p, pids)

    case_7_result = parse_case_7(parcel_number)
    case_4_result = parse_case_4(parcel_number)
    case_6_result = parse_case_6(parcel_number)

    all_results = [
        case_7_result, case_4_result, case_6_result
    ]

    pids = next((r for r in all_results if r), None)
    return pidlist_to_parcels(p, pids)
