# Import pandas library to work with structured data using DataFrames
import pandas as pd

# Import numpy library to handle numerical operations and NaN values
import numpy as np

# Import source and target database connection helper functions
from sqlserver_connector import get_OLTP_connection, get_connection_OLAP

# Import audit logging function and row-level error logging function
from audit_log import log_audit, log_row_error
from config import CONFIG

# Import dimension loading functions (used if foreign key data is missing)
from load_dim_facility import load_dim_facility
from load_dim_emission_Type import load_dim_emission_type
from load_dim_fuel_type import load_dim_fuel_type
from load_dim_timeperiod import load_dim_timeperiod


# --------------------------------------------------
# SQL Query for Fact Table Extraction
# --------------------------------------------------

# Define SQL query to extract aggregated Scope 1 emission data
FactScope1Emissions = """
        -- Select minimum ID to act as SourceId
        SELECT 
    --MIN(se.id) AS Id,
<<<<<<< HEAD
    --ROW_NUMBER() OVER (ORDER BY se.facility_id) AS Id,
=======
    ROW_NUMBER() OVER (ORDER BY se.facility_id) AS Id,
>>>>>>> 430e410 (Initial commit)

    -- Get Facility foreign key
    se.facility_id AS DimFacilityId,

    -- Get Emission Type foreign key
    et.id AS DimEmissionTypeId,

    -- Get Fuel Type foreign key
    fc.fuel_type_id AS DimFuelTypeId,

    -- Create TimeKey in YYYYMM format
    (YEAR(rp.end_date) * 100 + MONTH(rp.end_date)) AS TimeKey,

    -- Aggregate total fuel consumed
    SUM(fc.quantity_consumed) AS FuelQuantity,

    -- Aggregate total emission value
    SUM(se.emission_value) AS EmissionValue,

    -- Get Gas Type
    se.gas_type_id AS GasTypeId

-- Main source table
FROM scope1_emission se

-- Join fuel consumption table
JOIN fuel_consumption fc 
    ON fc.id = se.fuel_consumption_id

-- Join reporting period table
JOIN reporting_period rp 
    ON rp.id = se.reporting_period_id

-- Join emission source table
JOIN emission_source es
    ON es.id = se.emission_source_id

-- Join equipment type table
JOIN emission_equipment_type et
    ON et.id = es.equipment_type_id

-- Filter only active records
WHERE se.is_active = 'True'

-- Group by required columns for aggregation
GROUP BY
    se.facility_id,
    et.id,
    fc.fuel_type_id,
    (YEAR(rp.end_date) * 100 + MONTH(rp.end_date)),
    se.gas_type_id
    """


# Create a set to track which dimension tables were already triggered
triggered_dims = set()


# Define helper function to check if a record already exists in a table
def record_exists(cursor, table_name, pk_column, pk_value):

    # Execute query to count records matching primary key value
    cursor.execute(f"SELECT COUNT(1) FROM {table_name} WHERE {pk_column} = ?", (pk_value,))

    # Return True if record exists, otherwise False
    return cursor.fetchone()[0] > 0


# Define helper function to check foreign key existence
# If missing, dynamically load the required dimension
def smart_dim_load(cursor, table_name, column_name, value, load_function, run_id):

    # Check if foreign key value exists in dimension table
    cursor.execute(f"SELECT COUNT(1) FROM {table_name} WHERE {column_name} = ?", (value,))

    # If record does not exist
    if cursor.fetchone()[0] == 0:

        # Ensure dimension loader runs only once per session
        if table_name not in triggered_dims:

            # Print message indicating missing dimension record
            print(f"🔍 [CHECK] Key {value} missing in {table_name}. Calling Loader...")

            # Call respective dimension load function
            load_function(run_id)

            # Add table name to triggered set to prevent duplicate runs
            triggered_dims.add(table_name)


# Main ETL function for loading FactScope1Emissions
def load_fact_scope1(run_id):
    process_name = "load_fact_scope1.py"
    process_type = CONFIG["Fact_process"]
    table_name = "FactScope1Emissions"
    triggered_dims.clear() 

    print(f"\n--- Starting Optimized ETL Session: {run_id} ---")
    
    # 1. EXTRACT
    conn_src = get_OLTP_connection()
    df = pd.read_sql(FactScope1Emissions, conn_src)
    conn_src.close() 

<<<<<<< HEAD
    

    df["CreatedBy"] = CONFIG["system_user"]
    
=======
    df = df.rename(columns={'Id': 'SourceId'})
    df = df.replace({np.nan: None})
>>>>>>> 430e410 (Initial commit)
    total_records = len(df)

    # 2. PREPARE TARGET & CACHE DIMENSIONS
    conn_tgt = get_connection_OLAP()
    cursor = conn_tgt.cursor()

    print("🧠 Caching dimension keys for speed...")
<<<<<<< HEAD
    # Cache existing Ids to skip duplicates
    cursor.execute(f"SELECT Id FROM {table_name}")
=======
    # Cache existing SourceIds to skip duplicates
    cursor.execute(f"SELECT SourceId FROM {table_name}")
>>>>>>> 430e410 (Initial commit)
    existing_source_ids = {row[0] for row in cursor.fetchall()}

    # Cache dimension keys (Adjust column names to match your DW schema)
    cursor.execute("SELECT FacilityId FROM DimFacility")
    cache_facility = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT EmissionTypeId FROM DimEmissionType")
    cache_emission = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT FuelTypeId FROM DimFuelType")
    cache_fuel = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT TimeKey FROM DimTimeperiod")
    cache_time = {row[0] for row in cursor.fetchall()}

    # 3. ROW-BY-ROW PROCESSING (With Instant Lookups)
    rows_inserted = 0
    rows_skipped = 0
    rows_failed = 0

