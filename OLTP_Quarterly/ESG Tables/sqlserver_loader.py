import pandas as pd
import pyodbc
from pathlib import Path
from config import CONFIG
# ===============================
# SQL SERVER CONFIG
# ===============================
SQL_CONFIG = {
    "server": r"PRAVEENS-PC\SQLEXPRESS01",
    "database": "esg_sample",
    "driver": "{ODBC Driver 17 for SQL Server}"
}

EXCEL_FILE = Path(CONFIG["output_folder"]) / CONFIG["excel_file"]

print(f"📂 Reading Excel file from: {EXCEL_FILE}")


# Tables that CANNOT be truncated due to FK references
FK_PROTECTED_TABLES = {
    "esg_evidance",
    "scope1_emission",
    "fuel_consumption",
    "emission_factor",
    "reporting_period",
    "emission_source",
    "facility",
    "document_type"
}



# ===============================
# TABLE LOAD ORDER (FK SAFE)
# ===============================
TABLE_ORDER = [
    "organization",
    "facility_type",
    "emission_equipment_type",
    "fuel_type",
    "gas_type",
    "standard",
    "calculation_method",
    "document_type",
    "facility",
    "emission_source",
    "reporting_period",
    "emission_factor",
    "fuel_consumption",
    "scope1_emission",
    "esg_evidance"
]

# ===============================
# CONNECT TO SQL SERVER
# ===============================
def get_connection():
    conn_str = (
        f"DRIVER={SQL_CONFIG['driver']};"
        f"SERVER={SQL_CONFIG['server']};"
        f"DATABASE={SQL_CONFIG['database']};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str, autocommit=False)

# ===============================
# TRUNCATE TABLE
# ===============================
def is_fk_referenced(cursor, table):
    cursor.execute("""
        SELECT 1
        FROM sys.foreign_keys fk
        JOIN sys.tables t
            ON fk.referenced_object_id = t.object_id
        WHERE t.name = ?
    """, table)

    return cursor.fetchone() is not None

def truncate_table(cursor, table):
    if is_fk_referenced(cursor, table):
        cursor.execute(f"DELETE FROM {table}")
        print(f"🧹 Deleted (FK-safe): {table}")
    else:
        cursor.execute(f"TRUNCATE TABLE {table}")
        print(f"🧹 Truncated: {table}")



# ===============================
# INSERT DATA
# ===============================
def clean_value(v):
    if pd.isna(v):
        return None
    if isinstance(v, str):
        v = v.strip()
        if v.lower() in ("", "na", "n/a", "null", "none"):
            return None
    return v


def insert_table(cursor, table, df):
    if df.empty:
        print(f"⚠️ Skipped empty table: {table}")
        return

    # ✅ Pandas 3.x compatible replacement for applymap
    df = df.apply(lambda col: col.map(clean_value))

    columns = ",".join(df.columns)
    placeholders = ",".join(["?"] * len(df.columns))
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    data = [tuple(row) for row in df.itertuples(index=False, name=None)]

    cursor.fast_executemany = True
    cursor.executemany(sql, data)

    print(f"✅ Inserted {len(data)} rows into {table}")

# ===============================
# MAIN LOAD FUNCTION
# ===============================
def load_data():

    if not EXCEL_FILE.exists():
        raise FileNotFoundError(f"Excel file not found: {EXCEL_FILE}")

    sheets = pd.read_excel(EXCEL_FILE, sheet_name=None)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("\n🔒 Disabling constraints...")
        cursor.execute("EXEC sp_msforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL'")

        # 🔥 TRUNCATE IN REVERSE ORDER
        for table in reversed(TABLE_ORDER):
            truncate_table(cursor, table)

        # 🔥 INSERT IN FK ORDER
        for table in TABLE_ORDER:
            df = sheets.get(table)
            if df is None:
                print(f"⚠️ Sheet not found in Excel: {table}")
                continue

            insert_table(cursor, table, df)

        print("\n🔓 Enabling constraints...")
        cursor.execute("EXEC sp_msforeachtable 'ALTER TABLE ? WITH CHECK CHECK CONSTRAINT ALL'")

        conn.commit()
        print("\n🎉 DATA LOAD COMPLETED SUCCESSFULLY")

    except Exception as e:
        conn.rollback()
        print("\n❌ ERROR OCCURRED — TRANSACTION ROLLED BACK")
        raise e

    finally:
        cursor.close()
        conn.close()

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    load_data()
