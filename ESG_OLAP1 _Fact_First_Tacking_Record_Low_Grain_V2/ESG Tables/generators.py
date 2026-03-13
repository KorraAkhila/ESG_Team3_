# generators.py
# This file contains transformation (generator) functions for Dimension Tables


# Import random library to generate random numbers
import random



# Import datetime and timedelta to generate random dates
from datetime import datetime, timedelta



# Import CONFIG dictionary to get system user name
from config import CONFIG


# Define audit start date
START_DATE = datetime(2023, 1, 1)

# Define audit end date (current date and time)
END_DATE = datetime.now()


def random_audit_date():
    """
    Generate a random audit datetime between START_DATE and END_DATE.
    """

    # Calculate total time difference between start and end date
    delta = END_DATE - START_DATE

    # Generate random number of days within the range
    random_days = random.randint(0, delta.days)

    # Generate random number of seconds within a day (0–86399)
    random_seconds = random.randint(0, 86399)

    # Return random datetime value
    return START_DATE + timedelta(days=random_days, seconds=random_seconds)


# ============================================
# DIM FACILITY
# ============================================

def gen_dimFacility(row):
    """
    Transform OLTP Facility data into Dimension Facility format.
    """

    return {

        # Map FacilityId from OLTP source
        "FacilityId": row["FacilityId"],

        # Map FacilityName from OLTP source
        "FacilityName": row["FacilityName"],

        # Map FacilityTypeId from OLTP source
        "FacilityTypeId": row["FacilityTypeId"],

        # Map FacilityTypeName from OLTP source
        "FacilityTypeName": row["FacilityTypeName"],

        # Map OrganizationId from OLTP source
        "OrganizationId": row["OrganizationId"],

        # Map OrganizationName from OLTP source
        "OrganizationName": row["OrganizationName"],

        # Map Location from OLTP source
        "Location": row["Location"],

        # Generate random Created Date
        "CreatedDate": random_audit_date(),

        # Set CreatedBy using system user from config file
        "CreatedBy": CONFIG["system_user"],

        # UpdatedBy is NULL initially
        "UpdatedBy": None,

        # UpdatedDate is NULL initially
        "UpdatedDate": None
    }


# ============================================
# DIM EMISSION SOURCE
# ============================================


# Define a function that generates a DimEmissionType record
# This function takes one row (usually from source data) as input
def gen_DimEmissionType(row):

    # Return a dictionary (key-value pairs) representing one dimension record
    return {

        # Get EmissionTypeId value from the input row
        # This acts as the primary/business key for the emission type
        "EmissionTypeId": row["EmissionTypeId"],

        # Get EmissionTypeName from the input row
        # This is the descriptive name of the emission type
        "EmissionTypeName": row["EmissionTypeName"],

        # Set CreatedDate with a randomly generated audit date
        # random_audit_date() is a custom function that generates a date for auditing purposes
        "CreatedDate": random_audit_date(),

        # Set CreatedBy with system user value from CONFIG dictionary
        # CONFIG["system_user"] usually stores the ETL/system username
        "CreatedBy": CONFIG["system_user"],

        # Set UpdatedBy as None because this is a newly created record
        # It has not been updated yet
        "UpdatedBy": None,

        # Set UpdatedDate as None because no update has happened yet
        "UpdatedDate": None
    }
# ============================================
# DIM FUEL TYPE
# ============================================

def gen_DimFuelType(row):
    """
    Transform Fuel Type data into Dimension Fuel Type format.
    """

    return {

        # Keep SQL surrogate key
        "Id": row["Id"],

        # Map FuelTypeId
        "FuelTypeId": row["FuelTypeId"],

        # Map FuelTypeName
        "FuelTypeName": row["FuelTypeName"],

        # Map Fuel Unit
        "FuelUnit": row["FuelUnit"],

        # Map GasTypeId
        "GasTypeId": row["GasTypeId"],

        # Map Gas Name
        "GasName": row["GasName"],

        # Map Gas Unit
        "GasUnit": row["GasUnit"],

        # Generate random Created Date
        "CreatedDate": random_audit_date(),

        # Set CreatedBy
        "CreatedBy": CONFIG["system_user"],

        # UpdatedBy is NULL initially
        "UpdatedBy": None,

        # UpdatedDate is NULL initially
        "UpdatedDate": None
    }


# ============================================
# DIM TIME PERIOD
# ============================================

def gen_DimTimeperiod(row):
    """
    Transform Time Period data into Dimension Time Period format.
    """

    return {

        # Map TimeKey
        "TimeKey": row["TimeKey"],

        # Map Period Start Date
        "PeriodStartDate": row["PeriodStartDate"],

        # Map Period End Date
        "PeriodEndDate": row["PeriodEndDate"],

        # Map Reporting Year
        "Year": row["ReportingYear"],

        # Map Reporting Month
        "Month": row["ReportingMonth"],

        # Map Month Name
        "MonthName": row["MonthName"],

        # Map Quarter
        "Quarter": row["Quarter"],

        # Generate random Created Date
        "CreatedDate": random_audit_date(),

        # Set CreatedBy
        "CreatedBy": CONFIG["system_user"],

        # UpdatedBy is NULL initially
        "UpdatedBy": None,

        # UpdatedDate is NULL initially
        "UpdatedDate": None
    }