from datetime import datetime, date, timedelta
import random

SYSTEM_USER = "system"

# =========================
# MASTER CONSTANTS
# =========================
FACILITY_TYPES = ["Plant", "Office", "Warehouse"]
EQUIPMENT_TYPES = ["Boiler", "Generator", "Furnace", "Vehicle"]
FUEL_TYPES = [("Diesel", "Liters"), ("Petrol", "Liters"), ("Natural Gas", "SCM")]
GAS_TYPES = [("CO2", "kg"), ("CH4", "kg"), ("N2O", "kg")]
STANDARDS = ["GHG Protocol", "ISO 14064"]
METHODS = ["Fuel Based", "Distance Based"]
DATA_SOURCES = ["Meter Reading", "Invoice", "ERP Export"]
DOCUMENT_TYPES = ["Invoice", "Meter Photo", "Fuel Receipt"]

# =========================
# DATE UTIL
# =========================
def random_datetime_between(start, end):
    if start >= end:
        return start
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# =========================
# ORGANIZATION
# =========================
def gen_organization(i, start_year):
    start = datetime(start_year, 1, 1)
    created = random_datetime_between(start, datetime.now())
    return {
        "id": i,
        "name": f"Organization {i}",
        "description": "Corporate organization",
        "created_date": created,
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# FACILITY TYPE
# =========================
def gen_facility_type(i):
    return {
        "id": f"FT{i}",
        "facility_type_name": FACILITY_TYPES[(i-1) % len(FACILITY_TYPES)],
        "description": "Facility type",
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# FACILITY
# =========================
def gen_facility(i, org_id, facility_type_id, org_created):
    created = random_datetime_between(org_created, datetime.now())
    return {
        "id": i,
        "organization_id": org_id,
        "facility_name": f"Facility {i}",
        "facility_type_id": facility_type_id,
        "location": "India",
        "created_date": created,
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# EMISSION EQUIPMENT TYPE
# =========================
def gen_emission_equipment_type(i):
    return {
        "id": i,
        "equipment_name": EQUIPMENT_TYPES[(i-1) % len(EQUIPMENT_TYPES)],
        "description": "Emission equipment",
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# EMISSION SOURCE
# =========================
def gen_emission_source(i, equipment_type_id):
    return {
        "id": i,
        "source_name": f"Source {i}",
        "equipment_type_id": equipment_type_id,
        "description": "Direct emission source",
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# FUEL / GAS / STANDARD / METHOD
# =========================
def gen_fuel_type(i):
    name, unit = FUEL_TYPES[(i-1) % len(FUEL_TYPES)]
    return {
        "id": i,
        "fuel_name": name,
        "unit": unit,
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

def gen_gas_type(i):
    name, unit = GAS_TYPES[(i-1) % len(GAS_TYPES)]
    return {
        "id": i,
        "gas_name": name,
        "unit": unit,
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

def gen_standard(i):
    return {
        "id": i,
        "standard_name": STANDARDS[(i-1) % len(STANDARDS)],
        "description": "Emission reporting standard",
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

def gen_calculation_method(i):
    return {
        "id": i,
        "method_name": METHODS[(i-1) % len(METHODS)],
        "description": "Emission calculation method",
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# EMISSION FACTOR
# =========================
def gen_emission_factor(i, fuel_id, gas_id, standard_id, method_id):
    return {
        "id": i,
        "fuel_type_id": fuel_id,
        "gas_type_id": gas_id,
        "factor_value": round(random.uniform(1.2, 3.8), 6),
        "standard_id": standard_id,
        "calculation_method_id": method_id,
        "effective_from": date(2020, 1, 1),
        "effective_to": None,
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# REPORTING PERIOD
# =========================
def gen_reporting_period(i, year, month):
    start = date(year, month, 1)
    end = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    created = random_datetime_between(
        datetime.combine(start, datetime.min.time()),
        datetime.combine(end, datetime.max.time())
    )
    return {
        "id": i,
        "start_date": start,
        "end_date": end,
        "year": year,
        "month": month,
        "created_date": created,
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# DATA SOURCE
# =========================
def gen_data_source(i):
    return {
        "id": i,
        "source_name": DATA_SOURCES[(i-1) % len(DATA_SOURCES)],
        "description": "Fuel consumption source",
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# FUEL CONSUMPTION
# =========================
def gen_fuel_consumption(i, facility_id, fuel_type_id, period, data_source_id):
    created = random_datetime_between(
        datetime.combine(period["start_date"], datetime.min.time()),
        datetime.combine(period["end_date"], datetime.max.time())
    )
    return {
        "id": i,
        "facility_id": facility_id,
        "fuel_type_id": fuel_type_id,
        "reporting_period_id": period["id"],
        "quantity": round(random.uniform(100, 8000), 2),
        "data_source_id": data_source_id,
        "created_date": created,
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# SCOPE 1 EMISSION
# =========================
def gen_scope1_emission(i, fuel_cons, factor_id):
    created = fuel_cons["created_date"] + timedelta(hours=random.randint(1, 72))
    return {
        "id": i,
        "facility_id": fuel_cons["facility_id"],
        "fuel_consumption_id": fuel_cons["id"],
        "emission_factor_id": factor_id,
        "emission_value": round(random.uniform(100, 20000), 6),
        "reporting_period_id": fuel_cons["reporting_period_id"],
        "created_date": created,
        "created_by": SYSTEM_USER,
        "is_active": True
    }

# =========================
# DOCUMENT / EVIDANCE
# =========================
def gen_document_type(i):
    return {
        "id": i,
        "document_name": DOCUMENT_TYPES[(i-1) % len(DOCUMENT_TYPES)],
        "created_date": datetime.now(),
        "created_by": SYSTEM_USER,
        "is_active": True
    }

def gen_esg_evidance(i, emission, document_type_id):
    uploaded = emission["created_date"] + timedelta(days=random.randint(1, 7))
    return {
        "id": i,
        "scope1_emission_id": emission["id"],
        "document_type_id": document_type_id,
        "file_path": f"/evidence/emission_{i}.pdf",
        "uploaded_date": uploaded,
        "uploaded_by": SYSTEM_USER,
        "is_active": True
    }
