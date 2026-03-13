from datetime import date



CONFIG = {


    # =======================
    # Data Base Cofigurations
    # =======================
    "server": r"ANIS-PG02X1LW-P\SQLEXPRESS",
    "OLTP_database": "ESG_SCOPE3",
    "OLAP_database": "ESG_SCOPL1_OLAP_Grain",
    "driver": "{ODBC Driver 17 for SQL Server}",


    "dim_process" : "Dim_Load",
    "Fact_process" : "Fact_Load",







    # ======================
    # SYSTEM
    # ======================
    "system_user": "system"
}
