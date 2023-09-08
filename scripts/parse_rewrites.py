import itertools
import json
from collections import defaultdict

REWRITES = """

Rights-Type= [ID-water:'TypeGroup', ID-roads: 'Easement Right']


Transaction Type = [CO-Misc: 'Transaction Type', ID-Misc:'TypeGroup', ID-Roads: 'TypeGroup']


Lease Status = [CO-Misc: 'Lease Status', ID-Misc:'Status', ID-Roads: 'Status', ID-Water:'Status', MN-AggMin: 'Status_1', 
ND-Min: 'LEASE_STATUS', NE-Water: 'RightStatu', NE-Rec: 'Status', OK-Misc:'EasementType', TX-Misc:'LEASE_STAT', TX-HardMin:'LEASE_STAT',
TX-OilGas:'LEASE_STAT', AZ-Misc:'leased', AZ-Min:'leased', AZ-OilGas:'leased', AZ-Solar:'status', WY-MetallicNonMet:'LeaseStatusLabel',
WY-OilGas:'LeaseStatusLabel', WY-Easement:'Status_LU', WY-Grazing:'Status_LU', WY-Special:'Status_LU', WY-Wind:'Status_LU', WA-Metal:'PRODUCTION',
WA-OilGas: 'WELL_STATU', UT-OilGasFields:'STATUS',UT-Rec:'STATUS',UT-Water:'LU_Group', NM-Ag:'STATUS', NM-Com:'STATUS',NM-Energy:'STATUS',
NM-Mineral:'STATUS',NM-OilGas:'STATUS', NM-RoW:'STATUS']


Activity = [CO-Misc: 'Lease Type', ID-Misc:'Type', ID-Roads: 'Easement Purpose', MN-Peat: 'T_LEASETYP', MT-Misc: 'UNITTYPE', 
OK-Misc:'Purpose', OK-Ag: 'Lease Type', TX-Coastal:'ACTIVITY_T', TX-Misc:'ACTIVITY', WI-Misc:'PROP_NAME', AZ-Misc:'ke', AZ-Min:'ke', 
AZ-OilGas:'type', WY-MetallicNonMet:'MineralTypeLabel', WY-OilGas:'MineralTypeLabel', WY-Easement:'Sub_Group_LU', WY-Special:'Type_LU',
WA-AG:'CropType', UT-Rec:'TYPE', NM-Energy:'LEASE_TYPE',NM-Mineral:'LEASE_TYPE']


Sub-activity = [CO-Misc: 'Lease Subtype', ID-Water:'WaterUse', MN-Rec:'AREA_NAME', MN-DNRRec:'UNIT_NAME', MN-AggMin: 'Type', 
MT-Misc: 'MANAME', ND-Rec: 'UNIT_NAME', NE-Water: 'RightUse', NE-Rec: 'AreaName', SD-Rec:'ParkName', TX-Coastal:'PROJECT_NA', 
TX-Misc:'PURPOSE', AZ-Ag:'name', AZ-Solar:'technology', WY-MetallicNonMet:'MetallicNonMetallicLeaseSubType', WY-Easement:'Use_Type_LU',
WY-Special:'Purpose_LU', WA-Mining:'MINE_NAME', WA-Metal:'ORE_MINERA', WA-NonMetal:'MINERAL', WA-AG:'CropGroup', UT-Grazing:'AllotName',
UT-Rec:'NAME',UT-Water:'Descriptio',NM-Mineral:'SUB_TYPE']


Use Purpose = [MN-Rec:'AREA_TYPE', MN-DNRRec:'UNIT_TYPE', MN-AggMin: 'Status_2']


Commodity = [ID-Misc:'Commodities', MN-ActMin:'T_LEASETYP', MN-HisMin:'T_LEASETYP', WA-Mining:'COMMODITY_', WA-Metal:'COMMODITIE']


Lessee or Owner or Manager = [CO-Misc: 'Lessee Name',ID-Misc:'Name'*, ID-Roads: 'Parties', MN-Peat: 'T_PNAMES', MN-DNRRec:'ADMINISTRA', 
MN-ActMin:'T_PNAMES', MN-HisMin:'T_PNAMES', MT-Misc: 'INST', ND-Min: 'LESSEE', NE-Water: 'FirstName', OK-Misc:'Grantee', 
OK-Min:'OwnerName', OK-Ag: 'OwnerName', TX-Coastal:'GRANTEE', TX-Misc:'PRIMARY_LE', TX-HardMin:'ORIGINAL_L', TX-OilGas:'ORIGINAL_L', AZ-Misc:'full_name', 
AZ-Min:'full_name', AZ-OilGas:'full_name', AZ-Solar:'projectnam', WY-MetallicNonMet:'CompanyName', WY-OilGas:'CompanyName', WY-Easement:'Leaseholder_LU',
WY-Grazing:'Leaseholder_LU', WY-Special:'Leaseholder_LU', WY-Wind:'Leaseholder_LU', WA-Mining:'APPLICANT_', WA-OilGas: 'COMPANY_NA', UT-Grazing:'Manager',
UT-OilGasWell:'Operator', NM-Ag:'OGRID_NAM',NM-Com:'OGRID_NAM', NM-Energy:'OGRID_NAM',NM-Mineral:'OGRID_NAM', NM-OilGas:'OGRID_NAM',
NM-RoW:'OGRID_NAM']


Lessee Name 2 = [NE-Water: 'LastName']

Owner Address or Location = [OK-Min:'Address2', OK-Ag: 'Address2', WY-MetallicNonMet:'CompanyZipCode', WY-OilGas:'CompanyZipCode']

Lessor = [TX-OilGas:'LESSOR']

Lease Start Date = [CO-Misc: 'Lease State Date', ID-Misc:'DteGranted', ID-Roads: 'DteGranted', MN-Peat: 'T_STARTDAT', 
MN-ActMin:'T_STARTDAT', MN-HisMin:'T_STARTDAT', ND-Min: 'LEASE_EFFECTIVE', NE-Rec: 'StartDate', OK-Min:'Begin Date', OK-Ag: 'Begin Date', TX-HardMin:'EFFECTIVE_',
TX-OilGas:'EFFECTIVE_', AZ-Misc:'effdate', AZ-Min:'effdate', AZ-OilGas:'effdate', WY-MetallicNonMet:'LeaseIssueDate', WY-OilGas:'LeaseIssueDate',
WY-Easement:'Issue_Date_LU', WY-Grazing:'Start_Date_LU', WY-Special:'Start_Date_LU', WY-Wind:'Start_Date_LU', NM-Com:'VEREFF_DTE',
NM-Mineral:'VEREFF_DTE', NM-OilGas:'VEREFF_DTE']


Lease End Date = [CO-Misc: 'Lease End Date', ID-Misc:'DteExpires', ID-Roads: 'DteExpires', MN-Peat: 'T_EXPDAT', MN-ActMin:'T_EXPDAT', 
MN-HisMin:'T_EXPDAT', ND-Min: 'LEASE_EXPIRATION', OK-Min:'End Date', OK-Ag: 'End Date', AZ-Misc:'expdate', AZ-Min:'expdate', AZ-OilGas:'expdate', WY-MetallicNonMet:'LeaseExpirationDate',
WY-OilGas:'LeaseExpirationDate', WY-Easement:'Expiration_Date_LU', WY-Grazing:'Expiration_Date_LU', WY-Special:'Expiration_Date_LU',
WY-Wind:'Expiration_Date_LU',NM-Com:'VERTRM_DTE',NM-Mineral:'VERTRM_DTE', NM-OilGas:'VERTRM_DTE']


Lease Extension Date = [ND-Min: 'LEASE_EXTENDED']


Source = [ID-Water:'Source']


LandClass = [MN-ActMin:'ML_SU_LAND', MN-HisMin:'ML_SU_LAND']



"""


def clean_text(t):
    t = t.strip(' ')
    t = t.strip('\n')
    t = t.strip('[')
    t = t.strip(']')
    t = t.strip('*')
    t = t.strip("'")
    t = t.strip('"')
    return t


def main():
    clean_output = defaultdict(lambda: defaultdict(dict))
    units = [u.split('=') for u in REWRITES.split('\n\n') if u]
    unit_parts = [(l, r.split(',')) for l, r in units]
    for out_var, in_vars in unit_parts:
        for in_var in in_vars:
            in_var = clean_text(clean_text(in_var))
            out_var = clean_text(clean_text(out_var))

            address, true_in_var = in_var.split(':')
            true_in_var = clean_text(clean_text(true_in_var))
            state, activity = address.split('-')

            clean_output[state.lower()][activity.lower()][true_in_var] = out_var

    uniq_activities = set(
        itertools.chain.from_iterable([list(activities.keys()) for activities in clean_output.values()])
    )
    print(uniq_activities)

    with open('/scripts/activity_match_extras/rewrite_rules.json', 'w') as fh:
        json.dump(clean_output, fh, indent=4)


if __name__ == '__main__':
    main()
