queries = {
    'WA': {
        'url':
        'https://gis.dnr.wa.gov/site3/rest/services/Public_Boundaries/WADNR_PUBLIC_Cadastre_OpenData/MapServer/6/',
        'attribute_label_to_filter_by':
        ['SURFACE_TRUST_CD', 'MINERAL_TRUST_CD', 'TIMBER_TRUST_CD'],
        'attribute_value_to_alias_map': {
            4: 'Agricultural School',
            5: 'University Transferred',
            10: 'Scientific School',
            11: 'University Original'
        },
    },
    'MT': {
        'url':
        'https://gis.dnrc.mt.gov/arcgis/rest/services/DNRALL/BasemapService/MapServer/31',
        'attribute_label_to_filter_by': ['GrantID'],
        'attribute_value_to_alias_map': {
            "'ACI'": 'MSU Morrill',
            "'ACB'": 'MSU 2nd Grant'
        },
    },
    'UT-surface-trust': {
        'url':
        'https://gis.trustlands.utah.gov/server/rest/services/Ownership/UT_SITLA_Ownership_Beneficiary/MapServer/1',
        'attribute_label_to_filter_by': ['bene_abrev'],
        'attribute_value_to_alias_map': {
            "'USU'": 'Utah State University'
        },
    },
    'UT-mineral-trust': {
        'url':
        'https://gis.trustlands.utah.gov/server/rest/services/Ownership/UT_SITLA_Ownership_Beneficiary/MapServer/0',
        'attribute_label_to_filter_by': ['bene_abrev'],
        'attribute_value_to_alias_map': {
            "'USU'": 'Utah State University'
        },
    },
    'AL': {
        'url':
        'https://conservationgis.alabama.gov/adcnrweb/rest/services/StateLands/MapServer/0',
        'attribute_label_to_filter_by': [],
        'attribute_value_to_alias_map': {},
    },
    'OR': {
        'url':
        'https://maps.dsl.state.or.us/arcgis/rest/services/SlisPublic/MapServer/0',
        'attribute_label_to_filter_by': ['SURF_OWNER', 'SUB_OWNER'],
        'attribute_value_to_alias_map': {
            "'OSU'": 'Oregon State University'
        },
    },
    'ID': {
        'url':
        'https://gis1.idl.idaho.gov/arcgis/rest/services/State_Ownership/MapServer/0',
        'attribute_label_to_filter_by': ['SURF_ENDOWMENT'],
        'attribute_value_to_alias_map': {
            8: 'University of ID',
            20: 'University of ID Regent',
            907: 'Split - PS 65%, CI 27%, and U 8%',
            908: 'Split - PS 68% and U 32%',
            910: 'Split - U 77.8% and NS 22.2%',
            911: 'Split - U 96% and HS 4%',
            928: 'Split - U and F.&G.'
        },
    },
    'CO-trustland-leases': {
        'url':
        'https://services5.arcgis.com/rqsYvPKZmvSrSWbw/ArcGIS/rest/services/SLB_Leases_ALL_Trustlands2_View/FeatureServer/0',
        'attribute_label_to_filter_by': ['Beneficiary'],
        'attribute_value_to_alias_map': {
            "'Colorado State University'": 'Colorado State University'
        },
    },
    'CO-ownership-beneficiary': {
        'url':
        'https://services5.arcgis.com/rqsYvPKZmvSrSWbw/ArcGIS/rest/services/Surface_Ownership_Beneficiary/FeatureServer/0',
        'attribute_label_to_filter_by': ['Beneficiary'],
        'attribute_value_to_alias_map': {
            "'Colorado State University'": 'Colorado State University'
        },
    },
    'MI': {
        'url':
        'https://services3.arcgis.com/Jdnp1TjADvSDxMAX/ArcGIS/rest/services/dnrRealEstate/FeatureServer/2',
        'attribute_label_to_filter_by': [],
        'attribute_value_to_alias_map': {},
    },
    'IA': {
        'url':
        'https://programs.iowadnr.gov/geospatial/rest/services/Boundaries/Public_Lands/MapServer/0',
        # 'https://programs.iowadnr.gov/geospatial/rest/services/Boundaries/Public_Lands_ESRI/MapServer/0',
        'attribute_label_to_filter_by': [],
        'attribute_value_to_alias_map': {},
    },
    'WY-subsurface': {
        'url':
        'https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/19',
        'attribute_label_to_filter_by': ['FundCode'],
        'attribute_value_to_alias_map': {
            "'UN'": 'University Land (trust)',
            "'UW'": 'University of Wyoming (acquired)'
        },
    },
    'WY-surface': {
        'url':
        'https://gis2.statelands.wyo.gov/arcgis/rest/services/Services/MapViewerService2/MapServer/18',
        'attribute_label_to_filter_by': ['FundCode'],
        'attribute_value_to_alias_map': {
            "'UN'": 'University Land (trust)',
            "'UW'": 'University of Wyoming (acquired)'
        },
    },
    'AZ': {
        'url':
        'https://server.azgeo.az.gov/arcgis/rest/services/azland/State_Trust_Parcels/MapServer/0',
        'attribute_label_to_filter_by': ['fundtxt'],
        'attribute_value_to_alias_map': {
            "'UNIVERSITY'": 'UNIVERSITY',
            "'UNIV OF ARIZ (ACT 2/18/1881)'": 'UNIV OF ARIZ (ACT 2.18.1881)'
        },
    },
}