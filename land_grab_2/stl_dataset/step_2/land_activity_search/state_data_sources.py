from land_grab_2.stl_dataset.step_2.land_activity_search.entities import StateForActivity, StateActivityDataSource

rewrite_rules = {
    "id": {
        "Water": {
            "TypeGroup": "Rights-Type",
            "Status": "Lease Status",
            "WaterUse": "Sub-activity",
            "Source": "Source"
        },
        "roads": {
            "EasementRight": "Rights-Type",
            "TypeGroup": "Transaction Type",
            "Status": "Lease Status",
            "EasementPurpose": "Activity",
            "Easement Purpose": "Activity",
            "Parties": "Lessee or Owner or Manager",
            "DteGranted": "Lease Start Date",
            "DteExpires": "Lease End Date"
        },
        "misc": {
            "TypeGroup": "Transaction Type",
            "Status": "Lease Status",
            "Type": "Activity",
            "Commodities": "Commodity",
            "Name": "Lessee or Owner or Manager",
            "DteGranted": "Lease Start Date",
            "DteExpires": "Lease End Date"
        }
    },
    "co": {
        "misc": {
            "Transaction Type": "Transaction Type",
            "Lease Status": "Lease Status",
            "Lease Type": "Activity",
            "Lease Subtype": "Sub-activity",
            "Lessee Name": "Lessee or Owner or Manager",
            "Lease State Date": "Lease Start Date",
            "Lease End Date": "Lease End Date"
        }
    },
    "mn": {
        "Aggregate Minerals": {
            "Status_1": "Lease Status",
            "Type": "Sub-activity",
            "Status_2": "Use Purpose"
        },
        "Peat": {
            "T_LEASETYP": "Activity",
            "T_PNAMES": "Lessee or Owner or Manager",
            "T_STARTDAT": "Lease Start Date",
            "T_EXPDATE": "Lease End Date"
        },
        "Recreation": {
            "AREA_NAME": "Sub-activity",
            "AREA_TYPE": "Use Purpose"
        },
        "Recreation-DNR Managed": {
            "UNIT_NAME": "Sub-activity",
            "UNIT_TYPE": "Use Purpose",
            "ADMINISTRA": "Lessee or Owner or Manager"
        },
        "Active Minerals": {
            "T_LEASETYP": "Commodity",
            "T_PNAMES": "Lessee or Owner or Manager",
            "T_STARTDAT": "Lease Start Date",
            "T_EXPDATE": "Lease End Date",
            "ML_SU_LAND": "LandClass"
        },
        "Historic Mineral Leases": {
            "T_LEASETYP": "Commodity",
            "T_PNAMES": "Lessee or Owner or Manager",
            "T_STARTDAT": "Lease Start Date",
            "T_EXPDAT": "Lease End Date",
            "ML_SU_LAND": "LandClass"
        }
    },
    "nd": {
        "Minerals": {
            "LEASE_STATUS": "Lease Status",
            "LESSEE": "Lessee or Owner or Manager",
            "LEASE_EFFECTIVE": "Lease Start Date",
            "LEASE_EXPIRATION": "Lease End Date",
            "LEASE_EXTENDED": "Lease Extension Date"
        },
        "Recreation": {
            "UNIT_NAME": "Sub-activity"
        }
    },
    "ne": {
        "Water": {
            "RightStatu": "Lease Status",
            "RightUse": "Sub-activity",
            "FirstName": "Lessee or Owner or Manager",
            "LastName": "Lessee Name 2"
        },
        "Recreation": {
            "Status": "Lease Status",
            "AreaName": "Sub-activity",
            "StartDate": "Lease Start Date"
        }
    },
    "ok": {
        "misc": {
            "EasementType": "Lease Status",
            "Purpose": "Activity",
            "Grantee": "Lessee or Owner or Manager"
        },
        "Agriculture": {
            "LeaseType": "Activity",
            "OwnerName": "Lessee or Owner or Manager",
            "Address2": "Owner Address or Location",
            "BeginDate": "Lease Start Date",
            "EndDate": "Lease End Date"
        },
        "Minerals": {
            "OwnerName": "Lessee or Owner or Manager",
            "Address2": "Owner Address or Location",
            "BeginDate": "Lease Start Date",
            "EndDate": "Lease End Date"
        }
    },
    "tx": {
        "renewables": {
            "FIRST_sitedescription": "Activity"
        },
        "minerals": {
            "UnitTypeDescription": "Activity"
        },
        "misc": {
            "LEASE_STAT": "Lease Status",
            "ACTIVITY": "Activity",
            "Purpose": "Sub-activity",
            "PRIMARY_LE": "Lessee or Owner or Manager"
        },
        "Hard Minerals": {
            "LEASE_STAT": "Lease Status",
            "ORIGINAL_L": "Lessee or Owner or Manager",
            "EFFECTIVE_": "Lease Start Date"
        },
        "Oil and gas": {
            "LEASE_STAT": "Lease Status",
            "ORIGINAL_L": "Lessee or Owner or Manager",
            "LESSOR": "Lessor",
            "EFFECTIVE_": "Lease Start Date"
        },
        "Coastal": {
            "ACTIVITY_T": "Activity",
            "PROJECT_NA": "Sub-activity",
            "GRANTEE": "Lessee or Owner or Manager"
        }
    },
    "az": {
        "misc": {
            "leased": "Lease Status",
            "ke": "Activity",
            "full_name": "Lessee or Owner or Manager",
            "effdate": "Lease Start Date",
            "expdate": "Lease End Date"
        },
        "Minerals": {
            "leased": "Lease Status",
            "ke": "Activity",
            "full_name": "Lessee or Owner or Manager",
            "effdate": "Lease Start Date",
            "expdate": "Lease End Date"
        },
        "Oil and gas": {
            "leased": "Lease Status",
            "type": "Activity",
            "full_name": "Lessee or Owner or Manager",
            "effdate": "Lease Start Date",
            "expdate": "Lease End Date"
        },
        "Solar": {
            "status": "Lease Status",
            "technology": "Sub-activity",
            "projectnam": "Lessee or Owner or Manager"
        },
        "Agriculture": {
            "name": "Sub-activity"
        }
    },
    "wy": {
        "Metallic and Nonmetallic Minerals": {
            "LeaseStatusLabel": "Lease Status",
            "MineralTypeLabel": "Activity",
            "MetallicNonMetallicLeaseSubType": "Sub-activity",
            "CompanyName": "Lessee or Owner or Manager",
            "CompanyZipCode": "Owner Address or Location",
            "LeaseIssueDate": "Lease Start Date",
            "LeaseExpirationDate": "Lease End Date"
        },
        "Oil and gas": {
            "LeaseStatusLabel": "Lease Status",
            "MineralTypeLabel": "Activity",
            "CompanyName": "Lessee or Owner or Manager",
            "CompanyZipCode": "Owner Address or Location",
            "LeaseIssueDate": "Lease Start Date",
            "LeaseExpirationDate": "Lease End Date"
        },
        "Easements": {
            "Status_LU": "Lease Status",
            "Sub_Group_LU": "Activity",
            "Use_Type_LU": "Sub-activity",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Issue_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        },
        "Grazing": {
            "Status_LU": "Lease Status",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Start_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        },
        "Special": {
            "Status_LU": "Lease Status",
            "Type_LU": "Activity",
            "Purpose_LU": "Sub-activity",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Start_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        },
        "Wind": {
            "Status_LU": "Lease Status",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Start_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        }
    },
    "wa": {
        "Metallic Minerals": {
            "PRODUCTION": "Lease Status",
            "ORE_MINERA": "Sub-activity",
            "COMMODITIE": "Commodity"
        },
        "Oil and gas": {
            "WELL_STATU": "Lease Status",
            "COMPANY_NA": "Lessee or Owner or Manager"
        },
        "Agriculture": {
            "CropType": "Activity",
            "CropGroup": "Sub-activity"
        },
        "Mining": {
            "MINE_NAME": "Sub-activity",
            "COMMODITY_": "Commodity",
            "APPLICANT_": "Lessee or Owner or Manager"
        },
        "Non-Metallic Minerals": {
            "MINERAL": "Sub-activity"
        }
    },
    "ut": {
        "Oil and gas fields": {
            "STATUS": "Lease Status"
        },
        "Recreation": {
            "STATUS": "Lease Status",
            "TYPE": "Activity",
            "NAME": "Sub-activity"
        },
        "Water": {
            "LU_Group": "Lease Status",
            "Descriptio": "Sub-activity"
        },
        "Grazing": {
            "AllotName": "Sub-activity",
            "Manager": "Lessee or Owner or Manager"
        },
        "Oil and gas wells": {
            "Operator": "Lessee or Owner or Manager"
        }
    },
    "nm": {
        "Agriculture": {
            "STATUS": "Lease Status",
            "OGRID_NAM": "Lessee or Owner or Manager"
        },
        "Commercial Leases": {
            "STATUS": "Lease Status",
            "OGRID_NAM": "Lessee or Owner or Manager",
            "VEREFF_DTE": "Lease Start Date",
            "VERTRM_DTE": "Lease End Date"
        },
        "Energy": {
            "STATUS": "Lease Status",
            "LEASE_TYPE": "Activity",
            "OGRID_NAM": "Lessee or Owner or Manager"
        },
        "Minerals": {
            "STATUS": "Lease Status",
            "LEASE_TYPE": "Activity",
            "SUB_TYPE": "Sub-activity",
            "OGRID_NAM": "Lessee or Owner or Manager",
            "VEREFF_DTE": "Lease Start Date",
            "VERTRM_DTE": "Lease End Date"
        },
        "Oil and gas": {
            "STATUS": "Lease Status",
            "OGRID_NAM": "Lessee or Owner or Manager",
            "VEREFF_DTE": "Lease Start Date",
            "VERTRM_DTE": "Lease End Date"
        },
        "Roads": {
            "STATUS": "Lease Status",
            "OGRID_NAM": "Lessee or Owner or Manager"
        }
    },
    "mt": {
        "misc": {
            "UNITTYPE": "Activity",
            "MANAME": "Sub-activity",
            "INST": "Lessee or Owner or Manager"
        },
        "Oil and Gas Wells": {
            "Status": "Lease Status",
            "Type": 'Sub-activity',
            "CoName": "Lessee or Owner or Manager",
            "Completed": "Lease End Date"
        },
        "Timber": {
            "LandOffice": "Lessee or Owner or Manager",
            "HarvestPrescription": "Sub-activity",
            "DateSold": "Lease Start Date",
            "DateClosed": "Lease End Date"
        },
        "Lumber Mill": {
            "facilname": "Lessee or Owner or Manager",
            "milltypeDe": "Sub-activity"
        },
        "Oil and Gas Active Lease": {
            "Prim_Cust": "Lessee or Owner or Manager",
            "Producing": "Lease Status",
            "DateEffect": "Lease Start Date",
            "DateExpire": "Lease End Date"
        },
        "Coal Active Lease": {
            "Prim_Cust": "Lessee or Owner or Manager",
            "Producing": "Lease Status",
            "DateEffect": "Lease Start Date",
            "DateExpire": "Lease End Date"
        }
    },
    "wi": {
        "misc": {
            "PROP_NAME": "Activity"
        }
    },
    "sd": {
        "Recreation": {
            "ParkName": "Sub-activity"
        }
    }
}
STATE_ACTIVITIES = {
    'AZ': StateForActivity(name='arizona', activities=[
        StateActivityDataSource(name='misc',
                                location='Arizona_All/Miscellaneous.shp',
                                keep_cols=['leased', 'ke', 'effdate', 'expdate', 'full_name'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Minerals',
                                location='Arizona_All/Minerals.shp',
                                keep_cols=['leased', 'ke', 'effdate', 'expdate', 'full_name'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas',
                                location='Arizona_All/OilGas.shp',
                                keep_cols=['type', 'leased', 'effdate',
                                           'expdate',
                                           'full_name'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Agriculture',
                                location='Arizona_All/Grazing.shp',
                                keep_cols=['name'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Solar',
                                location='Arizona_All/Solar.shp',
                                keep_cols=['technology', 'projectnam', 'status'],
                                use_name_as_activity=True),
    ]),
    'CO': StateForActivity(name='colorado', activities=[
        StateActivityDataSource(name='misc',
                                location='Colorado_All/Miscellaneous.shp',
                                keep_cols=['Transaction Type', 'Lease Type', 'Lease Subtype', 'Lessee Name',
                                           'Lease State Date',
                                           'Lease End Date', 'Lease Status'],
                                use_name_as_activity=False)

    ]),
    'ID': StateForActivity(name='idaho', activities=[
        StateActivityDataSource(name='misc',
                                location='Idaho_All/Miscellaneous.shp',
                                keep_cols=['TypeGroup', 'Type', 'Status', 'DteGranted', 'DteExpires', 'Name',
                                           'Commodities'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='roads',
                                location='Idaho_All/Roads.shp',
                                keep_cols=['TypeGroup', 'Status', 'DteGranted', 'DteExpires', 'Parties',
                                           'EasementRight', 'EasementPurpose'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Water',
                                location='Idaho_All/Water.shp',
                                keep_cols=['TypeGroup', 'Status', 'WaterUse', 'Source'],
                                use_name_as_activity=True),

    ]),
    'MN': StateForActivity(name='minnesota', activities=[
        StateActivityDataSource(name='Peat',
                                location='Minnesota_All/shp_plan_state_peatleases',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Recreation',
                                location='Minnesota_All/shp_bdry_dnr_managed_areas/dnr_stat_plan_areas.shp',
                                keep_cols=['AREA_NAME', 'AREA_TYPE'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation-DNR Managed',
                                location='Minnesota_All/shp_bdry_dnr_managed_areas/dnr_management_units.shp',
                                keep_cols=['UNIT_NAME', 'UNIT_TYPE', 'ADMINISTRA'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Aggregate Minerals',
                                location='Minnesota_All/shp_geos_aggregate_mapping/armp_aggmines.shp',
                                keep_cols=['Type', 'Status_1', 'Status_2'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active Minerals',
                                location='Minnesota_All/shp_plan_state_minleases/active_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic Mineral Leases',
                                location='Minnesota_All/shp_plan_state_minleases/historic_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                use_name_as_activity=True)

    ]),

    'ND': StateForActivity(name='north dakota', activities=[
        StateActivityDataSource(name='Minerals',
                                location='NorthDakota_All/Minerals.shp',
                                keep_cols=['LEASE_STATUS', 'LEASE_EFFECTIVE', 'LEASE_EXPIRATION', 'LEASE_EXTENDED',
                                           'LESSEE'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation',
                                location='NorthDakota_All/Recreation.shp',
                                keep_cols=['UNIT_NAME'],
                                use_name_as_activity=True),

    ]),
    'NE': StateForActivity(name='nebraska', activities=[
        StateActivityDataSource(name='Water',
                                location='Nebraska_All/LOC_SurfaceWaterRightsDiversionsExternal_DNR.shp',
                                keep_cols=['RightStatu', 'RightUse', 'FirstName', 'LastName'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation',
                                location='Nebraska_All/Park_Areas.shp',
                                keep_cols=['AreaName', 'StartDate', 'Status'],
                                use_name_as_activity=True),

    ]),
    'NM': StateForActivity(name='new mexico', activities=[
        StateActivityDataSource(name='Agriculture',
                                location='NewMexico_All/Ag_Leases',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM']),
        StateActivityDataSource(name='Commercial Leases',
                                location='NewMexico_All/Commercial_Leases',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM', 'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Energy',
                                location='NewMexico_All/Energy_Leases',
                                use_name_as_activity=False,
                                keep_cols=['STATUS', 'LEASE_TYPE',
                                           'OGRID_NAM']),
        StateActivityDataSource(name='Minerals',
                                location='NewMexico_All/Mineral_Leases',
                                use_name_as_activity=False,
                                keep_cols=['STATUS', 'LEASE_TYPE', 'OGRID_NAM', 'SUB_TYPE',
                                           'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Oil and gas',
                                location='NewMexico_All/OilGas_Leases',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'VEREFF_DTE', 'VERTRM_DTE', 'OGRID_NAM']),
        StateActivityDataSource(name='Roads',
                                location='NewMexico_All/slo_rwleased',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM']),

    ]),
    'OK': StateForActivity(name='oklahoma', activities=[
        StateActivityDataSource(name='misc',
                                location='Oklahoma_All/Miscellaneous.shp',
                                keep_cols=['Purpose', 'Grantee',
                                           'EasementType'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Minerals',
                                location='Oklahoma_All/Minerals.shp',
                                keep_cols=['BeginDate', 'EndDate', 'OwnerName', 'Address2'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Agriculture',
                                location='Oklahoma_All/Miscellaneous.shp',
                                keep_cols=['LeaseType', 'BeginDate', 'EndDate', 'OwnerName',
                                           'Address2'],
                                use_name_as_activity=False),

    ]),
    'SD': StateForActivity(name='south dakota', activities=[
        StateActivityDataSource(name='Recreation',
                                location='SouthDakota_All',
                                keep_cols=['ParkName'],
                                use_name_as_activity=True),

    ]),
    'TX': StateForActivity(name='texas', activities=[
        StateActivityDataSource(name='Coastal',
                                location='Texas_All/NonMineralPoly',
                                keep_cols=['PROJECT_NA', 'GRANTEE', 'ACTIVITY_T'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='misc',
                                location='Texas_All/ME',
                                keep_cols=['LEASE_STAT', 'PRIMARY_LE',
                                           'ALL_LESSEE', 'PURPOSE'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Hard Minerals',
                                location='Texas_All/HardMinerals',
                                keep_cols=['LEASE_STAT', 'ORIGINAL_L', 'EFFECTIVE_'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Texas_All/ActiveLeases',
                                keep_cols=['LEASE_STAT', 'EFFECTIVE_', 'ORIGINAL_L', 'LESSOR'],
                                use_name_as_activity=True),

        StateActivityDataSource(name='Fracking Ponds',
                                location='Texas_All/PUF-FracPonds.shp',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Grazing',
                                location='Texas_All/PUF-Grazing.shp',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Water for Grazing',
                                location='Texas_All/PUF-GrazingWaterSources.shp',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Highways',
                                location='Texas_All/PUF-Highways.shp',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Minerals',
                                location='Texas_All/PUF-Minerals.shp',
                                keep_cols=['UnitTypeDescription'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas',
                                location='Texas_All/PUF-OilandGas.shp',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas Wellbores',
                                location='Texas_All/PUF-OilandGasWellbores.shp',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Renewables',
                                location='Texas_All/PUF-Renewables.shp',
                                keep_cols=['FIRST_sitedescription'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Well Bottom Hole',
                                location='Texas_All/PUF-WellBottomHole.shp',
                                keep_cols=[],
                                use_name_as_activity=True),

    ]),
    'UT': StateForActivity(name='utah', activities=[
        StateActivityDataSource(name='Water',
                                location='Utah_All/Utah_Water_Related_Land_Use',
                                keep_cols=['Descriptio',
                                           'LU_Group'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Geothermal',
                                location='Utah_All/Utah_UREZ_Phase_2_Geothermal',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Wind Zones',
                                location='Utah_All/Utah_UREZ_Phase_1_Wind_Zones',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Solar Zones',
                                location='Utah_All/Utah_UREZ_Phase_1_Solar_Zones',
                                keep_cols=[],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation',
                                location='Utah_All/Utah_Parks_Local',
                                keep_cols=['NAME', 'TYPE', 'STATUS'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas wells',
                                location='Utah_All/Utah_Oil_and_Gas_Well_Locations',
                                keep_cols=['Operator'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas fields',
                                location='Utah_All/Utah_Oil_and_Gas_Fields-shp',
                                keep_cols=['STATUS'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Grazing',
                                location='Utah_All/Utah_Grazing_Allotments',
                                keep_cols=['Manager', 'AllotName'],
                                use_name_as_activity=True)

    ]),
    'WA': StateForActivity(name='washington', activities=[
        StateActivityDataSource(name='Agriculture',
                                location='Washington_All/Agriculture.shp',
                                keep_cols=['CropType', 'CropGroup'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Non-Metallic Minerals',
                                location='Washington_All/NonMetallic_Minerals.shp',
                                keep_cols=['MINERAL'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Metallic Minerals',
                                location='Washington_All/Metallic_Minerals.shp',
                                keep_cols=['COMMODITIE', 'PRODUCTION', 'ORE_MINERA'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Mining',
                                location='Washington_All/Active_Surface_Mine_Permit_Sites.shp',
                                keep_cols=['APPLICANT_', 'MINE_NAME', 'COMMODITY_'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Washington_All/Oil_and_Gas_Wells.shp',
                                keep_cols=['COMPANY_NA', 'WELL_STATU'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Coal',
                                location='Washington_All/Coal.shp',
                                keep_cols=[],
                                use_name_as_activity=True),

    ]),
    'WI': StateForActivity(name='wisconsin', activities=[
        StateActivityDataSource(name='misc',
                                location='Wisconson_All/Miscellaneous.shp',
                                keep_cols=['PROP_NAME'],
                                use_name_as_activity=False),

    ]),
    'WY': StateForActivity(name='wyoming', activities=[
        StateActivityDataSource(name='Metallic and Nonmetallic Minerals',
                                location='Wyoming_All/MetallicNonMetallic.shp',
                                keep_cols=['MetallicNonMetallicLeaseSubType',
                                           'LeaseIssueDate',
                                           'LeaseExpirationDate', 'CompanyName', 'LeaseStatusLabel', 'CompanyZipCode',
                                           'MineralTypeLabel'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas',
                                location='Wyoming_All/OilandGas.shp',
                                keep_cols=['LeaseIssueDate',
                                           'LeaseExpirationDate', 'CompanyName', 'LeaseStatusLabel', 'CompanyZipCode',
                                           'MineralTypeLabel'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Easements',
                                location='Wyoming_All/Easements.shp',
                                keep_cols=['Leaseholder_LU', 'Issue_Date_LU', 'Expiration_Date_LU', 'Status_LU',
                                           'Sub_Group_LU',
                                           'Use_Type_LU'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Grazing',
                                location='Wyoming_All/Grazing.shp',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Special',
                                location='Wyoming_All/SpecialUse.shp',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU',
                                           'Type_LU', 'Purpose_LU'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Wind',
                                location='Wyoming_All/Wind.shp',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU'],
                                use_name_as_activity=True)
    ]),

    'MT': StateForActivity(name='Montana', activities=[
        StateActivityDataSource(name='Oil and Gas Wells',
                                location='Montana_All/wells/wells.shp',
                                keep_cols=['CoName', 'Status', 'Type', 'Completed'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='miscellaneous',
                                location='https://gisservicemt.gov/arcgis/rest/services/MSDI_Framework/ManagedAreas/MapServer/0/query',
                                keep_cols=['MANAME', 'INST', 'UNITTYPE'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Timber',
                                location='https://services2.arcgis.com/DRQySz3VhPgOv7Bo/ArcGIS/rest/services/FMB_Harvest_History/FeatureServer/1/query',
                                keep_cols=['HarvestPrescription', 'DateSold', 'DateClosed', 'LandOffice'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Lumber Mill',
                                location='https://services2.arcgis.com/DRQySz3VhPgOv7Bo/ArcGIS/rest/services/Active_Mills/FeatureServer/0/query',
                                keep_cols=['facilname', 'milltypeDe'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Coal Active Lease',
                                location='Montana_All/MMB_CoalActiveLease.shp',
                                keep_cols=['Prim_Cust', 'Producing', 'DateEffect', 'DateExpire'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and Gas Active Lease',
                                location='Montana_All/MMB_OilandGasActiveLease.shp',
                                keep_cols=['Prim_Cust', 'Producing', 'DateEffect', 'DateExpire'],
                                use_name_as_activity=True)]),
}

