# truncate_tables.py

from sqlserver_connector import get_connection_OLAP

FACT_TABLES = [
    "FactScope1Emissions"
]

DIM_TABLES = [
    "DimFacility",
    "DimEmissionType",
    "DimFuelType",
    "DimTimeperiod"
]


def delete_table(cursor, table_name):
    print(f"🧹 Clearing {table_name}...")
    cursor.execute(f"DELETE FROM {table_name}")


def reset_identity_if_exists(cursor, table_name):
    check_identity_sql = f"""
        SELECT COUNT(*)
        FROM sys.identity_columns
        WHERE object_id = OBJECT_ID('{table_name}')
    """

    cursor.execute(check_identity_sql)
    has_identity = cursor.fetchone()[0]

    if has_identity > 0:
        print(f"🔁 Resetting identity for {table_name}...")
        cursor.execute(f"DBCC CHECKIDENT ('{table_name}', RESEED, 0)")
    else:
        print(f"ℹ {table_name} has no identity column. Skipping reseed.")


def clear_all_tables():
    print("🔄 Starting table clearing process...")

    conn = get_connection_OLAP()
    cursor = conn.cursor()

    try:
        for table in FACT_TABLES:
            delete_table(cursor, table)
            reset_identity_if_exists(cursor, table)

        for table in DIM_TABLES:
            delete_table(cursor, table)
            reset_identity_if_exists(cursor, table)

        conn.commit()
        print("✅ All tables cleared successfully!")

    except Exception as e:
        conn.rollback()
        print("❌ Error during clearing:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    clear_all_tables()