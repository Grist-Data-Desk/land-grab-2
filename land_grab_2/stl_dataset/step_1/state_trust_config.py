from land_grab_2.stl_dataset.step_1.constants import (
    DOWNLOAD_TYPE, API_QUERY_DOWNLOAD_TYPE, SHAPEFILE_DOWNLOAD_TYPE, STATE,
    UNIVERSITY, MANAGING_AGENCY, DATA_SOURCE, LOCAL_DATA_SOURCE,
    ATTRIBUTE_LABEL_TO_FILTER_BY, ATTRIBUTE_CODE_TO_ALIAS_MAP, RIGHTS_TYPE,
    SURFACE_RIGHTS_TYPE, SUBSURFACE_RIGHTS_TYPE, TIMBER_RIGHTS_TYPE, LAYER,
    STATE_TRUST_DATA_SOURCE_DIRECTORY, EXISTING_COLUMN_TO_FINAL_COLUMN_MAP,
    ACRES, COUNTY, MERIDIAN, TOWNSHIP, RANGE, SECTION, ALIQUOT, BLOCK, ACTIVITY,
    STATE_ENABLING_ACT)

STATE_TRUST_CONFIGS = {
    # 'AL': {
    #     DATA_SOURCE:
    #     'https://conservationgis.alabama.gov/adcnrweb/rest/services/StateLands/MapServer/0',
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: [],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {},
    # },
    'AZ-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'AZ',
        UNIVERSITY: 'University of Arizona',
        MANAGING_AGENCY: 'State Land Department',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '36 Stat. 557-579 (1910)',
        DATA_SOURCE:
            'https://server.azgeo.az.gov/arcgis/rest/services/azland/State_Trust_Parcels/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['fundtxt'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'UNIVERSITY'": 'UNIVERSITY',
            "'UNIV OF ARIZ (ACT 2/18/1881)'": 'UNIV OF ARIZ (ACT 2.18.1881)',
            "'AGRICULTURE & MECHANICAL CLLGE'":
                'AGRICULTURE & MECHANICAL COLLEGE',
            "'SCHOOL OF MINES'": 'SCHOOL OF MINES',
            "'MILITARY INSTITUTES'": 'MILITARY INSTITUTES',
            "'NORMAL SCHOOL'": 'NORMAL SCHOOL',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'acres': ACRES,
            'County': COUNTY,
        },
    },
    'AZ-subsurface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'AZ',
        UNIVERSITY: 'University of Arizona',
        MANAGING_AGENCY: 'State Land Department',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '36 Stat. 557-579 (1910)',
        DATA_SOURCE:
            'https://server.azgeo.az.gov/arcgis/rest/services/azland/Mineral_Parcels/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['fundtxt'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'UNIVERSITY'": 'UNIVERSITY',
            "'UNIV OF ARIZ (ACT 2/18/1881)'": 'UNIV OF ARIZ (ACT 2.18.1881)',
            "'AGRICULTURE & MECHANICAL CLLGE'":
                'AGRICULTURE & MECHANICAL COLLEGE',
            "'SCHOOL OF MINES'": 'SCHOOL OF MINES',
            "'MILITARY INSTITUTES'": 'MILITARY INSTITUTES',
            "'NORMAL SCHOOL'": 'NORMAL SCHOOL',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'acres': ACRES,
            'County': COUNTY,
        },
    },
    'CO-surface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'CO',
        UNIVERSITY: 'Colorado State University',
        MANAGING_AGENCY: 'State Land Board',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '18 Stat. 474-476',
        LOCAL_DATA_SOURCE: STATE_TRUST_DATA_SOURCE_DIRECTORY + 'CO',
        LAYER: 'SLB_Surface_University_Beneficiary',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Beneficiar'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            'Colorado State University': 'Colorado State University'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'Acreage': ACRES,
            'County': COUNTY,
            'Township': TOWNSHIP,
            'Range': RANGE,
            'Section': SECTION,
            'Meridian': MERIDIAN,
        },
    },
    'CO-subsurface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'CO',
        UNIVERSITY: 'Colorado State University',
        MANAGING_AGENCY: 'State Land Board',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '18 Stat. 474-476',
        LOCAL_DATA_SOURCE: STATE_TRUST_DATA_SOURCE_DIRECTORY + 'CO',
        LAYER: 'SLB_Minerals_University_Beneficiary',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Beneficiar'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            'Colorado State University': 'Colorado State University'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'Acreage': ACRES,
            'County': COUNTY,
            'Township': TOWNSHIP,
            'Range': RANGE,
            'Section': SECTION,
            'Meridian': MERIDIAN,
            'Asset_Laye': ACTIVITY,
        },
    },
    'ID-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'ID',
        UNIVERSITY: 'University of Idaho',
        MANAGING_AGENCY: 'Department of Lands',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '26 Stat. 215-219 (1890)',
        DATA_SOURCE:
            'https://gis1.idl.idaho.gov/arcgis/rest/services/State_Ownership/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['SURF_ENDOWMENT'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            2: '100.00% Agricultural College',
            6: '100.00% School of Science (Scientific School)',
            921: 'Split - AC and F.&G.',
            927: 'Split - SS and F.&G.',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'L_ACRES': ACRES,
        },
    },
    'ID-subsurface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'ID',
        UNIVERSITY: 'University of Idaho',
        MANAGING_AGENCY: 'Department of Lands',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '26 Stat. 215-219 (1890)',
        DATA_SOURCE:
            'https://gis1.idl.idaho.gov/arcgis/rest/services/State_Ownership/MapServer/1',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['SUB_ENDOWMENT'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            2: '100.00% Agricultural College',
            6: '100.00% School of Science (Scientific School)',
            921: 'Split - AC and F.&G.',
            927: 'Split - SS and F.&G.',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'L_ACRES': ACRES,
        },
    },
    'MN-surface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'MN',
        UNIVERSITY: 'University of Minnesota',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '11 Stat. 166-167 (1857); 11 Stat. 285 (1858)',
        LOCAL_DATA_SOURCE:
            STATE_TRUST_DATA_SOURCE_DIRECTORY + 'shp_plan_stateland_dnrcounty.zip',
        DATA_SOURCE:
            'https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_dnr/plan_stateland_dnrcounty/shp_plan_stateland_dnrcounty.zip',
        LAYER: 'stateland_type_trust',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['LANDTYPECO'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '5': 'University',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'SU_ACRES': ACRES,
            'COUNTYNAME': COUNTY,
            'TOWN': TOWNSHIP,
            'RANG': RANGE,
            'SECT': SECTION,
            'FORTDESC': ALIQUOT,
        },
    },
    'MN-subsurface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'MN',
        UNIVERSITY: 'University of Minnesota',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '11 Stat. 166-167 (1857); 11 Stat. 285 (1858)',
        LOCAL_DATA_SOURCE:
            STATE_TRUST_DATA_SOURCE_DIRECTORY + 'MN_UnivTrustMins-20230621',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['LANDTYPECO'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '5': 'University',
            '6': 'Transferred University',
            '8': 'Agricultural College',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'SU_ACRES': ACRES,
            'COUNTYNAME': COUNTY,
            'TOWN': TOWNSHIP,
            'RANG': RANGE,
            'SECT': SECTION,
            'FORTDESC': ALIQUOT,
        },
    },
    'MT-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'MT',
        UNIVERSITY: 'Montana State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        DATA_SOURCE:
            'https://gis.dnrc.mt.gov/arcgis/rest/services/DNRALL/BasemapService/MapServer/31',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['GrantID'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'ACI'": 'MSU Morrill',
            "'ACB'": 'MSU 2nd Grant',
            "'SNS'": 'State Normal School'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'Acres': ACRES,
        },
    },
    'MT-subsurface-coal': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'MT',
        UNIVERSITY: 'Montana State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        LOCAL_DATA_SOURCE: STATE_TRUST_DATA_SOURCE_DIRECTORY + 'MT-coal',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['GrantID'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            'ACI': 'MSU Morrill',
            'ACB': 'MSU 2nd Grant',
            'SNS': 'State Normal School'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'Acres': ACRES,
            'COUNTY1': COUNTY,
            'LegalDesc': ALIQUOT,
            'Activity': ACTIVITY,
        },
    },
    'MT-subsurface-oil-and-gas': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'MT',
        UNIVERSITY: 'Montana State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        LOCAL_DATA_SOURCE: STATE_TRUST_DATA_SOURCE_DIRECTORY + 'MT-oil-and-gas',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['GrantID'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            'ACI': 'MSU Morrill',
            'ACB': 'MSU 2nd Grant',
            'SNS': 'State Normal School'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'Acres': ACRES,
            'COUNTY1': COUNTY,
            'LegalDesc': ALIQUOT,
            'Activity': ACTIVITY,
        },
    },
    'MT-subsurface-other-minerals': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'MT',
        UNIVERSITY: 'Montana State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        LOCAL_DATA_SOURCE:
            STATE_TRUST_DATA_SOURCE_DIRECTORY + 'MT-other-minerals',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['GrantID'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            'ACI': 'MSU Morrill',
            'ACB': 'MSU 2nd Grant',
            'SNS': 'State Normal School'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'Acres': ACRES,
            'COUNTY1': COUNTY,
            'LegalDesc': ALIQUOT,
            'Activity': ACTIVITY,
        },
    },
    'ND-surface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'ND',
        UNIVERSITY: 'North Dakota State University',
        MANAGING_AGENCY: 'Commissioner of University and School Lands',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        LOCAL_DATA_SOURCE: STATE_TRUST_DATA_SOURCE_DIRECTORY +
                           'Surface_Trust_Lands_with_Trusts.zip',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Trust_Desc'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            'ND STATE UNIVERSITY': 'North Dakota State University',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'ACRES': ACRES,
            'COUNTY': COUNTY,
            'TOWNSHIP': TOWNSHIP,
            'RANGE': RANGE,
            'SECTION': SECTION,
            'SUBDIVISIO': ALIQUOT,
        },
    },
    'ND-subsurface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'ND',
        UNIVERSITY: 'North Dakota State University',
        MANAGING_AGENCY: 'Commissioner of University and School Lands',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        DATA_SOURCE:
            'https://ndgishub.nd.gov/arcgis/rest/services/All_GovtLands_State/MapServer/2',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['TRUST'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'N'": 'North Dakota State University'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'GROSS_ACRES': ACRES,
            'COUNTY': COUNTY,
            'TWP': TOWNSHIP,
            'RNG': RANGE,
            'SEC': SECTION,
            'SUBDIVISION': ALIQUOT,
        },
    },
    'NE': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'NE',
        UNIVERSITY: 'University of Nebraska',
        MANAGING_AGENCY: 'Board of Educational Lands and Funds',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        LOCAL_DATA_SOURCE:
            STATE_TRUST_DATA_SOURCE_DIRECTORY + '2023_Nebraska_BELF_lands.zip',
        LAYER: '233103 BELF trust lands',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Fund_Desc'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            'University': 'University',
            'AG College': 'AG College',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'County': COUNTY,
        },
    },
    'NM-surface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'NM',
        UNIVERSITY: 'New Mexico State University',
        MANAGING_AGENCY: 'State Land Office',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '36 Stat. 557-579 , esp. 572-573 (1910)',
        LOCAL_DATA_SOURCE:
            STATE_TRUST_DATA_SOURCE_DIRECTORY + 'slo_STLStatusCombined.zip',
        DATA_SOURCE:
            'https://mapservice.nmstatelands.org/GISDataDownloads/ZipFiles/slo_STLStatusCombined.zip',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Benef_Surf'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '04': 'New Mexico State University',
            '28': 'New Mexico State University',
            '42': 'New Mexico State University',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'Acres_Surf': ACRES,
            'County': COUNTY,
            'Township': TOWNSHIP,
            'Range': RANGE,
            'Section': SECTION,
            'Meridian': MERIDIAN,
            'Aliquot': ALIQUOT,
        },
    },
    'NM-subsurface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'NM',
        UNIVERSITY: 'New Mexico State University',
        MANAGING_AGENCY: 'State Land Office',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '36 Stat. 557-579 , esp. 572-573 (1910)',
        LOCAL_DATA_SOURCE:
            STATE_TRUST_DATA_SOURCE_DIRECTORY + 'slo_STLStatusCombined.zip',
        DATA_SOURCE:
            'https://mapservice.nmstatelands.org/GISDataDownloads/ZipFiles/slo_STLStatusCombined.zip',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Benef_SubS'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '04': 'New Mexico State University',
            '28': 'New Mexico State University',
            '42': 'New Mexico State University',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'Acres_SubS': ACRES,
            'County': COUNTY,
            'Township': TOWNSHIP,
            'Range': RANGE,
            'Section': SECTION,
            'Meridian': MERIDIAN,
            'Aliquot': ALIQUOT,
        },
    },
    'OK-unleased-mineral-lands': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'OK',
        UNIVERSITY: 'Oklahoma State University',
        MANAGING_AGENCY: 'Commissioners of the Land Office',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        # RIGHTS_TYPE: 'Unleased Mineral Lands',
        STATE_ENABLING_ACT: '34. Stat. 267-286 , esp. 272, 274-75 (1906)',
        DATA_SOURCE:
            'https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/10',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['*'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "*": 'All'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'TotalAllAcreage': ACRES,
            'CountyName': COUNTY,
            'Section': SECTION,
            'Meridian': MERIDIAN,
            'QuarterDescription': ALIQUOT,
        },
    },
    'OK-real-estate-subdivs': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'OK',
        UNIVERSITY: 'Oklahoma State University',
        MANAGING_AGENCY: 'Commissioners of the Land Office',
        # RIGHTS_TYPE: 'Real Estate Subdivisions',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '34. Stat. 267-286 , esp. 272, 274-75 (1906)',
        DATA_SOURCE:
            'https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/2',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['*'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "*": 'All'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'TotalAllAcreage': ACRES,
            'CountyName': COUNTY,
            'Section': SECTION,
            'Meridian': MERIDIAN,
            'QuarterDescription': ALIQUOT,
        },
    },
    'OK-mineral-subdivs': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'OK',
        UNIVERSITY: 'Oklahoma State University',
        MANAGING_AGENCY: 'Commissioners of the Land Office',
        # RIGHTS_TYPE: 'Mineral Subdivisions',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '34. Stat. 267-286 , esp. 272, 274-75 (1906)',
        DATA_SOURCE:
            'https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/3',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['*'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "*": 'All'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'TotalAllAcreage': ACRES,
            'CountyName': COUNTY,
            'Section': SECTION,
            'Meridian': MERIDIAN,
            'QuarterDescription': ALIQUOT,
        },
    },
    'OK-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'OK',
        UNIVERSITY: 'Oklahoma State University',
        MANAGING_AGENCY: 'Commissioners of the Land Office',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '34. Stat. 267-286 , esp. 272, 274-75 (1906)',
        DATA_SOURCE:
            'https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/2',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['*'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "*": 'All'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'TotalAllAcreage': ACRES,
            'CountyName': COUNTY,
            'Section': SECTION,
            'Meridian': MERIDIAN,
            'QuarterDescription': ALIQUOT,
        },
    },
    'OK-subsurface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'OK',
        UNIVERSITY: 'Oklahoma State University',
        MANAGING_AGENCY: 'Commissioners of the Land Office',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '34. Stat. 267-286 , esp. 272, 274-75 (1906)',
        DATA_SOURCE:
            'https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/1',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['TrustName'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'Oklahoma State University'": 'Oklahoma State University'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'NetAcres': ACRES,
            'CountyName': COUNTY,
            # 'LegalDescription': ALIQUOT,
        },
    },
    'SD': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'SD',
        UNIVERSITY: 'South Dakota State University',
        MANAGING_AGENCY: 'Commissioner of School and Public Lands',
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        LOCAL_DATA_SOURCE: STATE_TRUST_DATA_SOURCE_DIRECTORY + 'SD',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['*'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "*": 'South Dakota State University'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'RECRDAREAN': ACRES,
            'QQSEC': ALIQUOT,
        },
    },
    # 'TX': {
    #     DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
    #     STATE: 'TX',
    #     UNIVERSITY: 'Texas A&M',
    #     MANAGING_AGENCY: 'General Land Office',
    #     RIGHTS_TYPE: SURFACE_RIGHTS_TYPE + '+' + SUBSURFACE_RIGHTS_TYPE,
    #     # found at https://universitylands.utsystem.edu/Resources/GIS
    #     DATA_SOURCE:
    #     'https://gisapps.universitylands.org/server/rest/services/Hosted/GrantTracts_SpatialJoin/FeatureServer/16',
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: ['tractid'],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {
    #         "*": None
    #     },
    #     EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
    #         'acres': ACRES,
    #         'countyname': COUNTY,
    #         'section': SECTION,
    #         'block': BLOCK,
    #     },
    # },
    'TX-surface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'TX',
        UNIVERSITY: 'Texas A&M',
        MANAGING_AGENCY: 'General Land Office',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        LOCAL_DATA_SOURCE: STATE_TRUST_DATA_SOURCE_DIRECTORY + 'TX',
        # found at https://universitylands.utsystem.edu/Resources/GIS
        DATA_SOURCE:
            'https://gisapps.universitylands.org/server/rest/services/Hosted/GrantTracts_SpatialJoin/FeatureServer/16',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['hassurface'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            1: 'Texas A&M'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'acres': ACRES,
            'countyname': COUNTY,
            'section': SECTION,
            'block': BLOCK,
        },
    },
    'TX-subsurface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'TX',
        UNIVERSITY: 'Texas A&M',
        MANAGING_AGENCY: 'General Land Office',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        LOCAL_DATA_SOURCE: STATE_TRUST_DATA_SOURCE_DIRECTORY + 'TX',
        # found at https://universitylands.utsystem.edu/Resources/GIS
        DATA_SOURCE:
            'https://gisapps.universitylands.org/server/rest/services/Hosted/GrantTracts_SpatialJoin/FeatureServer/16',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['hasmineral'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            1: 'Texas A&M'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'acres': ACRES,
            'countyname': COUNTY,
            'section': SECTION,
            'block': BLOCK,
        },
    },
    'UT-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'UT',
        UNIVERSITY: 'Utah State University',
        MANAGING_AGENCY: 'Trust Lands Administration',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '28 Stat. 107-110 (1894)',
        DATA_SOURCE:
            'https://gis.trustlands.utah.gov/server/rest/services/Ownership/UT_SITLA_Ownership_Beneficiary/MapServer/1',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['bene_abrev'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'USU'": 'Utah State University',
            "'NS'": 'Normal School',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'acres': ACRES,
        },
    },
    'UT-subsurface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'UT',
        UNIVERSITY: 'Utah State University',
        MANAGING_AGENCY: 'Trust Lands Administration',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '28 Stat. 107-110 (1894)',
        DATA_SOURCE:
            'https://gis.trustlands.utah.gov/server/rest/services/Ownership/UT_SITLA_Ownership_Beneficiary/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['bene_abrev'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'USU'": 'Utah State University',
            "'NS'": 'Normal School',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'acres': ACRES,
        },
    },
    'WA-timber': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'WA',
        UNIVERSITY: 'Washington State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        ACTIVITY: 'timber',
        DATA_SOURCE:
            'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['TIMBER_TRUST_CD'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            4: 'Agricultural School',
            10: 'Scientific School',
        },
    },
    'WA-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'WA',
        UNIVERSITY: 'Washington State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        DATA_SOURCE:
            'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['SURFACE_TRUST_CD'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            4: 'Agricultural School',
            10: 'Scientific School',
        },
    },
    'WA-subsurface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'WA',
        UNIVERSITY: 'Washington State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '25 Stat. 676-684, esp. 679-81 (1889)',
        DATA_SOURCE:
            'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['MINERAL_TRUST_CD'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            4: 'Agricultural School',
            10: 'Scientific School',
        },
    },
    'WI': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'WI',
        UNIVERSITY: 'University of Wisconsin',
        MANAGING_AGENCY: 'Board of Commissioners of Public Lands',
        STATE_ENABLING_ACT: '9 Stat.  56-58 (1846)',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        LOCAL_DATA_SOURCE:
            STATE_TRUST_DATA_SOURCE_DIRECTORY + 'BCPLShapeFIleforWeb',
        DATA_SOURCE:
            'https://bcpl.wisconsin.gov/bcpl.wisconsin.gov%20Shared%20Documents/Maps/BCPLPropertyBoundariesShapefile.zip',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['FUND'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '744': 'Common School',
            '745': 'Normal School',
            '746': 'University or Ag College',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'GLOACRES': ACRES,
            'COUNTY_NAM': COUNTY,
        },
    },
    'WY-subsurface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'WY',
        UNIVERSITY: 'University of Wyoming',
        MANAGING_AGENCY: 'Board of Commissioners of Public Lands',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '26 Stat. 222-226 (1890)',
        DATA_SOURCE:
            'https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/19',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['FundCode'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'UN'": 'University Land (trust)',
            "'AG'": 'Agricultural College',
            # "'UW'": 'University of Wyoming (acquired)'
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'SurfaceAcres': ACRES,
            'Township_Temp': TOWNSHIP,
            'Range_Temp': RANGE,
            'FirstDivision_Temp': SECTION,
        },
    },
    'WY-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'WY',
        UNIVERSITY: 'University of Wyoming',
        MANAGING_AGENCY: 'Board of Commissioners of Public Lands',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        STATE_ENABLING_ACT: '26 Stat. 222-226 (1890)',
        DATA_SOURCE:
            'https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/18',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['FundCode'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'UN'": 'University Land (trust)',
            "'AG'": 'Agricultural College',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'SurfaceAcres': ACRES,
            'Township_Temp': TOWNSHIP,
            'Range_Temp': RANGE,
            'FirstDivision_Temp': SECTION,
        },
    },
}
