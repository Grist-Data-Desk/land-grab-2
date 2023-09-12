from tasks.to_be_moved.land_grab.university_real_estate.parcel_list_parsers.mo_universityofmissouri_parser import moum_parser


def test_handles_all_weird_cases_of_parcel_number_column():
    normal = '30-810-18-04-00-0-00-000'
    normal_out = '30810180400000000'

    case_1 = '8121 Evarts: 14H430334 & 8112 Oxeye: 14H431021'
    case_1_out = ['14H430334', '14H431021']

    case_2 = '71-09-1.0-02-004-019-001.000 (07280.00)'
    case_2_out = ['71091002004019001000', '0728000']

    case_3 = '30-810-13-05-00-0-00-000;143427 (City), JA30810130500000000 (County); Resurvey of Mulkey Park'
    case_4 = '125285 (City); JA29540160100000000 (County)'
    case_3_out = ['30810130500000000', '143427 (City), JA30810130500000000 (County); Resurvey of Mulkey Park']
    case_4_out = ['29540160100000000', '125285 (City); JA29540160100000000 (County)']

    case_5 = '25-400-20-00-002.00 (part of this parcel - NW to Hwy Y, south to edge, west to edge)'
    case_6 = '16-608-00-04-001.00.01 (50x260 = 0.3 acres); west half of this parcel'
    case_5_out = ['25400200000200', '(part of this parcel - NW to Hwy Y, south to edge, west to edge)']
    case_6_out = ['1660800040010001', '(50x260 = 0.3 acres); west half of this parcel']

    case_7 = '16-501-00-02-037.00 01 & 16-501-00-02-037.02 01'
    case_7_out = ['1650100020370001', '1650100020370201']

    case_8 = '14H431957 - Florissant Road; 14H431063 - 4122 Lowen Drive'
    case_8_out = ['14H431957', '14H431063']

    case_9 = '$5,000 for 10 acres in T21N R13E S31; $3,500 for 10 acres in T20N, R13E S11'
    case_9_out = ['$5,000 for 10 acres in T21N R13E S31', '$3,500 for 10 acres in T20N, R13E S11']

    for i, (input_s, output) in enumerate(
            [(normal, normal_out), (case_1, case_1_out), (case_2, case_2_out), (case_3, case_3_out),
             (case_4, case_4_out),
             (case_5, case_5_out), (case_6, case_6_out), (case_7, case_7_out), (case_8, case_8_out),
             (case_9, case_9_out)]
    ):
        row = [None] * 10
        row[7] = input_s
        result = moum_parser(row)
        assert result == output
