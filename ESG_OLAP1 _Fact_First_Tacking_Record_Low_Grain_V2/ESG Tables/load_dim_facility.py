# Import pandas library for data manipulation and working with DataFrames
import pandas as pd

# Import numpy library for handling numerical operations (like NaN values)
import numpy as np

# Import database connection functions and predefined OLAP queries
from sqlserver_connector import get_OLTP_connection, get_connection_OLAP

# Import transformation function that converts source row to DimFacility format
from generators import gen_dimFacility

# Import audit logging functions (main audit + row-level error logging)
from audit_log import log_audit, log_row_error  # Import the new error logger
from config import CONFIG


# Define the SQL query to extract facility-related data from OLTP system
DimFacility = """
        -- Select facility and related information
        SELECT 
            -- Get Facility primary key
            f.id AS FacilityId,

            -- Get Facility name
            f.name AS FacilityName,

            -- Get Facility location
            f.location AS Location,

            -- Get Facility Type Id
            ft.id AS FacilityTypeId,

            -- Get Facility Type Name
            ft.name AS FacilityTypeName,

            -- Get Organization Id
            o.id AS OrganizationId,

            -- Get Organization Name
            o.name AS OrganizationName

        -- Main table: facility
        FROM facility f

        -- Join facility_type table
        LEFT JOIN facility_type ft 
            ON ft.id = f.facility_type_id

        -- Join organization table
        LEFT JOIN organization o 
            ON o.id = f.organization_id

        -- Filter only active facilities
        WHERE f.is_active = 'True'
    """


# Define main ETL function to load data into DimFacility table
# run_id is used for tracking the ETL execution
def load_dim_facility(run_id):

    # Define process name for auditing
    process_name = "load_dim_facility_stage.py"
    process_type = CONFIG["dim_process"]

    # Define target table name
    table_name = "DimFacility"
    
    # Initialize target connection variable (used in finally block)
    conn_tgt = None

    # Initialize cursor variable (used in finally block)
    cursor = None

    # Start main try block for ETL process
    try:

        # -----------------------------
        # 1. EXTRACT PHASE
        # -----------------------------

        # Get source (OLTP) database connection
        conn_src = get_OLTP_connection()

        # Execute SQL query and load result into pandas DataFrame
        df = pd.read_sql(DimFacility, conn_src)

        # Close source connection after extraction
        conn_src.close()


        # -----------------------------
        # 2. TRANSFORM PHASE
        # -----------------------------

        # Apply transformation function row by row
        # axis=1 means apply function to each row
        # result_type="expand" expands dictionary output into columns
        df = df.apply(gen_dimFacility, axis=1, result_type="expand")

<<<<<<< HEAD
        

=======
>>>>>>> 430e410 (Initial commit)
        # Insert a surrogate key column named "Id" at position 0
        # Generates sequential values starting from 1
        df.insert(0, "Id", range(1, len(df) + 1)) 


        # -----------------------------
        # 3. LOAD SETUP PHASE
        # -----------------------------

        # Get target (OLAP) database connection
        conn_tgt = get_connection_OLAP()

        # Create cursor to execute SQL statements
        cursor = conn_tgt.cursor()

        # Replace NaN values with None (so SQL Server accepts NULL values)
<<<<<<< HEAD
        
=======
        df = df.replace({np.nan: None})
>>>>>>> 430e410 (Initial commit)

        # Create comma-separated column names for INSERT statement
        columns = ",".join(df.columns)

        # Create placeholders (?) dynamically based on column count
        placeholders = ",".join(["?"] * len(df.columns))

        # Build dynamic INSERT SQL statement
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Initialize counters for tracking ETL results
        rows_inserted = 0
        rows_skipped = 0
        rows_failed = 0


        # -----------------------------
        # 4. RESILIENT ROW-LEVEL LOADING
        # -----------------------------

        # Loop through each row in DataFrame
        for index, row in df.iterrows():

            # Start try block for each row (so one row failure doesn't stop whole ETL)
            try:

                # Check if record already exists in target table using Id
<<<<<<< HEAD
                cursor.execute(f"SELECT COUNT(1) FROM DimFacility WHERE FacilityId = ?", (row['Id'],))
=======
                cursor.execute(f"SELECT COUNT(1) FROM {table_name} WHERE Id = ?", (row['Id'],))
>>>>>>> 430e410 (Initial commit)

                # If record does NOT exist
                if cursor.fetchone()[0] == 0:

                    # Insert the row into target table
<<<<<<< HEAD
                    cursor.execute(insert_sql, (
                        row['Id'],
                        row['FacilityId'],
                        row['FacilityName'],
                        row['FacilityTypeId'],
                        row['FacilityTypeName'],
                        row['OrganizationId'],
                        row['OrganizationName'],
                        row['Location'],
                        row['CreatedDate'],
                        row['CreatedBy'],
                        row['UpdatedBy'],
                        row['UpdatedDate']
                        ))
=======
                    cursor.execute(insert_sql, tuple(row))
>>>>>>> 430e410 (Initial commit)

                    # Increment inserted counter
                    rows_inserted += 1

                else:
                    # If record already exists, increment skipped counter
                    rows_skipped += 1
                
                # Commit every 50 inserted rows (batch commit for performance)
                if rows_inserted % 50 == 0:
                    conn_tgt.commit()

            # If any error occurs for that particular row
            except Exception as row_err:

                # Increment failed counter
                rows_failed += 1

                # Log row-level error into database
                log_row_error(run_id, process_name, table_name, row.to_dict(), str(row_err))

                # Print warning message for debugging
                print(f"⚠️ Row {index+1} failed in {table_name}: {row_err}")

                # Continue with next row without stopping entire ETL
                continue 


        # -----------------------------
        # 5. FINALIZATION PHASE
        # -----------------------------

        # Final commit to ensure all records are saved
        conn_tgt.commit()

        # Determine overall status based on failed rows
        status = "SUCCESS" if rows_failed == 0 else "PARTIAL SUCCESS"

        # Log overall ETL audit information
        log_audit(run_id, process_name,process_type, table_name, status, f"Failed: {rows_failed}", rows_inserted)

<<<<<<< HEAD
        print(f"✅ {table_name} load finished. Success: {rows_inserted}, Failed: {rows_failed}")
=======
>>>>>>> 430e410 (Initial commit)

    # If any major error occurs in entire ETL process
    except Exception as e:

        # Print critical error message
        print(f"❌ Critical Error: {e}")

        # Log failure in audit table
        log_audit(run_id, process_name,process_type, table_name, "FAILED", str(e), 0)
    

    # Finally block always executes (even if error occurs)
    finally:

        # Close cursor if it was created
        if cursor:
            cursor.close()

        # Close target connection if it was created
        if conn_tgt:
            conn_tgt.close()