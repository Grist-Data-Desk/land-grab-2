from land_grab_2.stl_dataset.step_2.land_activity_search.entities import StateForActivity, StateActivityDataSource

REWRITE_RULES = {
    "id": {
        "Water Rights": {
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
            # "EasementPurpose": "Activity",
            # "Easement Purpose": "Activity",
            "Parties": "Lessee or Owner or Manager",
            "DteGranted": "Lease Start Date",
            "DteExpires": "Lease End Date"
        },
        "Timber": {
            "Sale_Status": "Activity"
        },
        "Oil and gas": {
            "Status": "Activity"
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
           # "T_LEASETYPE": "Activity",
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
        "Active Mineral Lease": {
            "T_LEASETYP": "Commodity",
            "T_PNAMES": "Lessee or Owner or Manager",
            "T_STARTDAT": "Lease Start Date",
            "T_EXPDATE": "Lease End Date",
            "ML_SU_LAND": "LandClass"
        },
        "Historic Mineral Lease": {
            "T_LEASETYP": "Commodity",
            "T_PNAMES": "Lessee or Owner or Manager",
            "T_STARTDAT": "Lease Start Date",
            "T_EXPDAT": "Lease End Date",
            "ML_SU_LAND": "LandClass"
        }
    },
    # "nd": {
    #     "Minerals": {
    #         "LEASE_STATUS": "Lease Status",
    #         "LESSEE": "Lessee or Owner or Manager",
    #         "LEASE_EFFECTIVE": "Lease Start Date",
    #         "LEASE_EXPIRATION": "Lease End Date",
    #         "LEASE_EXTENDED": "Lease Extension Date"
    #     },
    #     "Recreation": {
    #         "UNIT_NAME": "Sub-activity"
    #     }
    # },
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
        "Renewables": {
            "sitedescri": "Activity",
        },
        "Minerals": {
            "UnitTypeDescription": "Sub-Activity",
            "unittypede": "Activity"
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
        "Metallic and nonmetallic mineral lease": {
            "LeaseStatusLabel": "Lease Status",
            # "MineralTypeLabel": "Activity",
            # 'oslisde._8': 'Activity',
            'oslisde.OSLISDE.FC_MetallicNonMetallic.MetallicNonMetallicLeaseSubType': 'Activity',
            "MetallicNonMetallicLeaseSubType": "Sub-activity",
            "CompanyName": "Lessee or Owner or Manager",
            "CompanyZipCode": "Owner Address or Location",
            "LeaseIssueDate": "Lease Start Date",
            "LeaseExpirationDate": "Lease End Date"
        },
        "Oil and gas lease": {
            "LeaseStatusLabel": "Lease Status",
            # "MineralTypeLabel": "Activity",
            # 'oslisde.88': "Activity",
            "CompanyName": "Lessee or Owner or Manager",
            "CompanyZipCode": "Owner Address or Location",
            "LeaseIssueDate": "Lease Start Date",
            "LeaseExpirationDate": "Lease End Date"
        },
        "Easements": {
            "Status_LU": "Lease Status",
            # "Sub_Group_LU": "Activity",
            'oslisde.20': "Activity",
            # "Use_Type_LU": "Sub-activity",
            'oslisde.21': "Sub-activity",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Issue_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        },
        "Grazing lease": {
            "Status_LU": "Lease Status",
            "Leaseholder_LU": "Lessee or Owner or Manager",
            "Start_Date_LU": "Lease Start Date",
            "Expiration_Date_LU": "Lease End Date"
        },
        "Special use lease": {
            "Status_LU": "Lease Status",
            "oslisde.19": "Activity",
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
        "Metallic minerals": {
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
        "Non-metallic minerals": {
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
        "Coal lease": {
            "AllotName": "Sub-activity",
            "Manager": "Lessee or Owner or Manager"
        },
        "Development lease": {
            "app_descr": "Activity",
        },
        "Grazing lease": {
            "app_descr": "Activity",
        },
        "Other minerals": {
            "app_descr": "Activity",
        },
        "Renewables": {
            "app_descr": "Activity",
        },
        "Special use lease": {
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
        "Commercial lease": {
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
        "Oil and gas lease": {
            "STATUS": "Lease Status",
            "OGRID_NAM": "Lessee or Owner or Manager",
            "VEREFF_DTE": "Lease Start Date",
            "VERTRM_DTE": "Lease End Date"
        },
        "Rights of way lease": {
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
        "Agriculture and grazing": {
            "Status": "Lease Status",
            "TractType": "Activity"
        },
        "Commercial lease": {
            "LeaseCateg": "Activity"
        },
        "Coal active lease": {
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
        "Conservation Easement": {
            "PROGRAM_NA": "Activity"
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
                                use_name_as_activity=False,
                                is_misc = True),
        StateActivityDataSource(name='Minerals',
                                location='Arizona_All/Minerals.shp',
                                keep_cols=['leased', 'ke', 'effdate', 'expdate', 'full_name'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas',
                                location='Arizona_All/OilGas.shp',
                                keep_cols=['type', 'leased', 'effdate',
                                           'expdate',
                                           'full_name'],
                                is_restricted_subsurface_activity=True,
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
                                use_name_as_activity=False,
                                is_misc = True)

    ]),
    'ID': StateForActivity(name='idaho', activities=[
        StateActivityDataSource(name='misc',
                                location='Idaho_All/Miscellaneous.shp',
                                keep_cols=['TypeGroup', 'Type', 'Status', 'DteGranted', 'DteExpires', 'Name',
                                           'Commodities'],
                                use_name_as_activity=False,
                                is_misc = True),
        StateActivityDataSource(name='Easements',
                                location='Idaho_All/Easements.shp',
                                keep_cols=['TypeGroup', 'Status', 'DteGranted', 'DteExpires', 'Parties',
                                           'EasementRight', 'EasementPu'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Timber',
                                location='Idaho_All/Timber.shp',
                                keep_cols=['Sale_Statu'],
                                is_restricted_activity=True,
                                activity_name_appendage_col='Sale_Statu',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Idaho_All/OilGas.shp',
                                keep_cols=['Status'],
                                activity_name_appendage_col='Status',
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Water Rights',
                                location='Idaho_All/Water.shp',
                                keep_cols=['TypeGroup', 'Status', 'WaterUse', 'Source'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),

    ]),
    'MN': StateForActivity(name='minnesota', activities=[
        StateActivityDataSource(name='Peat Lease',
                                location='Minnesota_All/shp_plan_state_peatleases/active_peatLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
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
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Conservation Easement',
                                location='Minnesota_All/shp_plan_stateland_dnrcounty/stateland_interest_conservationeasement.shp',
                                keep_cols=['EASETYPE'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active NonFerrous Mineral Lease',
                                location='Minnesota_All/ActiveNonFerrous.shp',
                                keep_cols=['T_LEASETYPE'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic NonFerrous Mineral Lease',
                                location='Minnesota_All/HistoricNonFerrous.shp',
                                keep_cols=['T_LEASETYPE'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active Mineral Lease',
                                location='Minnesota_All/shp_plan_state_minleases/active_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic Mineral Lease',
                                location='Minnesota_All/shp_plan_state_minleases/historic_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True)

    ]),
    # 'ND': StateForActivity(name='north dakota', activities=[
    #     StateActivityDataSource(name='Minerals',
    #                             location='NorthDakota_All/Minerals.shp',
    #                             keep_cols=['LEASE_STATUS', 'LEASE_EFFECTIVE', 'LEASE_EXPIRATION', 'LEASE_EXTENDED',
    #                                        'LESSEE'],
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Recreation',
    #                             location='NorthDakota_All/Recreation.shp',
    #                             keep_cols=['UNIT_NAME'],
    #                             is_restricted_activity=True,
    #                             use_name_as_activity=True),
    #
    # ]),
    'NM': StateForActivity(name='new mexico', activities=[
        StateActivityDataSource(name='Agriculture',
                                location='NewMexico_All/Ag_Leases',
                                use_name_as_activity=True,
                                is_restricted_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM']),
        StateActivityDataSource(name='Commercial lease',
                                location='NewMexico_All/Commercial_Leases',
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM', 'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Energy',
                                location='NewMexico_All/Energy_Leases',
                                use_name_as_activity=False,
                                is_restricted_activity=True,
                                keep_cols=['STATUS', 'LEASE_TYPE',
                                           'OGRID_NAM']),
        StateActivityDataSource(name='Minerals',
                                location='NewMexico_All/Mineral_Leases',
                                use_name_as_activity=False,
                                is_restricted_subsurface_activity=True,
                                keep_cols=['STATUS', 'LEASE_TYPE', 'OGRID_NAM', 'SUB_TYPE',
                                           'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Oil and gas lease',
                                location='NewMexico_All/OilGas_Leases',
                                use_name_as_activity=True,
                                is_restricted_subsurface_activity=True,
                                keep_cols=['STATUS', 'VEREFF_DTE', 'VERTRM_DTE', 'OGRID_NAM']),
        StateActivityDataSource(name='Oil and gas lease',
                                location='NewMexico_All/OilGas_State_Leases/OG_Leases_Intersect.shp',
                                use_name_as_activity=True,
                                is_restricted_subsurface_activity=True,
                                keep_cols=['STATUS', 'VEREFF_DTE', 'VERTRM_DTE', 'OGRID_NAM']),
        StateActivityDataSource(name='Rights of way lease',
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
                                use_name_as_activity=False,
                                is_misc = True),
        # StateActivityDataSource(name='Minerals',
        #                         location='Oklahoma_All/Minerals.shp',
        #                         keep_cols=['BeginDate', 'EndDate', 'OwnerName', 'Address2'],
        #                         is_restricted_subsurface_activity=True,
        #                         use_name_as_activity=True),
        # StateActivityDataSource(name='Agriculture',
        #                         location='Oklahoma_All/Miscellaneous.shp',
        #                         keep_cols=['LeaseType', 'BeginDate', 'EndDate', 'OwnerName',
        #                                    'Address2'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=False),

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
                                location='Texas_All/Coastal_Leases_Poly/Coastal_Leases_Poly.shp',
                                keep_cols=['PROJECT_NA', 'GRANTEE', 'ACTIVITY_T'],
                                use_name_as_activity=False),
        StateActivityDataSource(name='misc',
                                location='Texas_All/Misc_Easements/Misc_Easements.shp',
                                keep_cols=['LEASE_STAT', 'PRIMARY_LE',
                                           'ALL_LESSEE', 'PURPOSE'],
                                use_name_as_activity=False,
                                is_misc = True),
        StateActivityDataSource(name='Hard Minerals',
                                location='Texas_All/Hard_Minerals/Hard_Minerals.shp',
                                keep_cols=['LEASE_STAT', 'ORIGINAL_L', 'EFFECTIVE_'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Texas_All/OAG_Leases_Active/OAG_Leases_Active.shp',
                                keep_cols=['LEASE_STAT', 'EFFECTIVE_', 'ORIGINAL_L', 'LESSOR'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),

        StateActivityDataSource(name='Fracking Pond',
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
                                keep_cols=['unittypede'],
                                is_restricted_subsurface_activity=True,
                                activity_name_appendage_col='unittypede',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas lease',
                                location='Texas_All/PUF-OilGasLease.shp',
                                keep_cols=['leasestatu'],
                                is_restricted_subsurface_activity=True,
                                activity_name_appendage_col='leasestatu',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas Wellbores',
                                location='Texas_All/PUF-OilGasWellbores.shp',
                                keep_cols=['cycle'],
                                is_restricted_subsurface_activity=True,
                                activity_name_appendage_col='cycle',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas Well Bottom Hole',
                                location='Texas_All/PUF-WellBottomHole.shp',
                                keep_cols=['cycle'],
                                is_restricted_subsurface_activity=True,
                                activity_name_appendage_col='cycle',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Renewables',
                                location='Texas_All/PUF-Renewables.shp',
                                keep_cols=['sitedescri'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        # StateActivityDataSource(name='Renewable Tracts',
        #                         location='Texas_All/PUF-Renewables.shp',
        #                         keep_cols=['FIRST_sitedescription'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=False),
        StateActivityDataSource(name='Well Bottom Hole',
                                location='Texas_All/PUF-WellBottomHole.shp',
                                keep_cols=['cycle'],
                                is_restricted_subsurface_activity=True,
                                activity_name_appendage_col='cycle',
                                use_name_as_activity=True),

    ]),
    'UT': StateForActivity(name='utah', activities=[
        # StateActivityDataSource(name='Water',
        #                         location='Utah_All/Utah_Water_Related_Land_Use',
        #                         keep_cols=['Descriptio',
        #                                    'LU_Group'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=True),

        StateActivityDataSource(name='Coal contract',
                                location='Utah_All/Contracts_Coal/Contracts_Coal.shp',
                                keep_cols=['app_descr'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Development lease',
                                location='Utah_All/Contracts_Dev_Lease/Contracts_Dev_Lease.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Grazing lease',
                                location='Utah_All/Contracts_Dev_Lease/Contracts_Dev_Lease.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil shale contract',
                                location='Utah_All/Contracts_Oil_Shale/Contracts_Oil_Shale.shp',
                                keep_cols=['app_descr'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Other minerals',
                                location='Utah_All/Contracts_Other_Mineral/Contracts_Other_Mineral.shp',
                                keep_cols=['app_descr'],
                                is_restricted_subsurface_activity=True,
                                activity_name_appendage_col='app_descr',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Renewables',
                                location='Utah_All/Contracts_Renewable/Contracts_Renewable.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                activity_name_appendage_col='app_descr',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Range improvement project contract',
                                location='Utah_All/Contracts_Rip/Contracts_Rip.shp',
                                keep_cols=['app_descr'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Sand gravel contract',
                                location='Utah_All/Contracts_Sand_Gravel/Contracts_Sand_Gravel.shp',
                                keep_cols=['app_descr'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Tar sand contract',
                                location='Utah_All/Contracts_Sula/Contracts_Sula.shp',
                                keep_cols=['app_descr'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Special use lease',
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
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='OilGasOther',
                                location='Utah_All/OilGasOther.shp',
                                keep_cols=['app_descr'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        #
        # StateActivityDataSource(name='Geothermal',
        #                         location='Utah_All/Utah_UREZ_Phase_2_Geothermal',
        #                         keep_cols=[],
        #                         use_name_as_activity=True),
        StateActivityDataSource(name='Wind zone',
                                location='Utah_All/Utah_UREZ_Phase_1_Wind_Zones',
                                keep_cols=[],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Solar zone',
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
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas fields',
                                location='Utah_All/Utah_Oil_and_Gas_Fields-shp',
                                keep_cols=['STATUS'],
                                is_restricted_subsurface_activity=True,
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
                                use_name_as_activity=False,
                                is_misc = True),
        StateActivityDataSource(name='Non-metallic minerals',
                                location='Washington_All/NonMetallicMinerals.shp',
                                keep_cols=['MINERAL'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Metallic minerals',
                                location='Washington_All/MetallicMinerals.shp',
                                keep_cols=['COMMODITIE', 'PRODUCTION', 'ORE_MINERA'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active Surface Mine Permit Site',
                                location='Washington_All/Active_Surface_Mine_Permit_Sites.shp',
                                keep_cols=['APPLICANT_', 'MINE_NAME', 'COMMODITY_'],
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas',
                                location='Washington_All/OilGasWells.shp',
                                keep_cols=['COMPANY_NA', 'WELL_STATU'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Coal',
                                location='Washington_All/Coal.shp',
                                keep_cols=[],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),

    ]),
    'WI': StateForActivity(name='wisconsin', activities=[
        StateActivityDataSource(name='misc',
                                location='Wisconsin_All/Miscellaneous.shp',
                                keep_cols=['PROP_NAME'],
                                is_restricted_activity=True,
                                use_name_as_activity=False,
                                is_misc = True),
        StateActivityDataSource(name='Conservation Easement',
                                location='Wisconsin_All/Conservation_Easement.shp',
                                keep_cols=['PROGRAM_NA'],
                                activity_name_appendage_col='PROGRAM_NA',
                                use_name_as_activity=True),
        StateActivityDataSource(name='DNR Easement',
                                location='Wisconsin_All/DNR_Easement.shp',
                                keep_cols=['EASE_USE_C'],
                                activity_name_appendage_col='EASE_USE_C',
                                use_name_as_activity=True),
        StateActivityDataSource(name='DNR Owned',
                                location='Wisconsin_All/DNR_Owned.shp',
                                keep_cols=['EASE_USE_C'],
                                activity_name_appendage_col='EASE_USE_C',
                                use_name_as_activity=True)
    ]),
    'WY': StateForActivity(name='wyoming', activities=[
        StateActivityDataSource(name='Metallic and nonmetallic mineral lease',
                                location='Wyoming_All/MetallicNonMetallic.shp',
                                keep_cols=['MetallicNonMetallicLeaseSubType',
                                           'LeaseIssueDate',
                                           'oslisde.OSLISDE.FC_MetallicNonMetallic.MetallicNonMetallicLeaseSubType',
                                           'LeaseExpirationDate', 'CompanyName', 'LeaseStatusLabel', 'CompanyZipCode',
                                           'MineralTypeLabel'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas lease',
                                location='Wyoming_All/OilGasLease.shp',
                                keep_cols=['LeaseIssueDate',
                                           'LeaseExpirationDate', 'CompanyName', 'LeaseStatusLabel', 'CompanyZipCode',
                                           'MineralTypeLabel'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Easements',
                                location='Wyoming_All/Easements.shp',
                                keep_cols=['oslisde.20', 'Leaseholder_LU', 'Issue_Date_LU', 'Expiration_Date_LU',
                                           'Status_LU',
                                           'Sub_Group_LU',
                                           'Use_Type_LU'],
                                activity_name_appendage_col='oslisde.20',
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Grazing lease',
                                location='Wyoming_All/Grazing.shp',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Special use lease',
                                location='Wyoming_All/SpecialUseLeases.shp',
                                keep_cols=['oslisde.19','Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU',
                                           'Type_LU', 'Purpose_LU'],
                                activity_name_appendage_col='oslisde.19',
                                use_name_as_activity=True,
                                is_misc = True),
        StateActivityDataSource(name='Wind lease',
                                location='Wyoming_All/Wind.shp',
                                keep_cols=['Leaseholder_LU', 'Start_Date_LU', 'Expiration_Date_LU', 'Status_LU'],
                                is_restricted_activity=True,
                                use_name_as_activity=True)
    ]),
    'MT': StateForActivity(name='Montana', activities=[
        StateActivityDataSource(name='Oil and gas well',
                                location='Montana_All/wells/wells.shp',
                                keep_cols=['CoName', 'Status', 'Type', 'Completed'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='miscellaneous',
                                location='Montana_All/ManagedAreas.shp',
                                keep_cols=['MANAME', 'INST', 'UNITTYPE'],
                                use_name_as_activity=False,
                                is_misc = True),
        StateActivityDataSource(name='Timber',
                                location='Montana_All/FMB_HarvestHistory.shp',
                                keep_cols=['HarvestPrescription', 'DateSold', 'DateClosed', 'LandOffice'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Lumber mill',
                                location='Montana_All/Mills.shp',
                                keep_cols=['facilname', 'milltypeDe'],
                                is_restricted_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Coal active lease',
                                location='Montana_All/MMB_CoalActiveLease.shp',
                                keep_cols=['Prim_Cust', 'Producing', 'DateEffect', 'DateExpire'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Agriculture and grazing',
                                location='Montana_All/AGMB_AgreementTracts.shp',
                                keep_cols=['TractType'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Commercial lease',
                                location='Montana_All/REMB_LeaseLots.shp',
                                keep_cols=['LeaseCateg', 'LeaseStatu'],
                                is_restricted_activity=True,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas active lease',
                                location='Montana_All/MMB_OilandGasActiveLease.shp',
                                keep_cols=['Prim_Cust', 'Producing', 'DateEffect', 'DateExpire'],
                                is_restricted_subsurface_activity=True,
                                use_name_as_activity=True)])
}
