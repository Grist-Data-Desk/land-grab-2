from constants import (
    DOWNLOAD_TYPE, API_QUERY_DOWNLOAD_TYPE, SHAPEFILE_DOWNLOAD_TYPE, STATE,
    UNIVERSITY, MANAGING_AGENCY, DATA_SOURCE, LOCAL_DATA_SOURCE,
    ATTRIBUTE_LABEL_TO_FILTER_BY, ATTRIBUTE_CODE_TO_ALIAS_MAP, RIGHTS_TYPE,
    SURFACE_RIGHTS_TYPE, SUBSURFACE_RIGHTS_TYPE, TIMBER_RIGHTS_TYPE, LAYER,
    STATE_TRUST_DATA_SOURCE_DIRECTORY, EXISTING_COLUMN_TO_FINAL_COLUMN_MAP,
    ACRES, COUNTY, MERIDIAN, TOWNSHIP, RANGE, SECTION, ALIQUOT, BLOCK, ACTIVITY)

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
    # 'IA': {
    #     DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
    #     STATE: 'IA',
    #     UNIVERSITY: 'University of Idaho',
    #     MANAGING_AGENCY: 'Department of Lands',
    #     DATA_SOURCE:
    #     'https://programs.iowadnr.gov/geospatial/rest/services/Boundaries/Public_Lands/MapServer/0',
    #     # 'https://programs.iowadnr.gov/geospatial/rest/services/Boundaries/Public_Lands_ESRI/MapServer/0',
    #     # ATTRIBUTE_LABEL_TO_FILTER_BY: ['OWNER'],
    #     # ATTRIBUTE_CODE_TO_ALIAS_MAP: {
    #     #     "'Iowa State University'": 'Iowa State University'
    #     # },
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: ['MANAGER'],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {
    #         "'DNR - Wildlife'": 'DNR - Wildlife'
    #     },
    #     # ATTRIBUTE_LABEL_TO_FILTER_BY: [],
    #     # ATTRIBUTE_CODE_TO_ALIAS_MAP: {},
    # },
    'ID-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'ID',
        UNIVERSITY: 'University of Idaho',
        MANAGING_AGENCY: 'Department of Lands',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
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
    # 'MI': {
    #     DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
    #     STATE: 'IA',
    #     UNIVERSITY: 'University of Idaho',
    #     MANAGING_AGENCY: 'Department of Lands',
    #     DATA_SOURCE:
    #     'https://services3.arcgis.com/Jdnp1TjADvSDxMAX/ArcGIS/rest/services/dnrRealEstate/FeatureServer/2',
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: ['Beneficiary'],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {
    #         "'Colorado State University'": 'Colorado State University'
    #     },
    #     # ATTRIBUTE_LABEL_TO_FILTER_BY: [],
    #     # ATTRIBUTE_CODE_TO_ALIAS_MAP: {},
    # },
    'MN': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'MN',
        UNIVERSITY: 'University of Minnesota',
        MANAGING_AGENCY: 'Department of Natural Resources',
        LOCAL_DATA_SOURCE:
        STATE_TRUST_DATA_SOURCE_DIRECTORY + 'shp_plan_stateland_dnrcounty.zip',
        DATA_SOURCE:
        'https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_dnr/plan_stateland_dnrcounty/shp_plan_stateland_dnrcounty.zip',
        LAYER: 'stateland_type_trust',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['LANDTYPECO'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '5': 'Trust Fund: University (University Trust)',
        },
        EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
            'SU_ACRES': ACRES,
            'COUNTYNAME': COUNTY,
            'TOWN': TOWNSHIP,
            'RANG': RANGE,
            'SECT': SECTION,
        },
    },
    'MT-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'MT',
        UNIVERSITY: 'Montana State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
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
            'COUNTYNAME': COUNTY,
            'TOWN': TOWNSHIP,
            'RANG': RANGE,
            'SECT': SECTION,
        },
    },
    # TODO: add montana subsurface from 3 shapefiles
    # 'MT-subsurface': {
    #     DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
    #     STATE: 'MT',
    #     UNIVERSITY: 'Montana State University',
    #     MANAGING_AGENCY: 'Department of Natural Resources',
    #     RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
    #     DATA_SOURCE:
    #     'https://gis.dnrc.mt.gov/arcgis/rest/services/DNRALL/BasemapService/MapServer/31',
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: ['GrantID'],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {
    #         "'ACI'": 'MSU Morrill',
    #         "'ACB'": 'MSU 2nd Grant',
    #         "'SNS'": 'State Normal School'
    #     },
    #     EXISTING_COLUMN_TO_FINAL_COLUMN_MAP: {
    #         'Acres': ACRES,
    #         'COUNTY1': COUNTY,
    #         'LegalDesc': ALIQUOT,
    #     },
    # },
    'ND-surface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'ND',
        UNIVERSITY: 'North Dakota State University',
        MANAGING_AGENCY: 'Commissioner of University and School Lands',
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
    # TODO: check for duplicate parcels, and check for OK parcels with oregon state university label.
    'OK-surface': {
        # for oklahoma's real estate (surface) lease holdings, we query the API below, but the API does not
        # contain information on which trust fund the land belongs to. The CLO gavbe us a list of which
        # parcels, by HoldingDetailID, map to different funds which is not publicly available, so we
        # create a custom filter here.
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'OK',
        UNIVERSITY: 'Oklahoma State University',
        MANAGING_AGENCY: 'Commissioners of the Land Office',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
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
    # TODO: add STRM?
    'OK-subsurface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'OK',
        UNIVERSITY: 'Oklahoma State University',
        MANAGING_AGENCY: 'Commissioners of the Land Office',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
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
    'TX': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'TX',
        UNIVERSITY: 'Texas A&M',
        MANAGING_AGENCY: 'General Land Office',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE + '+' + SUBSURFACE_RIGHTS_TYPE,
        # found at https://universitylands.utsystem.edu/Resources/GIS
        DATA_SOURCE:
        'https://gisapps.universitylands.org/server/rest/services/Hosted/GrantTracts_SpatialJoin/FeatureServer/16',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['id'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "*": None
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
    'WA-surface': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'WA',
        UNIVERSITY: 'Washington State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
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
        DATA_SOURCE:
        'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['MINERAL_TRUST_CD'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            4: 'Agricultural School',
            10: 'Scientific School',
        },
    },
    'WA-timber': {
        DOWNLOAD_TYPE: API_QUERY_DOWNLOAD_TYPE,
        STATE: 'WA',
        UNIVERSITY: 'Washington State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: TIMBER_RIGHTS_TYPE,
        DATA_SOURCE:
        'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['TIMBER_TRUST_CD'],
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