<<<<<<< HEAD
    cursor.execute("SELECT DimFacilityId, DimEmissionTypeId, DimFuelTypeId, TimeKey FROM FactScope1Emissions")
    # Store them as a set of tuples
    # Convert each pyodbc.Row object into a standard Python tuple
    existing_records = {tuple(row) for row in cursor.fetchall()}
    # 3. ROW-BY-ROW PROCESSING
    for index, row in df.iterrows():
        # Create the composite key to check for existing records
        
        current_key = (row['DimFacilityId'], row['DimEmissionTypeId'], row['DimFuelTypeId'], row['TimeKey'])
        current_row = index + 1
        
        # This is your primary defense against duplicates
        if current_key in existing_records:
            rows_skipped += 1
            continue
        
        try:
            # A. VALIDATE FOREIGN KEYS (Only call DB if NOT in cache)
            # Facility check
            if row['DimFacilityId'] not in cache_facility:
                smart_dim_load(cursor, "DimFacility", "FacilityId", row['DimFacilityId'], load_dim_facility, run_id)
                cache_facility.add(row['DimFacilityId']) 

            # Emission Type check
=======
    for index, row in df.iterrows():
        current_row = index + 1
        
        try:
            # A. PREVENT DUPLICATE RECORDS (Using Local Set)
            if row['SourceId'] in existing_source_ids:
                rows_skipped += 1
                continue

            # B. VALIDATE FOREIGN KEYS (Only call DB if NOT in cache)
            if row['DimFacilityId'] not in cache_facility:
                smart_dim_load(cursor, "DimFacility", "FacilityId", row['DimFacilityId'], load_dim_facility, run_id)
                cache_facility.add(row['DimFacilityId']) # Update cache

>>>>>>> 430e410 (Initial commit)
            if row['DimEmissionTypeId'] not in cache_emission:
                smart_dim_load(cursor, "DimEmissionType", "EmissionTypeId", row['DimEmissionTypeId'], load_dim_emission_type, run_id)
                cache_emission.add(row['DimEmissionTypeId'])

<<<<<<< HEAD
            # Fuel Type check
=======
>>>>>>> 430e410 (Initial commit)
            if row['DimFuelTypeId'] not in cache_fuel:
                smart_dim_load(cursor, "DimFuelType", "FuelTypeId", row['DimFuelTypeId'], load_dim_fuel_type, run_id)
                cache_fuel.add(row['DimFuelTypeId'])

<<<<<<< HEAD
            # Time check
=======
>>>>>>> 430e410 (Initial commit)
            if row['TimeKey'] not in cache_time:
                smart_dim_load(cursor, "DimTimeperiod", "TimeKey", row['TimeKey'], load_dim_timeperiod, run_id)
                cache_time.add(row['TimeKey'])

<<<<<<< HEAD
            # B. INSERT FACT RECORD
            # Ensure df.columns matches the target table exactly (excluding 'Id')
=======
            # C. INSERT FACT RECORD
>>>>>>> 430e410 (Initial commit)
            columns = ",".join(df.columns)
            placeholders = ",".join(["?"] * len(df.columns))
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
<<<<<<< HEAD
            
            cursor.execute(insert_sql, (
                row['DimFacilityId'],
                row['DimEmissionTypeId'],
                row['DimFuelTypeId'],
                row['TimeKey'],
                row['FuelQuantity'],
                row['EmissionValue'],
                row['GasTypeId'],
                row['CreatedBy']
                ))
            rows_inserted += 1
            
            # Batch Commit
=======
            cursor.execute(insert_sql, tuple(row))
            rows_inserted += 1
            
            # Commit in batches for performance
>>>>>>> 430e410 (Initial commit)
            if rows_inserted % 100 == 0:
                conn_tgt.commit()

        except Exception as row_error:
            rows_failed += 1
<<<<<<< HEAD
            log_row_error(run_id, process_name, table_name, row.to_dict(), str(row_error))
=======
            log_row_error(run_id, process_name, process_type, table_name, row.to_dict(), str(row_error))

>>>>>>> 430e410 (Initial commit)
    # 4. FINALIZATION
   
    # ... rest of your logging logic ...
    try:

        # Final commit for any remaining records
        conn_tgt.commit() 
        
        # Print summary report
        print("\n" + "="*30)
        print(f"✅ LOAD FINISHED: {table_name}")
        print(f"✨ New Records: {rows_inserted}")
        print(f"⏭️  Skipped: {rows_skipped}")
        print(f"❌ Failed: {rows_failed}")
        print("="*30)
        
        # Determine final status
        status = "SUCCESS" if rows_failed == 0 else "PARTIAL SUCCESS"

        # Log summary into audit table
        log_audit(run_id, process_name,process_type, table_name, status, f"Failed rows: {rows_failed}", rows_inserted)

    # Handle final commit failure
    except Exception as e:

        # Print final commit error
        print(f"❌ FINAL COMMIT ERROR: {e}")

        # Log failure in audit table
        log_audit(run_id, process_name, table_name, "FAILED", str(e), 0)

    # Always close database connections
    finally:

        # Close cursor
        cursor.close()

        # Close target connection
        conn_tgt.close()