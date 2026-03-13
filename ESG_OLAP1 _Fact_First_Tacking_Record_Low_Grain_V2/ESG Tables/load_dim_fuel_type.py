# ==========================================================
# Import Required Libraries
# ==========================================================

# Pandas for data extraction and transformation
import pandas as pd

# Numpy for handling missing values (NaN → None)
import numpy as np

# Database connection helpers for OLTP (source) and OLAP (target)
from sqlserver_connector import get_OLTP_connection, get_connection_OLAP

# Transformation function for DimFuelType
from generators import gen_DimFuelType

# Audit logging functions (process-level + row-level error tracking)
from audit_log import log_audit, log_row_error   # log_row_error added for row-level tracking
from config import CONFIG


# ==========================================================
# SQL Query to Extract Fuel Type Data from OLTP
# ==========================================================

DimFuelType = """
    SELECT
        ROW_NUMBER() OVER (ORDER BY ft.id) AS Id,  -- Surrogate Key
        ft.id   AS FuelTypeId,
        ft.name AS FuelTypeName,
        ft.unit AS FuelUnit,
        gt.id   AS GasTypeId,
        gt.name AS GasName,
        gt.unit AS GasUnit
    FROM fuel_type ft
    JOIN emission_factor ef
        ON ft.id = ef.fuel_type_id
    JOIN gas_type gt
        ON gt.id = ef.gas_type_id
    WHERE gt.id = 1   -- Only CO2 records
    GROUP BY
        ft.id, ft.name, ft.unit,
        gt.id, gt.name, gt.unit
    ORDER BY ft.id
"""


# ==========================================================
# Function to Load DimFuelType into OLAP
# ==========================================================

def load_dim_fuel_type(run_id):

    # Process metadata for audit tracking
    process_name = "load_dim_fuel_type.py"
    process_type = CONFIG["dim_process"]
    table_name = "DimFuelType"

    # Initialize connection objects (avoids UnboundLocalError)
    conn_tgt = None
    cursor = None

    try:

        # ==================================================
        # 1️⃣ EXTRACT Phase
        # ==================================================
        
        # Connect to OLTP source database
        conn_src = get_OLTP_connection()

        # Execute SQL query and load data into Pandas DataFrame
        df = pd.read_sql(DimFuelType, conn_src)

        # Close source connection
        conn_src.close()


        # ==================================================
        # 2️⃣ TRANSFORM Phase
        # ==================================================
        
        # Apply transformation function row-wise
        df = df.apply(gen_DimFuelType, axis=1, result_type="expand")

        # Replace NaN values with None (SQL compatible)
        df = df.replace({np.nan: None})


        # ==================================================
        # 3️⃣ LOAD Setup Phase
        # ==================================================
        
        # Connect to OLAP target database
        conn_tgt = get_connection_OLAP()
        cursor = conn_tgt.cursor()

        # Dynamically build INSERT statement
        columns = ",".join(df.columns)
        placeholders = ",".join(["?"] * len(df.columns))
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Initialize counters for monitoring load results
        rows_inserted = 0
        rows_skipped = 0
        rows_failed = 0


        # ==================================================
        # 4️⃣ LOAD Phase (Row-by-Row Processing with Error Handling)
        # ==================================================
        
        # Loop through each row in the DataFrame
        for index, row in df.iterrows():

            # Nested try block for row-level error handling
            try:

                # Check if record already exists (Duplicate prevention)
                cursor.execute(
                    f"SELECT COUNT(1) FROM {table_name} WHERE FuelTypeId = ?",
                    (row['FuelTypeId'],)
                )

                # If record does not exist → Insert
                if cursor.fetchone()[0] == 0:
                    cursor.execute(insert_sql, tuple(row))
                    rows_inserted += 1
                else:
                    # If record exists → Skip
                    rows_skipped += 1

            except Exception as row_err:
                
                # If row-level error occurs
                rows_failed += 1

                # Log detailed row error into error log table
                log_row_error(
                    run_id,
                    process_name,
                    table_name,
                    row.to_dict(),
                    str(row_err)
                )

                # Print error message for debugging
                print(f"⚠️ Row {index+1} failed in {table_name}: {row_err}")

                # Skip bad record and continue with next row
                continue


        # ==================================================
        # 5️⃣ FINALIZATION Phase
        # ==================================================
        
        # Commit all successful inserts
        conn_tgt.commit()

        # Determine overall process status
        status = "SUCCESS" if rows_failed == 0 else "PARTIAL SUCCESS"

        # Log audit summary
        log_audit(
            run_id,
            process_name,
            process_type,
            table_name,
            status,
            f"Failed rows: {rows_failed}",
            rows_inserted
        )

        # Print final load summary
        print(f"✅ {table_name} load complete. Success: {rows_inserted}, Skipped: {rows_skipped}, Failed: {rows_failed}")


    except Exception as e:
        
        # ==================================================
        # Critical Error Handling (System-Level Failure)
        # ==================================================
        
        print(f"❌ Critical error in {process_name}: {e}")

        # Log failure in audit table
        log_audit(
            run_id,
            process_name,
            process_type,
            table_name,
            "FAILED",
            str(e),
            0
        )


    finally:
        
        # ==================================================
        # Resource Cleanup
        # ==================================================
        
        # Close cursor safely
        if cursor:
            cursor.close()

        # Close target connection safely
        if conn_tgt:
            conn_tgt.close()