from land_grab_2.stl_dataset.step_2.land_activity_search.entities import StateForActivity, StateActivityDataSource

REWRITE_RULES = {
    "id": {
        "Water": {
            "TypeGroup": "Rights-Type",
            "Status": "Lease Status",
            "WaterUse": "Sub-activity",
            "Source": "Source"
        },
        "Easements": {
            "EasementRi": "Rights-Type",
            "EasementRight": "Rights-Type",
            "TypeGroup": "Transaction Type",
            "Status": "Lease Status",
            "EasementPu": "Activity",
            "EasementPurpose": "Activity",
            "Easement Purpose": "Activity",
            "Parties": "Lessee or Owner or Manager",
            "DteGranted": "Lease Start Date",
            "DteExpires": "Lease End Date"
        },
        "Timber": {
            "Activity": "Sale_Status"
        },
        "Oil and gas": {
            "Activity": "WellStatus"
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
            "Transactio": "Transaction Type",
            "Lease_Stat": "Lease Status",
            "Lease_Type": "Activity",
            "Lease_Subt": "Sub-activity",
            "Lessee_Nam": "Lessee or Owner or Manager",
            "Lease_Star": "Lease Start Date",
            "Lease_End_": "Lease End Date"
        }
    },
    "mn": {
        "Aggregate Minerals": {
            "Status_1": "Lease Status",
            "Type": "Sub-activity",
            "Status_2": "Use Purpose"
        },
        "Peat": {
            "T_LEASETYPE": "Activity",
            "T_PNAMES": "Lessee or Owner or Manager",
            "T_STARTDAT": "Lease Start Date",
            "T_EXPDATE": "Lease End Date"
        },
        "Conservation Easement": {
            "EASETYPE": "Sub-activity"
        },
        "Active NonFerrous Mineral Lease": {
            "T_LEASETYPE": "Activity"
        },
        "Historic NonFerrous Mineral Lease": {
            "T_LEASETYPE": "Activity"
        },
        "Recreation": {
            "AREA_NAME": "Sub-activity",
            "AREA_TYPE": "Activity"
        },
        "Recreation-DNR Managed": {
            "UNIT_NAME": "Sub-activity",
            "UNIT_TYPE": "Activity",
            "ADMINISTRA": "Lessee or Owner or Manager"
        },
        "Active Mineral Leases": {
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
            "Type": "Activity",
            "first_site": "Activity"
        },
        "minerals": {
            "UnitTypeDescription": "Activity",
            "unittypede": "Sub-Activity"
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
            "ke": "Activity",
            "full_name": "Lessee or Owner or Manager",
            "effdate": "Lease Start Date",
            "expdate": "Lease End Date"
        },
        # "Agriculture": {
        #     "name": "Sub-activity"
        # },
        "Solar": {
            "status": "Lease Status",
            "technology": "Sub-activity",
            "projectnam": "Lessee or Owner or Manager"
        }
    },
    "wy": {
        "Metallic and Nonmetallic Mineral Leases": {
            "LeaseStatusLabel": "Lease Status",
            "MineralTypeLabel": "Activity",
            'oslisde._8': 'Activity',
            "MetallicNonMetallicLeaseSubType": "Sub-activity",
            "CompanyName": "Lessee or Owner or Manager",
            "CompanyZipCode": "Owner Address or Location",
            "LeaseIssueDate": "Lease Start Date",
            "LeaseExpirationDate": "Lease End Date"
        },
        "Oil and gas leases": {
            "LeaseStatusLabel": "Lease Status",
            "MineralTypeLabel": "Activity",
            'oslisde.88': "Activity",
            "CompanyName": "Lessee or Owner or Manager",
            "CompanyZipCode": "Owner Address or Location",
            "LeaseIssueDate": "Lease Start Date",
            "LeaseExpirationDate": "Lease End Date"
        },
        "Easements": {
            "Status_LU": "Lease Status",
            #"Sub_Group_LU": "Activity",
            'oslisde.20': "Activity",
            #"Use_Type_LU": "Sub-activity",
            'oslisde.21': "Sub-activity",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Issue_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        },
        "Grazing Lease": {
            "Status_LU": "Lease Status",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Start_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        },
        "Special Use Lease": {
            "Status_LU": "Lease Status",
            "Purpose_LU": "Activity",
            "Type_LU": "Sub-activity",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Start_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        },
        "Wind Lease": {
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
        "Active Surface Mine Permit Sites": {
            "MINE_NAME": "Sub-activity",
            "COMMODITY_": "Commodity",
            "APPLICANT_": "Lessee or Owner or Manager"
        },
        "Non-Metallic Minerals": {
            "MINERAL": "Sub-activity"
        },
        "Current Leases": {
            "AGREEMENT1": "Activity"
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
        "Coal Lease": {
            "AllotName": "Sub-activity",
            "Manager": "Lessee or Owner or Manager"
        },
        "Development Lease": {
            "app_descr": "Activity",
        },
        "Grazing Lease": {
            "app_descr": "Activity",
        },
        "Other Minerals": {
            "app_descr": "Activity",
        },
        "Renewables": {
            "app_descr": "Activity",
        },
        "Special Use Leases": {
            "app_descr": "Activity",
        },
        "Easements": {
            "app_descr": "Activity",
        },
        "OilGasHydrocarbon": {
            "app_descr": "Activity",
        },
        "OilGasOther": {
            "app_descr": "Activity",
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
        "miscellaneous": {
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
        "Agriculture and Grazing": {
            "Status": "Lease Status"
        },
        "Commercial Leases": {
            "LeaseCateg": "Activity"
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
        },
        "conservation easement": {
            "PROGRAM_NAME": "Activity"
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
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Minerals',
                                location='Arizona_All/Minerals.shp',
                                keep_cols=['leased', 'ke', 'effdate', 'expdate', 'full_name'],
                               # is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas',
                                location='Arizona_All/OilGas.shp',
                                keep_cols=['type', 'leased', 'effdate',
                                           'expdate',
                                           'full_name'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        # StateActivityDataSource(name='Agriculture',
        #                         location='Arizona_All/Grazing.shp',
        #                         keep_cols=['name'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=True),
        StateActivityDataSource(name='Solar',
                                location='Arizona_All/Solar.shp',
                                keep_cols=['technology', 'projectnam', 'status'],
                                is_restricted_activity=True,
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
                                # include if Status is active
                                use_name_as_activity=False),
        StateActivityDataSource(name='roads',
                                location='Idaho_All/Easements.shp',
                                keep_cols=['TypeGroup', 'Status', 'DteGranted', 'DteExpires', 'Parties',
                                           'EasementRight', 'EasementPurpose'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Timber',
                                location='Idaho_All/Timber.shp',
                                keep_cols=['Sale_Status'],
                                is_restricted_activity=True,
                                # can we have the name be Timber + 'Sale_Status' column value
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Idaho_All/OilGas.shp',
                                keep_cols=['WellStatus'],
                                # can we have the name be Oil and gas + 'Sale_Status' column value
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Water',
                                location='Idaho_All/Water.shp',
                                keep_cols=['TypeGroup', 'Status', 'WaterUse', 'Source'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),

    ]),
    'MN': StateForActivity(name='minnesota', activities=[
        StateActivityDataSource(name='Peat',
                                location='Minnesota_All/shp_plan_state_peatleases/active_peatLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Recreation',
                                location='Minnesota_All/shp_bdry_dnr_lrs_prk/dnr_stat_plan_areas_prk.shp',
                                keep_cols=['AREA_NAME', 'AREA_TYPE'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Recreation-DNR Managed',
                                location='Minnesota_All/shp_bdry_dnr_managed_areas/dnr_management_units.shp',
                                keep_cols=['UNIT_NAME', 'UNIT_TYPE', 'ADMINISTRA'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Aggregate Minerals',
                                location='Minnesota_All/shp_geos_aggregate_mapping/armp_aggmines.shp',
                                keep_cols=['Type', 'Status_1', 'Status_2'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Conservation Easement',
                                location='Minnesota_All/shp_plan_stateland_dnrcounty/stateland_interest_conservationeasement.shp',
                                keep_cols=['EASETYPE'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active NonFerrous Mineral Lease',
                                location='Minnesota_All/ActiveNonFerrous.shp',
                                keep_cols=['T_LEASETYPE'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic NonFerrous Mineral Lease',
                                location='Minnesota_All/HistoricNonFerrous.shp',
                                keep_cols=['T_LEASETYPE'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active Mineral Leases',
                                location='Minnesota_All/shp_plan_state_minleases/active_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic Mineral Leases',
                                location='Minnesota_All/shp_plan_state_minleases/historic_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                # is_restricted_subsurface_activity=True,
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
                                is_restricted_activity=True,
                                use_name_as_activity=True),

    ]),
    'NM': StateForActivity(name='new mexico', activities=[
        StateActivityDataSource(name='Agriculture',
                                location='NewMexico_All/Ag_Leases',
                                use_name_as_activity=True,
                                is_restricted_activity=True,
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
                                # is_restricted_subsurface_activity=True,
                                keep_cols=['STATUS', 'LEASE_TYPE', 'OGRID_NAM', 'SUB_TYPE',
                                           'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Oil and gas',
                                location='NewMexico_All/OilGas_Leases',
                                use_name_as_activity=True,
                                # is_restricted_subsurface_activity=True,
                                keep_cols=['STATUS', 'VEREFF_DTE', 'VERTRM_DTE', 'OGRID_NAM']),
        StateActivityDataSource(name='Roads',
                                location='NewMexico_All/slo_rwleased',
                                use_name_as_activity=True,
                                is_restricted_activity=True,
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
                                is_restricted_activity=True,
                                use_name_as_activity=False),

    ]),
    'SD': StateForActivity(name='south dakota', activities=[
        StateActivityDataSource(name='Recreation',
                                location='SouthDakota_All',
                                keep_cols=['ParkName'],
                                is_restricted_activity=True,
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
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Texas_All/ActiveLeases',
                                keep_cols=['LEASE_STAT', 'EFFECTIVE_', 'ORIGINAL_L', 'LESSOR'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),

        StateActivityDataSource(name='Fracking Ponds',
                                location='Texas_All/PUF-FracPonds.shp',
                                keep_cols=[],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Grazing Lease',
                                location='Texas_All/PUF-GrazingLease.shp',
                                keep_cols=[],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Water for Grazing',
                                location='Texas_All/PUF-GrazingWaterSources.shp',
                                keep_cols=[],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Highways',
                                location='Texas_All/PUF-Highways.shp',
                                keep_cols=[],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Minerals',
                                location='Texas_All/PUF-Minerals.shp',
                                keep_cols=['UnitTypeDescription'],
                                # is_restricted_subsurface_activity=True,
                                # can we have the name be Oil and Gas Lease + 'UnitTypeDescription' value
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas lease',
                                location='Texas_All/PUF-OilGasLease.shp',
                                keep_cols=['LeaseStatus'],
                                # is_restricted_subsurface_activity=True,
                                # can we have the name be Oil and Gas Lease + 'LeaseStatus' column value
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas Wellbores',
                                location='Texas_All/PUF-OilGasWellbores.shp',
                                keep_cols=['Cycle'],
                                # is_restricted_subsurface_activity=True,
                                # can we have the name be Oil and Gas Wellbore + 'Cycle' column value
                                use_name_as_activity=True),
        StateActivityDataSource(name='Renewables',
                                location='Texas_All/PUF-Renewables.shp',
                                keep_cols=['Type'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        # StateActivityDataSource(name='Renewable Tracts',
        #                         location='Texas_All/PUF-Renewables.shp',
        #                         keep_cols=['FIRST_sitedescription'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=False),
        StateActivityDataSource(name='Well Bottom Hole',
                                location='Texas_All/PUF-WellBottomHole.shp',
                                keep_cols=['Cycle'],
                                # is_restricted_subsurface_activity=True,
                                # can we have the name be Oil and Gas Well Bottom Hole + 'Cycle' column value
                                use_name_as_activity=True),

    ]),
    'UT': StateForActivity(name='utah', activities=[
        # StateActivityDataSource(name='Water',
        #                         location='Utah_All/Utah_Water_Related_Land_Use',
        #                         keep_cols=['Descriptio',
        #                                    'LU_Group'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=True),

        StateActivityDataSource(name='Coal Contracts',
                                location='Utah_All/Contracts_Coal/Contracts_Coal.shp',
                                keep_cols=['app_descr'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Development Lease',
                                location='Utah_All/Contracts_Dev_Lease/Contracts_Dev_Lease.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Grazing Lease',
                                location='Utah_All/Contracts_Dev_Lease/Contracts_Dev_Lease.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil Shale Contracts',
                                location='Utah_All/Contracts_Oil_Shale/Contracts_Oil_Shale.shp',
                                keep_cols=['app_descr'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Other Minerals',
                                location='Utah_All/Contracts_Other_Mineral/Contracts_Other_Mineral.shp',
                                keep_cols=['app_descr'],
                                # is_restricted_subsurface_activity=True,
                                # can we have the name be Other Minerals + 'app_descr' value
                                use_name_as_activity=False),
        StateActivityDataSource(name='Renewables',
                                location='Utah_All/Contracts_Renewable/Contracts_Renewable.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                # can we have the name be Other Minerals + 'app_descr' value
                                use_name_as_activity=False),
        StateActivityDataSource(name='Range Improvement Project Contracts',
                                location='Utah_All/Contracts_Rip/Contracts_Rip.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                # can we have the name be Other Minerals + 'app_descr' value
                                use_name_as_activity=True),
        StateActivityDataSource(name='Sand Gravel Contracts',
                                location='Utah_All/Contracts_Sand_Gravel/Contracts_Sand_Gravel.shp',
                                keep_cols=['app_descr'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Tar Sand Contracts',
                                location='Utah_All/Contracts_Sula/Contracts_Sula.shp',
                                keep_cols=['app_descr'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Special Use Leases',
                                location='Utah_All/Contracts_Tar_Sand/Contracts_Tar_Sand.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Easements',
                                location='Utah_All/Easements.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='OilGasHydrocarbon',
                                location='Utah_All/OilGasHydrocarbon.shp',
                                keep_cols=['app_descr'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='OilGasOther',
                                location='Utah_All/OilGasOther.shp',
                                keep_cols=['app_descr'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        #
        # StateActivityDataSource(name='Geothermal',
        #                         location='Utah_All/Utah_UREZ_Phase_2_Geothermal',
        #                         keep_cols=[],
        #                         use_name_as_activity=True),
        StateActivityDataSource(name='Wind Zones',
                                location='Utah_All/Utah_UREZ_Phase_1_Wind_Zones',
                                keep_cols=[],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Solar Zones',
                                location='Utah_All/Utah_UREZ_Phase_1_Solar_Zones',
                                keep_cols=[],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation',
                                location='Utah_All/Utah_Parks_Local',
                                keep_cols=['NAME', 'TYPE', 'STATUS'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas wells',
                                location='Utah_All/Utah_Oil_and_Gas_Well_Locations',
                                keep_cols=['Operator'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas fields',
                                location='Utah_All/Utah_Oil_and_Gas_Fields-shp',
                                keep_cols=['STATUS'],
                                use_name_as_activity=True),
        # StateActivityDataSource(name='Grazing',
        #                         location='Utah_All/Utah_Grazing_Allotments',
        #                         keep_cols=['Manager', 'AllotName'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=True),
        # StateActivityDataSource(name='Coal Lease',
        #                         location='Utah_All/Utah_Coal_Leases',
        #                         keep_cols=[],
        #                         use_name_as_activity=True)

    ]),
    'WA': StateForActivity(name='washington', activities=[
        # StateActivityDataSource(name='Agriculture',
        #                         location='Washington_All/Agriculture.shp',
        #                         keep_cols=['CropType', 'CropGroup'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=False),
        StateActivityDataSource(name='Current Leases',
                                location='Washington_All/current_leases_spatial_nature_20231109/current_leases_spatial_nature_20231109.shp',
                                keep_cols=['AGREEMENT1'],
                                # Use WA key
                                use_name_as_activity=True),
        StateActivityDataSource(name='Non-Metallic Minerals',
                                location='Washington_All/NonMetallicMinerals.shp',
                                keep_cols=['MINERAL'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Metallic Minerals',
                                location='Washington_All/MetallicMinerals.shp',
                                keep_cols=['COMMODITIE', 'PRODUCTION', 'ORE_MINERA'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active Surface Mine Permit Sites',
                                location='Washington_All/Active_Surface_Mine_Permit_Sites.shp',
                                keep_cols=['APPLICANT_', 'MINE_NAME', 'COMMODITY_'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Washington_All/OilGasWells.shp',
                                keep_cols=['COMPANY_NA', 'WELL_STATU'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Coal',
                                location='Washington_All/Coal.shp',
                                keep_cols=[],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),

    ]),
    'WI': StateForActivity(name='wisconsin', activities=[
        StateActivityDataSource(name='misc',
                                location='Wisconson_All/Miscellaneous.shp',
                                keep_cols=['PROP_NAME'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Conservation Easement',
                                location='https://dnrmaps.wi.gov/arcgis/rest/services/LF_DML/LF_NRCS_EASEMENT_WTM_Ext/MapServer/0/query',
                                keep_cols=['PROGRAM_NAME'],
                                # Name plus 'PROGRAM_NAME' field
                                use_name_as_activity=False),
        StateActivityDataSource(name='DNR Easement',
                                location='Wisconsin_All/DNR_Easement.shp',
                                keep_cols=['EASE_USE_C'],
                                # Name plus 'Ease use code' field
                                use_name_as_activity=False),
        StateActivityDataSource(name='DNR Owned',
                                location='Wisconsin_All/DNR_Owned.shp',
                                keep_cols=['EASE_USE_C'],
                                # Name plus 'Ease use code' field
                                use_name_as_activity=False)
    ]),
    'WY': StateForActivity(name='wyoming', activities=[
        StateActivityDataSource(name='Metallic and Nonmetallic Mineral Leases',
                                location='Wyoming_All/MetallicNonMetallic.shp',
                                keep_cols=['MetallicNonMetallicLeaseSubType',
                                           'LeaseIssueDate',
                                           'LeaseExpirationDate', 'CompanyName', 'LeaseStatusLabel', 'CompanyZipCode',
                                           'MineralTypeLabel'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas leases',
                                location='Wyoming_All/OilandGas.shp',
                                keep_cols=['LeaseIssueDate',
                                           'LeaseExpirationDate', 'CompanyName', 'LeaseStatusLabel', 'CompanyZipCode',
                                           'MineralTypeLabel'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Easements',
                                location='Wyoming_All/Easements.shp',
                                keep_cols=['oslisde.20', 'Leaseholder_LU', 'Issue_Date_LU', 'Expiration_Date_LU', 'Status_LU',
                                           'Sub_Group_LU',
                                           'Use_Type_LU'],
                                # can we use Easement + oslisde.20
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Grazing Lease',
                                location='Wyoming_All/Grazing.shp',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Special Use Lease',
                                location='Wyoming_All/SpecialUseLeases.shp',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU',
                                           'Type_LU', 'Purpose_LU'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Wind Lease',
                                location='Wyoming_All/Wind.shp',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU'],
                                is_restricted_activity=True,
                                use_name_as_activity=True)
    ]),
    'MT': StateForActivity(name='Montana', activities=[
        StateActivityDataSource(name='Oil and Gas Wells',
                                location='Montana_All/wells/wells.shp',
                                keep_cols=['CoName', 'Status', 'Type', 'Completed'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='miscellaneous',
                                location='https://gisservicemt.gov/arcgis/rest/services/MSDI_Framework/ManagedAreas/MapServer/0/query',
                                keep_cols=['MANAME', 'INST', 'UNITTYPE'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='Timber',
                                location='https://services2.arcgis.com/DRQySz3VhPgOv7Bo/ArcGIS/rest/services/FMB_Harvest_History/FeatureServer/1/query',
                                keep_cols=['HarvestPrescription', 'DateSold', 'DateClosed', 'LandOffice'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Lumber Mill',
                                location='https://services2.arcgis.com/DRQySz3VhPgOv7Bo/ArcGIS/rest/services/Active_Mills/FeatureServer/0/query',
                                keep_cols=['facilname', 'milltypeDe'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Coal Active Lease',
                                location='Montana_All/MMB_CoalActiveLease.shp',
                                keep_cols=['Prim_Cust', 'Producing', 'DateEffect', 'DateExpire'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Agriculture and Grazing',
                                location='Montana_All/AGMB_AgreementTracts.shp',
                                keep_cols=['Status'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Commercial Leases',
                                location='Montana_All/REMB_LeaseLots.shp',
                                keep_cols=['LeaseCateg'],
                                # include if Status is active
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and Gas Active Lease',
                                location='Montana_All/MMB_OilandGasActiveLease.shp',
                                keep_cols=['Prim_Cust', 'Producing', 'DateEffect', 'DateExpire'],
                                # is_restricted_subsurface_activity=True,
                                use_name_as_activity=True)])
}
