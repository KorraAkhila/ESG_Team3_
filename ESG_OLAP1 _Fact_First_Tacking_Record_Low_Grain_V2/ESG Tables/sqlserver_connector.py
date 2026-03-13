# sqlserver_loader.py

# --------------------------------------------------
# Import required libraries
# --------------------------------------------------

import pyodbc           # Used to connect Python to SQL Server
import pandas as pd     # Used for reading SQL data into DataFrames

# Import configuration dictionary (server, database, driver, etc.)
from config import CONFIG



# ==================================================
# OLTP CONNECTION FUNCTION
# ==================================================
def get_OLTP_connection():
    """
    Creates and returns a connection to the OLTP database.

    Uses configuration values from config.py:
        - driver
        - server
        - OLTP_database
    """

    # Build SQL Server connection string dynamically
    conn_str = (
        f"DRIVER={CONFIG['driver']};"          # ODBC driver name
        f"SERVER={CONFIG['server']};"          # SQL Server instance
        f"DATABASE={CONFIG['OLTP_database']};" # OLTP database name
        f"Trusted_Connection=yes;"             # Windows Authentication
    )

    # Return live connection object
    return pyodbc.connect(conn_str)







# ==================================================
# OLAP CONNECTION FUNCTION
# ==================================================
def get_connection_OLAP():
    """
    Creates and returns a connection to the OLAP database.

    Uses configuration values:
        - driver
        - server
        - OLAP_database
    """

    # Build connection string dynamically
    conn_str = (
        f"DRIVER={CONFIG['driver']};"           # ODBC driver
        f"SERVER={CONFIG['server']};"           # SQL Server instance
        f"DATABASE={CONFIG['OLAP_database']};"  # OLAP database name
        f"Trusted_Connection=yes;"              # Windows Authentication
    )

    # Return connection object
    return pyodbc.connect(conn_str)


