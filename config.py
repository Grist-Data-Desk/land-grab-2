STATE = 'state'
UNIVERSITY = 'university'
MANAGING_AGENCY = 'managing_agency'
RIGHTS_TYPE = 'rights_type'
GEOMETRY = 'geometry'
ATTRIBUTE_FILTER = 'attribute_filter'
SURFACE_RIGHTS_TYPE = 'surface'
SUBSURFACE_RIGHTS_TYPE = 'subsurface'
DOWNLOAD_TYPE = 'download_type'
API_QUERY_DOWNLOAD_TYPE = 'api_query'
SHAPEFILE_DOWNLOAD_TYPE = 'shapefile'
URL = 'url'
LAYER = 'layer'
ATTRIBUTE_LABEL_TO_FILTER_BY = 'attribute_label_to_filter_by'
SURFACE_ATTRIBUTE_LABEL_TO_FILTER_BY = 'surface_attribute_label_to_filter_by'
SUBSURFACE_ATTRIBUTE_LABEL_TO_FILTER_BY = 'subsurface_attribute_label_to_filter_by'
ATTRIBUTE_CODE_TO_ALIAS_MAP = 'attribute_code_to_alias_map'

COLUMNS = [
    STATE, UNIVERSITY, MANAGING_AGENCY, RIGHTS_TYPE, ATTRIBUTE_FILTER, GEOMETRY
]

