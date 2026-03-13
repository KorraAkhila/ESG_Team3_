# ==========================================================
# Import Required Libraries
# ==========================================================

# Pandas for data extraction and transformation
import pandas as pd  

# Numpy for handling NaN values
import numpy as np  

# Import database connection helpers and predefined queries
from sqlserver_connector import get_OLTP_connection, get_connection_OLAP

# Import transformation logic for DimEmissionType
from generators import gen_DimEmissionType  

# Import audit logging functions (process-level and row-level)
from audit_log import log_audit, log_row_error   # Added log_row_error for row-level tracking
from config import CONFIG


# ==========================================================
# SQL Query to Extract Emission Type Data from OLTP
# ==========================================================

DimEmissionSource = """
<<<<<<< HEAD
    

SELECT DISTINCT
        et.id   AS EmissionTypeId,
        et.name AS EmissionTypeName
    FROM emission_equipment_type  et
   where et.is_active=1
=======
    SELECT DISTINCT
        et.id   AS EmissionTypeId,
        et.name AS EmissionTypeName
    FROM emission_source es
    JOIN emission_equipment_type et
        ON et.id = es.equipment_type_id
    WHERE es.is_active = 'True'
>>>>>>> 430e410 (Initial commit)
"""


# ==========================================================
# Function to Load DimEmissionType Table into OLAP
# ==========================================================

def load_dim_emission_type(run_id):

    # Process name used in audit logging
    process_name = "load_dim_emission_source.py"
    process_type = CONFIG["dim_process"]

    # Target dimension table name
    table_name = "DimEmissionType"

    # Initialize target connection variables
    # (Prevents UnboundLocalError in finally block)
    conn_tgt = None
    cursor = None

    try:

        # ==================================================
        # 1️⃣ EXTRACT Phase
        # ==================================================
        
        # Establish connection to OLTP (source system)
        conn_src = get_OLTP_connection()

        # Execute SQL query and load result into DataFrame
        df = pd.read_sql(DimEmissionSource, conn_src)

        # Close source connection
        conn_src.close()


        # ==================================================
        # 2️⃣ TRANSFORM Phase
        # ==================================================
        
        # Apply transformation function row-wise
        df = df.apply(gen_DimEmissionType, axis=1, result_type="expand")
<<<<<<< HEAD
        

        # Add surrogate key column (Id)
        # df.insert(0, "Id", range(1, len(df) + 1))
=======

        # Add surrogate key column (Id)
        df.insert(0, "Id", range(1, len(df) + 1))
>>>>>>> 430e410 (Initial commit)


        # ==================================================
        # 3️⃣ LOAD Setup Phase
        # ==================================================
        
        # Connect to OLAP (target system)
        conn_tgt = get_connection_OLAP()
        cursor = conn_tgt.cursor()

        # Replace NaN values with None (SQL compatible NULL)
<<<<<<< HEAD
        
=======
        df = df.replace({np.nan: None})
>>>>>>> 430e410 (Initial commit)

        # Dynamically prepare INSERT statement
        columns = ",".join(df.columns)
        placeholders = ",".join(["?"] * len(df.columns))
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Initialize counters for monitoring
        rows_inserted = 0
        rows_skipped = 0
        rows_failed = 0


        # ==================================================
        # 4️⃣ LOAD Phase (Row-Level Error Handling)
        # ==================================================
        
        # Loop through each row in DataFrame
        for index, row in df.iterrows():
            try:

                # Duplicate check based on surrogate key (Id)
                cursor.execute(
<<<<<<< HEAD
                    f"SELECT COUNT(1) FROM {table_name} WHERE EmissionTypeId = ?",
                    (row['EmissionTypeId'],)
=======
                    f"SELECT COUNT(1) FROM {table_name} WHERE Id = ?",
                    (row['Id'],)
>>>>>>> 430e410 (Initial commit)
                )

                # If record does not exist → Insert
                if cursor.fetchone()[0] == 0:
<<<<<<< HEAD
                    cursor.execute(insert_sql, (
                        row['EmissionTypeId'],
                        row['EmissionTypeName'],
                        row['CreatedDate'],
                        row['CreatedBy'],
                        row['UpdatedBy'],
                        row['UpdatedDate']
                    ))
=======
                    cursor.execute(insert_sql, tuple(row))
>>>>>>> 430e410 (Initial commit)
                    rows_inserted += 1
                else:
                    # If record exists → Skip
                    rows_skipped += 1

                # Batch commit every 50 successful inserts
                if rows_inserted % 50 == 0:
                    conn_tgt.commit()

            except Exception as row_err:
                
                # If error occurs for a row:
                rows_failed += 1

                # Log row-level error with data snapshot
                log_row_error(
                    run_id,
                    process_name,
<<<<<<< HEAD
                    
=======
                    process_type,
>>>>>>> 430e410 (Initial commit)
                    table_name,
                    row.to_dict(),
                    str(row_err)
                )

                # Print error message
                print(f"⚠️ Row {index+1} failed in {table_name}: {row_err}")

                # Continue with next record
                continue


        # ==================================================
        # 5️⃣ FINALIZATION Phase
        # ==================================================
        
        # Commit remaining uncommitted records
        conn_tgt.commit()

        # Determine final process status
        status = "SUCCESS" if rows_failed == 0 else "PARTIAL SUCCESS"

        # Log audit summary
        log_audit(
            run_id,
            process_name,
            process_type,
            table_name,
            status,
            f"Failed: {rows_failed}",
            rows_inserted
        )

        # Print final load summary
        print(f"✅ {table_name} load finished. Success: {rows_inserted}, Failed: {rows_failed}")


    except Exception as e:
        
        # ==================================================
        # Critical Error Handling (System-Level Failure)
        # ==================================================
        
        print(f"❌ Critical error in {process_name}: {e}")

        # Log failure in audit table
        log_audit(
            run_id,
            process_name,
            table_name,
            "FAILED",
            str(e),
            0
        )


    finally:
        
        # ==================================================
        # Resource Cleanup
        # ==================================================
        
        # Close cursor if opened
        if cursor:
            cursor.close()

        # Close target connection if opened
        if conn_tgt:
            conn_tgt.close()