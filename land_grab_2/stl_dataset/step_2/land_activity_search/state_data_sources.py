from land_grab_2.stl_dataset.step_2.land_activity_search.entities import StateForActivity, StateActivityDataSource, \
    RightsType

REWRITE_RULES = {
    "id": {
        "Water Rights": {
            "TypeGroup": "Rights-Type",
            "Status": "lease_status",
            "WaterUse": "Sub-activity",
            "Source": "Source"
        },
        "Easements": {
            "EasementRi": "Rights-Type",
            "EasementRight": "Rights-Type",
            "TypeGroup": "Transaction Type",
            "StatusGrp": "lease_status",
            "EasementPu": "Activity",
            # "EasementPurpose": "Activity",
            # "Easement Purpose": "Activity",
            "Parties": "lessee",
            "DteGranted": "Lease Start Date",
            "DteExpires": "Lease End Date"
        },
        "Timber Sale": {
            "Sale_Statu": "lease_status"
        },
        "Active oil and gas well": {
            "Status": "lease_status",
            "OPERATOR": "lessee"
        },
        "Inactive oil and gas well": {
            "Status": "lease_status",
            "OPERATOR": "lessee"
        },
        "Misc": {
            "TypeGroup": "Transaction Type",
            "Status": "lease_status",
            "Type": "Activity",
            "Commodities": "Commodity",
            "Name": "lessee",
            "DteGranted": "Lease Start Date",
            "DteExpires": "Lease End Date"
        }
    },
    "co": {
        "Misc": {
            "Transactio": "Transaction Type",
            "Lease_Stat": "lease_status",
            "Lease_Type": "Activity",
            "Lease_Subt": "Sub-activity",
            "Lessee_Nam": "lessee",
            "Lease_Star": "Lease Start Date",
            "Lease_End_": "Lease End Date"
        }
    },
    "mn": {
        "Aggregate Minerals": {
            "Status_1": "lease_status",
            "Type": "Sub-activity",
            "Status_2": "Use Purpose"
        },
        "Sand and Gravel Potential Location": {
            "CLASS": "lease_status",
        },
        "Crushed Stone Potential Location": {
            "CLASS": "lease_status",
        },
        "Active Peat Lease": {
           # "T_LEASETYPE": "Activity",
            "T_PNAMES": "lessee",
            "T_STARTDAT": "Lease Start Date",
            "T_EXPDATE": "Lease End Date"
        },
        "Historic Peat Lease": {
            # "T_LEASETYPE": "Activity",
            "T_PNAMES": "lessee",
            "T_STARTDAT": "Lease Start Date",
            "T_EXPDATE": "Lease End Date"
        },
        "Conservation Easement": {
            "EASETYPE": "Sub-activity"
        },
        "Active NonFerrous Mineral Lease": {
            "T_LEASETYPE": "Activity",
            "T_PNAMES": "lessee"
        },
        "Historic NonFerrous Mineral Lease": {
            "T_LEASETYPE": "Activity",
            "T_PNAMES": "lessee"
        },
        "Recreation": {
            "AREA_NAME": "Sub-activity",
            "AREA_TYPE": "Activity"
        },
        "Recreation-DNR Managed": {
            "UNIT_NAME": "Sub-activity",
            "UNIT_TYPE": "Activity",
        },
        "Active Mineral Lease": {
            "T_LEASETYP": "Commodity",
            "T_PNAMES": "lessee",
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
    "nd": {
        "Oil/gas well - ": {
            "status": "lease_status",
            "operator": "lessee",
        },
        "Oil and gas lease": {
            "LEASE_STAT": "lease_status",
            "LESSEE": "lessee",
        },
        "Gas plant": {
            "status": "lease_status",
            "operator": "lessee",
        },
    },
    "ne": {
        "Water": {
            "RightStatu": "lease_status",
            "RightUse": "Sub-activity",
            "FirstName": "lessee",
            "LastName": "Lessee Name 2"
        },
        "Recreation": {
            "Status": "lease_status",
            "AreaName": "Sub-activity",
            "StartDate": "Lease Start Date"
        }
    },
    "ok": {
        "Misc": {
            "EasementTy": "lease_status",
            "Purpose": "Activity",
            "Grantee": "lessee"
        },
        "Agriculture": {
            "LeaseType": "Activity",
            "OwnerName": "lessee",
            "Address2": "Owner Address or Location",
            "BeginDate": "Lease Start Date",
            "EndDate": "Lease End Date"
        },
        "Minerals": {
            "OwnerName": "lessee",
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
            "LEASE_STAT": "lease_status",
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
        "Misc": {
            "leased": "lease_status",
            "ke": "Activity",
            "full_name": "lessee",
            "effdate": "Lease Start Date",
            "expdate": "Lease End Date"
        },
        "Minerals": {
            "leased": "lease_status",
            "ke": "Activity",
            "full_name": "lessee",
            "effdate": "Lease Start Date",
            "expdate": "Lease End Date"
        },
        "Oil and gas": {
            "leased": "lease_status",
            "ke": "Activity",
            "full_name": "lessee",
            "effdate": "Lease Start Date",
            "expdate": "Lease End Date"
        },
        "Subsurface Activities": {
            "leased": "lease_status",
            "ke": "Activity",
            "full_name": "lessee"
        },
        "Surface Activities": {
            "leased": "lease_status",
            "ke": "Activity",
            "full_name": "lessee"
        },
        # "Agriculture": {
        #     "name": "Sub-activity"
        # },
        "Solar": {
            "status": "lease_status",
            "technology": "Sub-activity",
            "projectnam": "lessee"
        }
    },
    "wy": {
        "Oil and gas active lease": {
            "oslisde.62": "lease_status",
            "oslisde.73": "lessee",
        },
        "Metallic and nonmetallic mineral active lease - ": {
            "oslisde.64": "lease_status",
            "oslisde.75": "lessee",
        },
        "Easements": {
            "oslisde.13": "lease_status",
            "oslisde.41": "lessee",
        },
        "Grazing lease": {
            "oslisde.12": "lease_status",
            "oslisde.31": "lessee",
        },
        "Special use lease": {
            "oslisde.13": "lease_status",
            "oslisde.34": "lessee",
        },
        "Wind Lease": {
            "oslisde.13": "lease_status",
            "oslisde.38": "lessee",
        },
        "WSGS Oil and gas well": {
            "STATUS": "lease_status",
            "COMPANY": "lessee",
        }
    },
    "wa": {
        "Metallic minerals": {
            "ORE_MINERA": "Sub-activity",
        },
        "Oil and gas": {
            "WELL_STATU": "lease_status",
            "COMPANY_NA": "lessee"
        },
        "Active Surface Mine Permit Sites": {
            "MINE_NAME": "Sub-activity",
            "COMMODITY_": "Commodity",
            "APPLICANT_": "lessee"
        },
        "Current Leases": {
            "AGREEMENT1": "Activity"
        }
    },
    "ut": {
        "Coal contract": {
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Development lease": {
            "app_descr": "Activity",
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Grazing contract - ": {
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Oil shale contract": {
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Other minerals contract - ": {
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Renewables": {
            "app_descr": "Activity",
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Range improvement project contract - ": {
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Sand gravel contract": {
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Tar sand contract": {
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Special use contract - ": {
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Easements": {
            "app_descr": "Activity",
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Oil and gas contract - ": {
            "app_descr": "Activity",
            "record_sta": "lease_status",
            "customer_n": "lessee",
        },
        "Historic/Past Uranium Production": {
            "OWNER": "lessee",
        },
        "Oil and gas wells": {
            "Operator": "lessee",
            "WellStatus": 'lease_status'
        },
        "Oil and gas well bottom hole": {
            "ConstructS": 'lease_status'
        },
    },
    "nm": {
        "Agriculture": {
            "STATUS": "lease_status",
            "OGRID_NAM": "lessee"
        },
        "Commercial lease": {
            "STATUS": "lease_status",
            "OGRID_NAM": "lessee",
            "VEREFF_DTE": "Lease Start Date",
            "VERTRM_DTE": "Lease End Date"
        },
        "Energy": {
            "STATUS": "lease_status",
            "LEASE_TYPE": "Activity",
            "OGRID_NAM": "lessee"
        },
        "Mineral lease": {
            "STATUS": "lease_status",
            # "LEASE_TYPE": "Activity",
            "SUB_TYPE": "Sub-activity",
            "OGRID_NAM": "lessee",
            "VEREFF_DTE": "Lease Start Date",
            "VERTRM_DTE": "Lease End Date"
        },
        "Oil and gas lease": {
            "STATUS": "lease_status",
            "OGRID_NAM": "lessee",
            "VEREFF_DTE": "Lease Start Date",
            "VERTRM_DTE": "Lease End Date"
        },
        "Oil and gas lease - layer 2": {
            "STATUS": "lease_status",
            "OGRID_NAM": "lessee",
        },
        "Rights of way lease": {
            "STATUS": "lease_status",
            "OGRID_NAM": "lessee"
        }
    },
    "mt": {
        "Misc": {
            "UNITTYPE": "Activity",
            "MANAME": "Sub-activity",
            "INST": "lessee"
        },
        "Oil and gas well": {
            "Status": "lease_status",
            "Type": 'Sub-activity',
            "CoName": "lessee",
            "Completed": "Lease End Date"
        },
        "Timber Harvest Sale": {
            "HarvestPrescription": "Sub-activity",
            "DateSold": "Lease Start Date",
            "DateClosed": "Lease End Date"
        },
        "Lumber Mill": {
            "facilname": "lessee",
            "milltypeDe": "Sub-activity"
        },
        "Oil and gas active lease": {
            "Prim_Cust": "lessee",
            "Producing": "lease_status",
            "DateEffect": "Lease Start Date",
            "DateExpire": "Lease End Date"
        },
        "Agriculture and grazing": {
            "Status": "lease_status",
            "TractType": "Activity"
        },
        "Commercial lease": {
            "LeaseCateg": "Activity",
            "LeaseStatu": "lease_status"
        },
        "Coal active lease": {
            "Prim_Cust": "lessee",
            "Producing": "lease_status",
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
        },
        "Spill Site - ": {
            "resp_party": "lessee",
            "status": "lease_status",
        },
        "Oil/gas well - ": {
            "Well_Admin": "lease_status",
            "Operator": "lessee",
        },
        "Construction Aggregate and Mining - ": {
            "sitestatus": "lease_status",
            "operator": "lessee",
        }
    },
}
STATE_ACTIVITIES = {
    'AZ': StateForActivity(name='arizona', activities=[
        StateActivityDataSource(name='Misc',
                                location='Arizona_All/Miscellaneous.shp',
                                keep_cols=['leased', 'ke', 'effdate', 'expdate', 'full_name'],
                                rights_type=RightsType.NEEDS_LOOKUP,
                                use_name_as_activity=False,
                                ),
        StateActivityDataSource(name='Minerals',
                                location='Arizona_All/Minerals.shp',
                                keep_cols=['leased', 'ke', 'effdate', 'expdate', 'full_name'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas',
                                location='Arizona_All/OilGas.shp',
                                keep_cols=['type', 'leased', 'effdate',
                                           'expdate',
                                           'full_name'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=False),
        # StateActivityDataSource(name='Subsurface Activities',
        #                         location='Arizona_All/All-AZ-Mineral-STLs-Fixed.shp',
        #                         keep_cols=['ke', 'leased', 'full_name'],
        #                         rights_type=RightsType.SUBSURFACE,
        #                         use_name_as_activity=False),
        # StateActivityDataSource(name='Surface Activities',
        #                         location='Arizona_All/AZ_Surface_TEST.shp',
        #                         keep_cols=['ke', 'leased', 'full_name'],
        #                         rights_type=RightsType.SURFACE,
        #                         use_name_as_activity=False),
        # Took out this layer because ag is reflected in Misc.
        # StateActivityDataSource(name='Agriculture',
        #                         location='Arizona_All/Grazing.shp',
        #                         keep_cols=['name'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=True),
        StateActivityDataSource(name='Solar',
                                location='Arizona_All/Solar.shp',
                                keep_cols=['technology', 'projectnam', 'status'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
    ]),
    'CO': StateForActivity(name='colorado', activities=[
        StateActivityDataSource(name='Misc',
                                location='Colorado_All/Miscellaneous.shp',
                                keep_cols=['Transaction Type', 'Lease Type', 'Lease Subtype', 'Lessee Name',
                                           'Lease State Date',
                                           'Lease End Date', 'Lease Status'],
                                use_name_as_activity=False,
                                rights_type=RightsType.UNIVERSAL,
                                )

    ]),
    'ID': StateForActivity(name='idaho', activities=[
        StateActivityDataSource(name='Misc',
                                location='Idaho_All/Miscellaneous.shp',
                                keep_cols=['TypeGroup', 'Type', 'Status', 'DteGranted', 'DteExpires', 'Name',
                                           'Commodities'],
                                use_name_as_activity=False,
                                rights_type=RightsType.NEEDS_LOOKUP,
                                ),
        StateActivityDataSource(name='Easements',
                                location='Idaho_All/Easements.shp',
                                keep_cols=['TypeGroup', 'Status', 'DteGranted', 'DteExpires', 'Parties',
                                           'EasementRight', 'StatusGrp', 'EasementPu'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Timber Sale',
                                location='Idaho_All/Timber.shp',
                                keep_cols=['Sale_Statu'],
                                rights_type=RightsType.SURFACE,
                                # activity_name_appendage_col='Sale_Statu', changed this so it could fit with
                                # lease status
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active oil and gas well',
                                location='Idaho_All/OilGas.shp',
                                keep_cols=['Status', 'OPERATOR'],
                                # activity_name_appendage_col='Status', same as above
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Inactive oil and gas well',
                                location='Idaho_All/OilGas.shp',
                                keep_cols=['Status', 'OPERATOR'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Water Rights',
                                location='Idaho_All/Water.shp',
                                keep_cols=['TypeGroup', 'Status', 'WaterUse', 'Source'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),

    ]),
    'MN': StateForActivity(name='minnesota', activities=[
        StateActivityDataSource(name='Active Peat Lease',
                                location='Minnesota_All/shp_plan_state_peatleases/active_peatLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic Peat Lease',
                                location='Minnesota_All/shp_plan_state_peatleases/historic_peatLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Recreation',
                                location='Minnesota_All/shp_bdry_dnr_managed_areas/dnr_stat_plan_areas.shp',
                                keep_cols=['AREA_NAME', 'AREA_TYPE'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Recreation-DNR Managed',
                                location='Minnesota_All/shp_bdry_dnr_managed_areas/dnr_management_units.shp',
                                keep_cols=['UNIT_NAME', 'UNIT_TYPE', 'ADMINISTRA'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Aggregate Minerals',
                                location='Minnesota_All/shp_geos_aggregate_mapping/armp_aggmines.shp',
                                keep_cols=['Type', 'Status_1', 'Status_2'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='Type',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Sand and Gravel Potential Location',
                                location='Minnesota_All/shp_geos_aggregate_mapping/armp_sandandgravelpotential.shp',
                                keep_cols=['CLASS'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Crushed Stone Potential Location',
                                location='Minnesota_All/shp_geos_aggregate_mapping/armp_crushedstonepotential.shp',
                                keep_cols=['CLASS'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Conservation Easement',
                                location='Minnesota_All/shp_plan_stateland_dnrcounty/stateland_interest_conservationeasement.shp',
                                keep_cols=['EASETYPE'],
                                activity_name_appendage_col='EASETYPE',
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active NonFerrous Mineral Lease',
                                location='Minnesota_All/ActiveNonFerrousMineralLeases.shp',
                                keep_cols=['T_LEASETYPE', 'T_PNAMES'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic NonFerrous Mineral Lease',
                                location='Minnesota_All/HistoricNonFerrousMineralLeases.shp',
                                keep_cols=['T_LEASETYPE', 'T_PNAMES'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active Mineral Lease',
                                location='Minnesota_All/shp_plan_state_minleases/active_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                activity_name_appendage_col='T_LEASETYP',
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic Mineral Lease',
                                location='Minnesota_All/shp_plan_state_minleases/historic_minLeases.shp',
                                keep_cols=['T_LEASETYP', 'T_STARTDAT', 'T_EXPDATE', 'T_PNAMES', 'ML_SU_LAND'],
                                activity_name_appendage_col='T_LEASETYP',
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True)

    ]),
    'ND': StateForActivity(name='north dakota', activities=[
        StateActivityDataSource(name='Gas plant',
                                location='NorthDakota_All/ND-GasPlants.shp',
                                keep_cols=['operator', 'status'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil/gas well - ',
                                location='NorthDakota_All/ND-Wells.shp',
                                keep_cols=['operator', 'well_type', 'status'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='well_type',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil field',
                                location='NorthDakota_All/ND-OilFields.shp',
                                keep_cols=['name'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        # StateActivityDataSource(name='Oil and gas lease',
        #                         location='NorthDakota_All/ND-OilGasLease.shp',
        #                         keep_cols=['LEASE_STAT', 'LESSEE'],
        #                         rights_type=RightsType.SUBSURFACE,
        #                         use_name_as_activity=True),
        StateActivityDataSource(name='Oil/gas directional well',
                                location='NorthDakota_All/ND-DirectionalWell.shp',
                                keep_cols=['well_sub'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),

    ]),
    'NM': StateForActivity(name='new mexico', activities=[
        StateActivityDataSource(name='Agriculture',
                                location='NewMexico_All/Ag_Leases/slo_agleased.shp',
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM']),
        StateActivityDataSource(name='Commercial lease',
                                location='NewMexico_All/Commercial_Leases/slo_cmleased.shp',
                                rights_type=RightsType.UNIVERSAL,
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM', 'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Energy',
                                location='NewMexico_All/Energy_Leases/slo_enleased.shp',
                                use_name_as_activity=False,
                                rights_type=RightsType.SURFACE,
                                keep_cols=['STATUS', 'LEASE_TYPE',
                                           'OGRID_NAM']),
        StateActivityDataSource(name='Mineral lease',
                                location='NewMexico_All/Mineral_Leases/slo_mnleased.shp',
                                use_name_as_activity=True,
                                activity_name_appendage_col='LEASE_TYPE',
                                rights_type=RightsType.SUBSURFACE,
                                keep_cols=['STATUS', 'LEASE_TYPE', 'OGRID_NAM', 'SUB_TYPE',
                                           'VEREFF_DTE', 'VERTRM_DTE']),
        StateActivityDataSource(name='Oil and gas lease',
                                location='NewMexico_All/OilGas_Leases/slo_ogleased.shp',
                                use_name_as_activity=True,
                                rights_type=RightsType.SUBSURFACE,
                                keep_cols=['STATUS', 'VEREFF_DTE', 'VERTRM_DTE', 'OGRID_NAM']),
        StateActivityDataSource(name='Oil and gas lease - layer 2',
                                location='NewMexico_All/OilGas_State_Leases/OG_Leases_Intersect.shp',
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'VEREFF_DTE', 'VERTRM_DTE', 'OGRID_NAM']),
        StateActivityDataSource(name='Rights of way lease',
                                location='NewMexico_All/slo_rwleased/slo_rwleased.shp',
                                rights_type=RightsType.UNIVERSAL,
                                use_name_as_activity=True,
                                keep_cols=['STATUS', 'OGRID_NAM']),

    ]),
    'OK': StateForActivity(name='oklahoma', activities=[
        StateActivityDataSource(name='Misc',
                                location='Oklahoma_All/Miscellaneous.shp',
                                keep_cols=['Purpose', 'Grantee',
                                           'EasementTy'],
                                rights_type=RightsType.UNIVERSAL,
                                use_name_as_activity=False,
                                ),
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
                                location='SouthDakota_All/Parks_And_Recreation_Areas.shp',
                                keep_cols=['ParkName'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Spill Site - ',
                                location='SouthDakota_All/SD-spills.shp',
                                keep_cols=['site_name', 'spill_cat', 'status', 'resp_party'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True,
                                activity_name_appendage_col='spill_cat'),
        StateActivityDataSource(name='Oil/gas well - ',
                                location='SouthDakota_All/SD-oil-gas-permits-wells.shp',
                                keep_cols=['Operator', 'Well_Type_', 'Well_Admin'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True,
                                activity_name_appendage_col='Well_Type_'),
        StateActivityDataSource(name='Construction Aggregate and Mining - ',
                                location='SouthDakota_All/SD-ConAggSites.shp',
                                keep_cols=['operator', 'type', 'sitestatus'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True,
                                activity_name_appendage_col='type'),


    ]),
    # 'TX': StateForActivity(name='texas', activities=[
    #     StateActivityDataSource(name='Coastal',
    #                             location='Texas_All/Coastal_Leases_Poly/Coastal_Leases_Poly.shp',
    #                             keep_cols=['PROJECT_NA', 'GRANTEE', 'ACTIVITY_T'],
    #                             use_name_as_activity=False),
    #     StateActivityDataSource(name='misc',
    #                             location='Texas_All/Misc_Easements/Misc_Easements.shp',
    #                             keep_cols=['LEASE_STAT', 'PRIMARY_LE',
    #                                        'ALL_LESSEE', 'PURPOSE'],
    #                             use_name_as_activity=False,
    #                             is_misc = True),
    #     StateActivityDataSource(name='Hard Minerals',
    #                             location='Texas_All/Hard_Minerals/Hard_Minerals.shp',
    #                             keep_cols=['LEASE_STAT', 'ORIGINAL_L', 'EFFECTIVE_'],
    #                             is_restricted_subsurface_activity=True,
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Oil and gas',
    #                             location='Texas_All/OAG_Leases_Active/OAG_Leases_Active.shp',
    #                             keep_cols=['LEASE_STAT', 'EFFECTIVE_', 'ORIGINAL_L', 'LESSOR'],
    #                             is_restricted_subsurface_activity=True,
    #                             use_name_as_activity=True),
    #
    #     StateActivityDataSource(name='Fracking Pond',
    #                             location='Texas_All/PUF-FracPonds.shp',
    #                             keep_cols=[],
    #                             is_restricted_activity=True,
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Grazing Lease',
    #                             location='Texas_All/PUF-GrazingLease.shp',
    #                             keep_cols=[],
    #                             is_restricted_activity=True,
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Water for Grazing',
    #                             location='Texas_All/PUF-GrazingWaterSources.shp',
    #                             keep_cols=[],
    #                             is_restricted_activity=True,
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Highways',
    #                             location='Texas_All/PUF-Highways.shp',
    #                             keep_cols=[],
    #                             is_restricted_activity=True,
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Minerals',
    #                             location='Texas_All/PUF-Minerals.shp',
    #                             keep_cols=['unittypede'],
    #                             is_restricted_subsurface_activity=True,
    #                             activity_name_appendage_col='unittypede',
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Oil and gas lease',
    #                             location='Texas_All/PUF-OilGasLease.shp',
    #                             keep_cols=['leasestatu'],
    #                             is_restricted_subsurface_activity=True,
    #                             activity_name_appendage_col='leasestatu',
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Oil and gas Wellbores',
    #                             location='Texas_All/PUF-OilGasWellbores.shp',
    #                             keep_cols=['cycle'],
    #                             is_restricted_subsurface_activity=True,
    #                             activity_name_appendage_col='cycle',
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Oil and gas Well Bottom Hole',
    #                             location='Texas_All/PUF-WellBottomHole.shp',
    #                             keep_cols=['cycle'],
    #                             is_restricted_subsurface_activity=True,
    #                             activity_name_appendage_col='cycle',
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='Renewables',
    #                             location='Texas_All/PUF-Renewables.shp',
    #                             keep_cols=['sitedescri'],
    #                             is_restricted_activity=True,
    #                             use_name_as_activity=False),
    #     # StateActivityDataSource(name='Renewable Tracts',
    #     #                         location='Texas_All/PUF-Renewables.shp',
    #     #                         keep_cols=['FIRST_sitedescription'],
    #     #                         is_restricted_activity=True,
    #     #                         use_name_as_activity=False),
    #     StateActivityDataSource(name='Well Bottom Hole',
    #                             location='Texas_All/PUF-WellBottomHole.shp',
    #                             keep_cols=['cycle'],
    #                             is_restricted_subsurface_activity=True,
    #                             activity_name_appendage_col='cycle',
    #                             use_name_as_activity=True),
    #
    # ]),
    'UT': StateForActivity(name='utah', activities=[
        # StateActivityDataSource(name='Water',
        #                         location='Utah_All/Utah_Water_Related_Land_Use',
        #                         keep_cols=['Descriptio',
        #                                    'LU_Group'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=True),
        StateActivityDataSource(name='Coal contract',
                                location='Utah_All/Contracts_Coal/Contracts_Coal.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Development lease',
                                location='Utah_All/Contracts_Dev_Lease/Contracts_Dev_Lease.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Grazing contract - ',
                                location='Utah_All/Contracts_Grazing/Contracts_Grazing.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True,
                                activity_name_appendage_col='app_descr'),
        StateActivityDataSource(name='Oil shale contract',
                                location='Utah_All/Contracts_Oil_Shale/Contracts_Oil_Shale.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Other minerals contract - ',
                                location='Utah_All/Contracts_Other_Mineral/Contracts_Other_Mineral.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='app_descr',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Renewables',
                                location='Utah_All/Contracts_Renewable/Contracts_Renewable.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SURFACE,
                                activity_name_appendage_col='app_descr',
                                use_name_as_activity=False),
        StateActivityDataSource(name='Range improvement project contract - ',
                                location='Utah_All/Contracts_Rip/Contracts_Rip.shp',
                                keep_cols=['descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SURFACE,
                                activity_name_appendage_col='descr',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Sand gravel contract',
                                location='Utah_All/Contracts_Sand_Gravel/Contracts_Sand_Gravel.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Tar sand contract',
                                location='Utah_All/Contracts_Tar_Sand/Contracts_Tar_Sand.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Special use contract - ',
                                location='Utah_All/Contracts_Sula/Contracts_Sula.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SURFACE,
                                activity_name_appendage_col='app_descr',
                                use_name_as_activity=False),
        StateActivityDataSource(name='Easements',
                                location='Utah_All/Contracts_Esmt/Contracts_Esmt.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas contract - ',
                                location='Utah_All/Contracts_Oil_Gas/Contracts_Oil_Gas.shp',
                                keep_cols=['app_descr', 'customer_n', 'record_sta'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='app_descr',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Wind zone',
                                location='Utah_All/UREZPhase1_WindZones/UREZPhase1_WindZones.shp',
                                keep_cols=[],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Solar zone',
                                location='Utah_All/UREZPhase1_SolarZones/UREZPhase1_SolarZones.shp',
                                keep_cols=[],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic/Past Uranium Production',
                                location='Utah_All/UraniumPastProducers/UraniumPastProducers.shp',
                                keep_cols=['OWNER'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas wells',
                                location='Utah_All/WellData/viewAGRC_WellData_Surf.shp',
                                keep_cols=['Operator', 'WellStatus'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas well bottom hole',
                                location='Utah_All/WellBottomHole/viewAGRC_WellData_DownHole.shp',
                                keep_cols=['ConstructS'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),

    ]),
    'WA': StateForActivity(name='washington', activities=[
        # StateActivityDataSource(name='Agriculture',
        #                         location='Washington_All/Agriculture.shp',
        #                         keep_cols=['CropType', 'CropGroup'],
        #                         is_restricted_activity=True,
        #                         use_name_as_activity=False),
        StateActivityDataSource(name='Current Leases',
                                location='Washington_All/current_leases_spatial_nature_20240515/current_leases_spatial_nature_20240515.shp',
                                keep_cols=['AGREEMENT1'],
                                # Use WA key
                                use_name_as_activity=False,
                                rights_type=RightsType.NEEDS_LOOKUP),
        StateActivityDataSource(name='Non-metallic minerals',
                                location='Washington_All/NonMetallicMinerals.shp',
                                keep_cols=['MINERAL', 'CATEGORY'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='CATEGORY',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Metallic minerals',
                                location='Washington_All/MetallicMinerals.shp',
                                keep_cols=['COMMODITIE', 'PRODUCTION', 'ORE_MINERA'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='COMMODITIE',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Active Surface Mine Permit Site',
                                location='Washington_All/ActiveSurfaceMinePermitSites.shp',
                                keep_cols=['APPLICANT_', 'MINE_NAME', 'COMMODITY_'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='COMMODITY_',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Oil and gas well',
                                location='Washington_All/OilGasWells.shp',
                                keep_cols=['COMPANY_NA', 'WELL_STATU'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        # StateActivityDataSource(name='Coal',
        #                         location='Washington_All/Coal.shp',
        #                         keep_cols=[],
        #                         rights_type=RightsType.SUBSURFACE,
        #                         use_name_as_activity=True),
        #Took this layer out because it was clear on QGIS there was no overlap

    ]),
    # 'WI': StateForActivity(name='wisconsin', activities=[
    #     StateActivityDataSource(name='misc',
    #                             location='Wisconsin_All/Miscellaneous.shp',
    #                             keep_cols=['PROP_NAME'],
    #                             is_restricted_activity=True,
    #                             use_name_as_activity=False,
    #                             is_misc = True),
    #     StateActivityDataSource(name='Conservation Easement',
    #                             location='Wisconsin_All/Conservation_Easement.shp',
    #                             keep_cols=['PROGRAM_NA'],
    #                             activity_name_appendage_col='PROGRAM_NA',
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='DNR Easement',
    #                             location='Wisconsin_All/DNR_Easement.shp',
    #                             keep_cols=['EASE_USE_C'],
    #                             activity_name_appendage_col='EASE_USE_C',
    #                             use_name_as_activity=True),
    #     StateActivityDataSource(name='DNR Owned',
    #                             location='Wisconsin_All/DNR_Owned.shp',
    #                             keep_cols=['EASE_USE_C'],
    #                             activity_name_appendage_col='EASE_USE_C',
    #                             use_name_as_activity=True)
    # ]),
    'WY': StateForActivity(name='wyoming', activities=[
        StateActivityDataSource(name='Metallic and nonmetallic mineral active lease - ',
                                location='Wyoming_All/ActiveMetallicNonMetallic.shp',
                                keep_cols=['oslisde._8', 'oslisde.64', 'oslisde.75'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='oslisde._8',
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas active lease',
                                location='Wyoming_All/OilGasLease.shp',
                                keep_cols=['oslisde.62', 'oslisde.73'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Easements',
                                location='Wyoming_All/Easements.shp',
                                keep_cols=['oslisde.20', 'oslisde.41', 'oslisde.13'],
                                activity_name_appendage_col='oslisde.20',
                                rights_type=RightsType.UNIVERSAL,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Grazing lease',
                                location='Wyoming_All/GrazingLease.shp',
                                keep_cols=['oslisde.12', 'oslisde.31'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Special use lease',
                                location='Wyoming_All/SpecialUseLeases.shp',
                                keep_cols=['oslisde.13','oslisde.19', 'oslisde.34'],
                                activity_name_appendage_col='oslisde.19',
                                rights_type=RightsType.UNIVERSAL,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Wind lease',
                                location='Wyoming_All/WindLeases.shp',
                                keep_cols=['oslisde.38', 'oslisde.13'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='WSGS Oil and gas well',
                                location='Wyoming_All/WSGS_OilGasWells.shp',
                                keep_cols=['COMPANY', 'STATUS'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Historic mine - ',
                                location='Wyoming_All/HistoricMinerals.shp',
                                keep_cols=['FTR_TYPE'],
                                activity_name_appendage_col='FTR_TYPE',
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True)
    ]),
    'MT': StateForActivity(name='Montana', activities=[
        StateActivityDataSource(name='Oil and gas well',
                                location='Montana_All/wells/wells_P.shp',
                                keep_cols=['CoName', 'Status', 'Type', 'Completed'],
                                rights_type=RightsType.SUBSURFACE,
                                activity_name_appendage_col='Type',
                                use_name_as_activity=True),
        StateActivityDataSource(name='Misc',
                                location='Montana_All/ManagedAreas.shp',
                                keep_cols=['MANAME', 'INST', 'UNITTYPE'],
                                rights_type=RightsType.UNIVERSAL),
        StateActivityDataSource(name='Timber Harvest Sale',
                                location='Montana_All/Timber.shp',
                                keep_cols=['HarvestPrescription', 'DateSold', 'DateClosed', 'LandOffice'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Lumber Mill',
                                location='Montana_All/Mills.shp',
                                keep_cols=['facilname', 'milltypeDe'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Coal active lease',
                                location='Montana_All/MMB_CoalActiveLease.shp',
                                keep_cols=['Prim_Cust', 'Producing', 'DateEffect', 'DateExpire'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True),
        StateActivityDataSource(name='Agriculture and grazing',
                                location='Montana_All/AGMB_AgreementTracts.shp',
                                keep_cols=['TractType', 'Status'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Commercial lease',
                                location='Montana_All/REMB_LeaseLots.shp',
                                keep_cols=['LeaseCateg', 'LeaseStatu'],
                                rights_type=RightsType.SURFACE,
                                use_name_as_activity=False),
        StateActivityDataSource(name='Oil and gas active lease',
                                location='Montana_All/MMB_OilandGasActiveLease.shp',
                                keep_cols=['Prim_Cust', 'Producing', 'DateEffect', 'DateExpire'],
                                rights_type=RightsType.SUBSURFACE,
                                use_name_as_activity=True)])
}
