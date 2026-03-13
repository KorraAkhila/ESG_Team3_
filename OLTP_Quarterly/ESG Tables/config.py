from datetime import date

CONFIG = {
    # ======================
    # OUTPUT
    # ======================
    "output_folder": "data",
    "excel_file": "ESG_Scope1_NewData.xlsx",


    #=======================
    # ORGANIZATION
    #=======================
    "resource_folder": "Resource",
    "organization_excel_file": "organizations.xlsx",

    # ======================
    # DATA VOLUME
    # ======================
    "min_rows": 10000,

    # ======================
    # TIME CONTROL
    # ======================
    # Generate data from 4 years ago until today
    "start_year_offset": 4,   # 4 years back from now

    # ======================
    # SYSTEM
    # ======================
    "system_user": "system",

    # ======================
    # ACTIVE GAS CONFIG
    # ======================
    "active_gas_id": 1,              # 1 = CO2
    "active_standard_id": 1             # GHG Protocol

}
