# audit_log.py

# Import the OLAP database connection function from sqlserver_loader module.
# We are renaming (aliasing) it as get_connection for easier usage inside this file.
from sqlserver_connector import get_connection_OLAP as get_connection

# audit_log.py additions
from datetime import datetime # Add this at the top


# Define a function called log_audit.
# This function is used to insert ETL execution details into the audit_log table.
# Parameters:
# RUN_ID          → Unique ID for the ETL run
# process_name    → Name of the process (Example: ETL_Load)
# table_name      → Name of the table being processed
# status          → Status of execution (Success / Failed)
# error_message   → Error details (if any error occurs)
# rows_affected   → Number of rows inserted/updated
def log_audit(RUN_ID, process_name,process_type, table_name, status, error_message=None, rows_affected=None):

    # Start a try block to handle possible runtime errors safely.
    try:

        # Establish connection to the OLAP database.
        # This calls get_connection() which internally connects to SQL Server.
        conn = get_connection()

        # Create a cursor object.
        # Cursor is used to execute SQL queries.
        cursor = conn.cursor()

        # Define the SQL INSERT query using triple quotes (multi-line string).
        # This query inserts execution details into audit_log table.
        query = """
        INSERT INTO audit_log
        (run_id, process_name,process_type, table_name, status,
         error_message, rows_affected, execution_time)
        VALUES (?, ?, ?, ?,?, ?, ?, GETDATE())
        """

        # Important:
        # ? are placeholders (parameterized query).
        # They prevent SQL Injection and safely pass values into SQL query.
        # GETDATE() is a SQL Server function that inserts current date & time.

        # Execute the SQL query.
        # The values are passed as a tuple in the same order as placeholders.
        cursor.execute(query, (
            RUN_ID,          # Value for run_id
            process_name,    # Value for process_name
            process_type,
            table_name,      # Value for table_name
            status,          # Value for status
            error_message,   # Value for error_message
            rows_affected    # Value for rows_affected
        ))

        # Commit the transaction.
        # This permanently saves the inserted record into the database.
        conn.commit()

    # If any error occurs inside try block, control comes here.
    except Exception as e:

        # Print error message to console.
        # This helps in debugging if audit logging fails.
        print("Audit logging failed:", e)

    # Finally block always executes whether error occurs or not.
    finally:

        # Close the cursor to release database resources.
        cursor.close()

        # Close the database connection.
        # Closing connection is very important to avoid memory leaks.
        conn.close()

# ----------------------------
# ROW LEVEL ERROR LOGGING
# ----------------------------

# Define a function to log row-level errors into the database
# Parameters:
# run_id -> Unique ID for the ETL run
# process_name -> Name of the process (e.g., ETL_Load)
# table_name -> Name of the table where error occurred
# failed_row -> The actual row data that failed
# error_message -> The error message generated
def log_row_error(run_id, process_name, table_name, failed_row, error_message):

    # Start a try block to handle any errors during logging
    try:

        # Create a database connection using the existing connection function
        conn = get_connection()

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        
        # Define the SQL INSERT query to store row-level error details
        # '?' are placeholders used to safely pass values (prevents SQL injection)
        query = """
            INSERT INTO log_row_error 
            (run_id, process_name, table_name, execution_date, failed_row_data, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        # Execute the INSERT query and pass actual values to replace placeholders
        cursor.execute(query, (

            # Insert the run ID
            run_id,

            # Insert the process name
            process_name,

            # Insert the table name
            table_name,

            # Insert the current date and time as execution date
            datetime.now(),

            # Convert the failed row data to string before storing in database
            str(failed_row), 

            # Convert the error message to string before storing
            str(error_message)
        ))
        
        # Commit the transaction to permanently save data into the database
        conn.commit()

    # If any error occurs while logging, control comes here
    except Exception as e:

        # Print a critical message to console if error logging itself fails
        print(f"Critical: Failed to log row error to database: {e}")

    # This block always executes whether error occurs or not
    finally:

        # Close the cursor to release database resources
        cursor.close()

        # Close the database connection to avoid memory leaks
        conn.close()