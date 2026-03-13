from datetime import datetime, date, timedelta

import random

import re

from constants import (
    SYSTEM_USER, FACILITY_TYPE_DATA, DATA_SOURCES, 
    FACILITY_TYPES_MASTER, EMISSION_EQUIPMENT_TYPES
)



def random_datetime_between(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


SYSTEM_USER = "system"


# =========================
# ORGANIZATION
# =========================
def gen_organization(row):
    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "created_date": datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
        "created_by": "system",
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


# =========================
# FACILITY TYPE
# =========================
def gen_facility_type(row):
    created_date = random_datetime_between(
        datetime(2020, 1, 1),
        datetime.now()
    )
    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "created_date": created_date,
        "created_by": "system",
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


# =========================
# FACILITY
# =========================
from datetime import datetime

# generate email for facility
def generate_facility_email(org_name, facility_name):
    # extract only facility part (after "-")
    if "-" in facility_name:
        facility_part = facility_name.split("-", 1)[1]
    else:
        facility_part = facility_name

    facility_part = re.sub(r"[^a-zA-Z0-9 ]", "", facility_part)
    facility_part = facility_part.strip().lower().replace(" ", ".")

    domain = re.sub(r"[^a-zA-Z0-9]", "", org_name).lower()

    return f"{facility_part}@{domain}.com"




def gen_facility(fid, org, facility_type_id):
    names = FACILITY_TYPE_DATA[facility_type_id]["names"]
    locations = FACILITY_TYPE_DATA[facility_type_id]["locations"]

    facility_label = random.choice(names)
    # location = random.choice(locations)
    CITIES = ["Mumbai, India", "Delhi, India", "Hyderabad,nIndia", "Chennai, India", "Bangalore, India", "Pune, India", "Ahmedabad, India", "Jaipur, India", "Lucknow, India", "Kanpur, India", "Nagpur, India", "Indore, India", "Thane, India", "Bhopal, India", "Visakhapatnam, India", "Pimpri-Chinchwad, India", "Patna, India", "Vadodara, India", "Ghaziabad, India", "Ludhiana, India"]

    location = random.choice(CITIES)

    facility_name = f"{org['name']} - {facility_label}"

    created = random_datetime_between(
        org["created_date"],
        datetime.now()
    )

    return {
        "id": fid,
        "name": facility_name,
        "organization_id": org["id"],
        "facility_type_id": facility_type_id,
        "location": location,
        "email": generate_facility_email(org["name"], facility_name),
        "created_date": created,
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


# =========================
# EMISSION EQUIPMENT TYPE
# =========================
def gen_emission_equipment_type(row):
    created_date = random_datetime_between(
        datetime(2020, 1, 1),
        datetime.now()
    )
    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "created_date": created_date,
        "created_by": "system",
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }




# =========================
# EMISSION SOURCE
# =========================
def gen_emission_source(
    i,
    facility_id,
    equipment
):
    install_date = date(
        random.randint(2018, datetime.now().year - 1),
        random.randint(1, 12),
        random.randint(1, 28)
    )


    equipment_name = equipment["name"]


    # Create realistic source name like Boiler-01, DG-Set-02
    source_name = f"{equipment_name}-{str(i).zfill(2)}"


    return {
        "id": i,
        "facility_id": facility_id,
        "equipment_type_id": equipment["id"],
        "name": source_name,                    # ✅ FIXED
        "source_code": f"SRC-{facility_id}-{i}",
        "capacity": round(random.uniform(1, 500), 2),
        "capacity_unit": random.choice(
            ["TPH", "kVA", "MW", "MT/hr", "MMSCFD"]
        ),
        "is_mobile_source": random.choice([0, 1]),
        "installation_date": install_date,
        "decommission_date": None,
        "description": f"{equipment_name} used for Scope-1 emission calculation",
        "created_date": random_datetime_between(
            datetime(install_date.year, 1, 1),
            datetime.now()
        ),
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }




# =========================
# MASTER TABLES
# =========================
def gen_fuel_type(row):
    created_date = random_datetime_between(
        datetime(2020, 1, 1),
        datetime.now()
    )


    return {
        "id": row[0],
        "name": row[1],
        "unit": row[2],
        "created_date": created_date,
        "created_by": "system",
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }




# =========================
# GAS TYPE
# =========================
def gen_gas_type(row):
    created_date = random_datetime_between(
        datetime(2020, 1, 1),
        datetime.now()
    )
    return {
        "id": row[0],
        "name": row[1],
        "unit": row[2],
        "created_date": created_date,
        "created_by": "system",
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }




# =========================
# STANDARD & METHOD
# =========================
def gen_standard(row):
    return {
        "id": row[0],
        "name": row[1],
        "issuing_authority": row[2],
        "version": row[3],
        "description": row[4],
        "created_date": random_datetime_between(
            datetime(2020, 1, 1),
            datetime.now()
        ),
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }



#=========================
# CALCULATION METHOD
#=========================
def gen_calculation_method(row):
    return {
        "id": row[0],
        "name": row[1],
        "formula": row[2],
        "standard_id": row[3],      # ✅ FK → standard.id
        "gas_type_id": row[4],      # ✅ FK → gas_type.id
        "unit_of_measure": row[5],
        "description": f"Calculation method for gas_type_id {row[4]}",
        "created_date": random_datetime_between(
            datetime(2020, 1, 1),
            datetime.now()
        ),
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }




# =========================
# EMISSION FACTOR
# =========================
def get_factor_for_period(factors, fuel_type_id, gas_id, period_year):
    """
    Find emission factor valid for fuel and year
    """

    for f in factors:
        if (
            f["fuel_type_id"] == fuel_type_id and
            f["gas_type_id"] == gas_id and
            f["effective_from"].year <= period_year <= f["effective_to"].year
        ):
            return f

    raise ValueError(
        f"No emission factor found for fuel={fuel_type_id} year={period_year}"
    )

def gen_emission_factor_yearly(
    factor_id,
    fuel_id,
    gas_id,
    standard_id,
    method_id,
    year
):
    start = date(year, 1, 1)
    end = date(year, 12, 31)

    return {
        "id": factor_id,
        "fuel_type_id": fuel_id,
        "gas_type_id": gas_id,
        "factor_value": round(random.uniform(1.2, 3.8), 6),
        "standard_id": standard_id,
        "calculation_method_id": method_id,
        "effective_from": start,
        "effective_to": end,
        "created_date": datetime(year, 1, 1),   # start of year
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }




# =========================
# REPORTING PERIOD
# =========================




def gen_reporting_period(i, year, month):
    # Determine start and end dates of the month
    start = date(year, month, 1)
    end = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)


    # Random created date within the reporting period
    created = random_datetime_between(
        datetime.combine(start, datetime.min.time()),
        datetime.combine(end, datetime.max.time())
    )


    quarter = (month - 1) // 3 + 1  # Q1=1, Q2=2, Q3=3, Q4=4

    return {
        "id": i,
        "start_date": start,
        "end_date": end,
        "year": year,
        "month": month,
        "quarter": quarter,
        "created_date": created,
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


# =========================
# DATA SOURCE
# =========================
def gen_data_source(i):
    return {
        "id": i,
        "name": DATA_SOURCES[(i - 1) % len(DATA_SOURCES)],
        "description": "Fuel consumption source",
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


# =========================
# FUEL CONSUMPTION
# =========================
def gen_fuel_consumption(
    i,
    facility_id,
    emission_source_id,
    fuel_type_id,
    period,
    document_id
):

    created = random_datetime_between(
        datetime.combine(period["start_date"], datetime.min.time()),
        datetime.combine(period["end_date"], datetime.max.time())
    )


    return {
        "id": i,
        "facility_id": facility_id,
        "emission_source_id": emission_source_id,
        "fuel_type_id": fuel_type_id,
        "reporting_period_id": period["id"],
        "quantity_consumed": round(random.uniform(100, 8000), 2),
        "document_type_id": document_id,
        "created_date": created,
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


# =========================
# SCOPE 1 EMISSION
# =========================
def gen_scope1_emission(
    emission_id,
    fuel_cons,
    reporting_period,
    factor
):
    created = fuel_cons["created_date"]

    emission_value = round(
        fuel_cons["quantity_consumed"] * factor["factor_value"],
        6
    )

    return {
        "id": emission_id,
        "facility_id": fuel_cons["facility_id"],
        "fuel_consumption_id": fuel_cons["id"],
        "emission_source_id": fuel_cons["emission_source_id"],
        "emission_factor_id": factor["id"],
        "gas_type_id": factor["gas_type_id"],
        "calculation_method_id": factor["calculation_method_id"],
        "emission_value": emission_value,
        "reporting_period_id": reporting_period["id"],
        "created_date": created,
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }







# def gen_scope1_emission(i, fuel_cons, factor_id, gas_id, calculation_id):
#     created = fuel_cons["created_date"] + timedelta(hours=random.randint(1, 72))
#     emission_value = (
#                             fuel_cons["quantity_consumed"] * random.uniform(1.2, 3.8)
#                             )
#     return {
#         "id": i,
#         "facility_id": fuel_cons["facility_id"],
#         "fuel_consumption_id": fuel_cons["id"],
#         "emission_source_id": fuel_cons["emission_source_id"],
#         "emission_factor_id": factor_id,
#         "gas_type_id": gas_id,
#         "calculation_method_id": calculation_id,  # Use data source ID as proxy for calculation method ID
        
#         "emission_value": round(emission_value, 6),

#         "emission_value": round(emission_value, 6),
#         "reporting_period_id": fuel_cons["reporting_period_id"],
#         "created_date": created,
#         "created_by": SYSTEM_USER,
#         "updated_by": None,
#         "updated_date": None,
#         "is_active": True
#     }
    




# =========================
# DOCUMENT & EVIDANCE
# =========================
def gen_document_type(row):
    return {
        "id": row[0],
        "name": row[1],
        "created_date": random_datetime_between(
            datetime(2020, 1, 1),
            datetime.now()
        ),
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


# =========================
# QUARTERLY EMISSION SUMMARY
# =========================
def gen_quarterly_emission(
    emission_id,
    facility_id,
    emission_source_id,
    fuel_type_id,
    gas_type_id,
    calculation_method_id,
    emission_factor_id,
    year,
    quarter,
    quarterly_fuel_qty,
    factor_value,
    reporting_period_id,
    created_date
):
    """
    Aggregated quarterly Scope-1 emission record.
    emission_value = sum of monthly fuel consumed in quarter × emission factor
    """
    emission_value = round(quarterly_fuel_qty * factor_value, 6)

    return {
        "id": emission_id,
        "facility_id": facility_id,
        "emission_source_id": emission_source_id,
        "fuel_type_id": fuel_type_id,
        "emission_factor_id": emission_factor_id,
        "gas_type_id": gas_type_id,
        "calculation_method_id": calculation_method_id,
        "year": year,
        "quarter": quarter,
        "quarterly_fuel_consumed": round(quarterly_fuel_qty, 2),
        "emission_value": emission_value,
        "reporting_period_id": reporting_period_id,   # last month's period in the quarter
        "created_date": created_date,
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


def gen_esg_evidance(i, emission, document_type_id):
    uploaded = emission["created_date"] + timedelta(days=random.randint(1, 7))
    return {
        "id": i,
        "scope1_emission_id": emission["id"],
        "document_type_id": document_type_id,
        "reporting_period_id": emission["reporting_period_id"],
        "file_path": f"/evidence/emission_{i}.pdf",
        "uploaded_date": uploaded,
        "uploaded_by": SYSTEM_USER,
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "updated_by": None,
        "updated_date": None,
        "is_active": True
    }