CONFIGS = {
    # 'AL': {
    #     URL:
    #     'https://conservationgis.alabama.gov/adcnrweb/rest/services/StateLands/MapServer/0',
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: [],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {},
    # },
    'AZ': {
        STATE: 'AZ',
        UNIVERSITY: 'University of Arizona',
        MANAGING_AGENCY: 'State Land Department',
        URL:
        'https://server.azgeo.az.gov/arcgis/rest/services/azland/State_Trust_Parcels/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['fundtxt'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'UNIVERSITY'": 'UNIVERSITY',
            "'UNIV OF ARIZ (ACT 2/18/1881)'": 'UNIV OF ARIZ (ACT 2.18.1881)'
        },
    },
    # TODO: do we want to use this source?
    # 'CO-trustland-leases': {
    #     URL:
    #     'https://services5.arcgis.com/rqsYvPKZmvSrSWbw/ArcGIS/rest/services/SLB_Leases_ALL_Trustlands2_View/FeatureServer/0',
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: ['Beneficiary'],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {
    #         "'Colorado State University'": 'Colorado State University'
    #     },
    # },
    'CO-ownership-beneficiary': {
        STATE: 'CO',
        UNIVERSITY: 'Colorado State University',
        MANAGING_AGENCY: 'State Land Board',
        URL:
        'https://services5.arcgis.com/rqsYvPKZmvSrSWbw/ArcGIS/rest/services/Surface_Ownership_Beneficiary/FeatureServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Beneficiary'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'Colorado State University'": 'Colorado State University'
        },
    },
    # 'IA': {
    #     URL:
    #     'https://programs.iowadnr.gov/geospatial/rest/services/Boundaries/Public_Lands/MapServer/0',
    #     # 'https://programs.iowadnr.gov/geospatial/rest/services/Boundaries/Public_Lands_ESRI/MapServer/0',
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: [],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {},
    # },
    'ID': {
        STATE: 'ID',
        UNIVERSITY: 'University of Idaho',
        MANAGING_AGENCY: 'Department of Lands',
        URL:
        'https://gis1.idl.idaho.gov/arcgis/rest/services/State_Ownership/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['SURF_ENDOWMENT'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            8: 'University of ID',
            20: 'University of ID Regent',
            907: 'Split - PS 65%, CI 27%, and U 8%',
            908: 'Split - PS 68% and U 32%',
            910: 'Split - U 77.8% and NS 22.2%',
            911: 'Split - U 96% and HS 4%',
            928: 'Split - U and F.&G.'
        },
    },
    # 'MI': {
    #     URL:
    #     'https://services3.arcgis.com/Jdnp1TjADvSDxMAX/ArcGIS/rest/services/dnrRealEstate/FeatureServer/2',
    #     ATTRIBUTE_LABEL_TO_FILTER_BY: [],
    #     ATTRIBUTE_CODE_TO_ALIAS_MAP: {},
    # },
    'MN': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'MN',
        UNIVERSITY: 'University of Minnesota',
        MANAGING_AGENCY: 'Department of Natural Resources',
        URL: '../../Downloads/shp_plan_stateland_dnrcounty.zip',
        # 'https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_dnr/plan_stateland_dnrcounty/shp_plan_stateland_dnrcounty.zip',
        LAYER: 'stateland_type_trust',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['LANDTYPECO'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '5': 'Trust Fund: University (University Trust)',
        },
    },
    'MT': {
        STATE: 'MT',
        UNIVERSITY: 'Montana State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        URL:
        'https://gis.dnrc.mt.gov/arcgis/rest/services/DNRALL/BasemapService/MapServer/31',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['GrantID'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'ACI'": 'MSU Morrill',
            "'ACB'": 'MSU 2nd Grant'
        },
    },
    'NM-surface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'NM',
        UNIVERSITY: 'New Mexico State University',
        MANAGING_AGENCY: 'State Land Office',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        URL: '../../Downloads/slo_STLStatusCombined.zip',
        # TODO: switch out actual url
        # 'https://mapservice.nmstatelands.org/GISDataDownloads/ZipFiles/slo_STLStatusCombined.zip',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Benef_Surf'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '04': 'New Mexico State University',
        },
    },
    'NM-subsurface': {
        DOWNLOAD_TYPE: SHAPEFILE_DOWNLOAD_TYPE,
        STATE: 'NM',
        UNIVERSITY: 'New Mexico State University',
        MANAGING_AGENCY: 'State Land Office',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        URL: '../../Downloads/slo_STLStatusCombined.zip',
        # TODO: switch out actual url
        # 'https://mapservice.nmstatelands.org/GISDataDownloads/ZipFiles/slo_STLStatusCombined.zip',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['Benef_SubS'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            '04': 'New Mexico State University',
        },
    },
    'OR-surface': {
        STATE: 'OR',
        UNIVERSITY: 'Oregon State University',
        MANAGING_AGENCY: 'Department of State Lands',
        URL:
        'https://maps.dsl.state.or.us/arcgis/rest/services/SlisPublic/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['SURF_OWNER'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'OSU'": 'Oregon State University'
        },
    },
    'OR-subsurface': {
        STATE: 'OR',
        UNIVERSITY: 'Oregon State University',
        MANAGING_AGENCY: 'Department of State Lands',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        URL:
        'https://maps.dsl.state.or.us/arcgis/rest/services/SlisPublic/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['SUB_OWNER'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'OSU'": 'Oregon State University'
        },
    },
    'UT-surface': {
        STATE: 'UT',
        UNIVERSITY: 'Utah State University',
        MANAGING_AGENCY: 'Trust Lands Administration',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        URL:
        'https://gis.trustlands.utah.gov/server/rest/services/Ownership/UT_SITLA_Ownership_Beneficiary/MapServer/1',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['bene_abrev'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'USU'": 'Utah State University'
        },
    },
    'UT-subsurface': {
        STATE: 'UT',
        UNIVERSITY: 'Utah State University',
        MANAGING_AGENCY: 'Trust Lands Administration',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        URL:
        'https://gis.trustlands.utah.gov/server/rest/services/Ownership/UT_SITLA_Ownership_Beneficiary/MapServer/0',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['bene_abrev'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'USU'": 'Utah State University'
        },
    },
    'WA-surface': {
        STATE: 'WA',
        UNIVERSITY: 'Washington State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        URL:
        'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['SURFACE_TRUST_CD'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            4: 'Agricultural School',
            5: 'University Transferred',
            10: 'Scientific School',
            11: 'University Original'
        },
    },
    'WA-subsurface': {
        STATE: 'WA',
        UNIVERSITY: 'Washington State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        URL:
        'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['MINERAL_TRUST_CD'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            4: 'Agricultural School',
            5: 'University Transferred',
            10: 'Scientific School',
            11: 'University Original'
        },
    },
    'WA-timber': {
        STATE: 'WA',
        UNIVERSITY: 'Washington State University',
        MANAGING_AGENCY: 'Department of Natural Resources',
        RIGHTS_TYPE: 'timber',
        URL:
        'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['TIMBER_TRUST_CD'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            4: 'Agricultural School',
            5: 'University Transferred',
            10: 'Scientific School',
            11: 'University Original'
        },
    },
    'WY-subsurface': {
        STATE: 'WY',
        UNIVERSITY: 'University of Wyoming',
        MANAGING_AGENCY: 'Board of Commissioners of Public Lands',
        RIGHTS_TYPE: SUBSURFACE_RIGHTS_TYPE,
        URL:
        'https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/19',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['FundCode'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'UN'": 'University Land (trust)',
            "'UW'": 'University of Wyoming (acquired)'
        },
    },
    'WY-surface': {
        STATE: 'WY',
        UNIVERSITY: 'University of Wyoming',
        MANAGING_AGENCY: 'Board of Commissioners of Public Lands',
        RIGHTS_TYPE: SURFACE_RIGHTS_TYPE,
        URL:
        'https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/18',
        ATTRIBUTE_LABEL_TO_FILTER_BY: ['FundCode'],
        ATTRIBUTE_CODE_TO_ALIAS_MAP: {
            "'UN'": 'University Land (trust)',
            "'UW'": 'University of Wyoming (acquired)'
        },
    },
}