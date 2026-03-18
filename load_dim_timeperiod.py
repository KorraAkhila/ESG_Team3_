# Import pandas library to work with structured data (DataFrames)
import pandas as pd

# Import numpy library to handle numerical operations and NaN values
import numpy as np

# Import database connection functions and OLAP queries from connector module
from sqlserver_connector import get_OLTP_connection, get_connection_OLAP

# Import transformation function that converts raw data into DimTimeperiod format
from generators import gen_DimTimeperiod

# Import audit logging functions (main audit log + row-level error log)
from audit_log import log_audit, log_row_error  # Import the row error logger


from config import CONFIG


# Define SQL query to extract reporting period data from source system
DimTimeperiod = """
        -- Select calculated TimeKey (YYYYMM format)
        SELECT 
            (YEAR(end_date) * 100 + MONTH(end_date)) AS TimeKey,

            -- Select period start date
            start_date AS PeriodStartDate,

            -- Select period end date
            end_date AS PeriodEndDate,

            -- Select reporting year
            year AS ReportingYear,

            -- Select reporting month number
            month AS ReportingMonth,

            -- Get month name from end_date (e.g., January, February)
            DATENAME(month, end_date) AS MonthName,

            -- Generate Quarter value (e.g., Q1, Q2, Q3, Q4)
            'Q' + CAST(DATEPART(quarter, end_date) AS VARCHAR) AS Quarter

        -- Source table name
        FROM reporting_period

        -- Filter only active reporting periods
        WHERE is_active = 'True'
    """


# Define ETL function to load DimTimeperiod dimension
# run_id is used to track this ETL execution
def load_dim_timeperiod(run_id):

    # Define process name for audit logging
    process_name = "load_dim_timeperiod_stage.py"
    process_type = CONFIG["dim_process"]

    # Define target table name
    table_name = "DimTimeperiod"
    
    # Initialize target connection variable (used in finally block)
    conn_tgt = None

    # Initialize cursor variable (used in finally block)
    cursor = None

    # Start main ETL try block
    try:

        # -----------------------------
        # 1. EXTRACT PHASE
        # -----------------------------

        # Establish connection to OLTP (source) database
        conn_src = get_OLTP_connection()

        # Execute SQL query and load result into pandas DataFrame
        df = pd.read_sql(DimTimeperiod, conn_src)

        # Close source connection after extraction
        conn_src.close()


        # -----------------------------
        # 2. TRANSFORM PHASE
        # -----------------------------

        # Apply transformation function row-by-row
        # axis=1 means apply to each row
        # result_type="expand" converts dictionary output into columns
        df = df.apply(gen_DimTimeperiod, axis=1, result_type="expand")

        # Replace NaN values with None so SQL Server accepts them as NULL
        df = df.replace({np.nan: None})


        # -----------------------------
        # 3. LOAD SETUP PHASE
        # -----------------------------

        # Establish connection to OLAP (target) database
        conn_tgt = get_connection_OLAP()

        # Create cursor object to execute SQL statements
        cursor = conn_tgt.cursor()

        # Create comma-separated column names for INSERT statement
        columns = ",".join(df.columns)

        # Create dynamic placeholders (?) based on number of columns
        placeholders = ",".join(["?"] * len(df.columns))

        # Build dynamic INSERT SQL query
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Initialize counters to track load statistics
        rows_inserted = 0
        rows_skipped = 0
        rows_failed = 0


        # -----------------------------
        # 4. ROW-BY-ROW PROCESSING
        # -----------------------------

        # Loop through each row in DataFrame
        for index, row in df.iterrows():

            # Try block for each individual row
            # Ensures one row failure doesn't stop entire process
            try:

                # Check whether record already exists using TimeKey
                # Prevents Primary Key violation
                cursor.execute(f"SELECT COUNT(1) FROM {table_name} WHERE TimeKey = ?", (row['TimeKey'],))
                
                # If record does NOT exist
                if cursor.fetchone()[0] == 0:

                    # Insert row into target table
                    cursor.execute(insert_sql, tuple(row))

                    # Increment inserted counter
                    rows_inserted += 1

                else:
                    # If record already exists, increment skipped counter
                    rows_skipped += 1
            
            # If an error occurs for this specific row
            except Exception as row_err:

                # Increment failed counter
                rows_failed += 1

                # Log row-level error into database table
                log_row_error(run_id, process_name,process_type, table_name, row.to_dict(), str(row_err))

                # Print warning message with row index and TimeKey
                print(f"⚠️ Row {index+1} (TimeKey: {row['TimeKey']}) failed: {row_err}")

                # Continue processing next row
                continue 


        # -----------------------------
        # 5. FINALIZATION PHASE
        # -----------------------------

        # Commit all successful inserts to database
        conn_tgt.commit()
        
        # Determine overall status based on whether any rows failed
        status = "SUCCESS" if rows_failed == 0 else "PARTIAL SUCCESS"

        # Log final ETL execution details into audit table
        log_audit(run_id, process_name,process_type, table_name, status, f"Failed rows: {rows_failed}", rows_inserted)

        # Print success summary message
        print(f"✅ {table_name} load complete. Success: {rows_inserted}, Failed: {rows_failed}")


    # If any major error occurs (like DB connection failure)
    except Exception as e:

        # Print critical error message
        print(f"❌ Critical Error in {process_name}: {e}")

        # Log failure status in audit table
        log_audit(run_id, process_name, table_name, "FAILED", str(e), 0)
        

    # Finally block always executes (cleanup section)
    finally:

        # Close cursor safely if it was created
        if cursor:
            cursor.close()

        # Close target database connection safely if it was created
        if conn_tgt:
            conn_tgt.close()