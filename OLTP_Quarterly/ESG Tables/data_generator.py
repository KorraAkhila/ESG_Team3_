from pathlib import Path
import pandas as pd
import random
import os
from datetime import datetime
from config import CONFIG
from generators import *
from generators import gen_scope1_emission
from sqlserver_loader import load_data

from constants import (
     EQUIPMENT_FUEL_MAP, FACILITY_TYPES_MASTER, EMISSION_EQUIPMENT_TYPES,
    DOCUMENT_TYPES_MASTER, FUEL_TYPES_MASTER, GAS_TYPES_MASTER,
    STANDARDS, CALCULATION_METHODS
)

def load_organizations():
    """
    Load organizations from sibling folder:
    EIGHT_ATT_MODIFIED2_EMISSION_FACTOR/Resource/organizations.xlsx
    """

    # folder where data_generator.py exists
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    # go one level UP → project root
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

    # build full path
    file_path = os.path.join(
        PROJECT_ROOT,
        CONFIG["resource_folder"],
        CONFIG["organization_excel_file"]
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Organization Excel not found: {file_path}")

    df = pd.read_excel(file_path)

    required = ["id", "organization_name", "description", "created_date"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column in organizations.xlsx: {col}")

    return df.to_dict("records")

def write_excel(table, rows, folder, file_name):
    Path(folder).mkdir(exist_ok=True)
    path = Path(folder) / file_name
    df = pd.DataFrame(rows)


    # 🔥 If file does not exist OR first table, create new file
    if not path.exists() or table == "organization":
        with pd.ExcelWriter(path, engine="openpyxl", mode="w") as w:
            df.to_excel(w, sheet_name=table, index=False)
    else:
        with pd.ExcelWriter(path, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
            df.to_excel(w, sheet_name=table, index=False)


    print(f"✅ {table}: {len(rows)} rows")




def main():
    data={}
    MIN = CONFIG["min_rows"]
    folder = CONFIG["output_folder"]
    file_name = CONFIG["excel_file"]


    now = datetime.now()
    start_year = now.year - CONFIG["start_year_offset"]


    # ORGANIZATION



    # =========================
    # ORGANIZATION (FROM EXCEL)
    # =========================

    org_rows = load_organizations()
    organizations = [gen_organization(
        (
            r["id"],
            r["organization_name"],
            r["description"],
            str(r["created_date"])
        )
    ) for r in org_rows]

    write_excel("organization", organizations, folder, file_name)




    # FACILITY TYPE



    # FACILITY TYPE
    facility_types = [gen_facility_type(r) for r in FACILITY_TYPES_MASTER]
    data["facility_type"] = facility_types

    # FACILITY (4–8 per organization)


    write_excel("facility_type", facility_types, folder, file_name)




    # FACILITY
    # =========================
    # FACILITY (OPTIMIZED)
    # =========================

    facilities = []
    append = facilities.append  # local reference (faster)

    facility_id = 1
    facility_type_ids = [ft["id"] for ft in facility_types]

    for org in organizations:

    # generate 4–8 facilities per organization
        num_facilities = random.randint(4, 8)

        for _ in range(num_facilities):
            ft_id = random.choice(facility_type_ids)

        # uses your generator (includes email automatically)
            append(
                gen_facility(
                    facility_id,
                    org,
                    ft_id
                )
            )

            facility_id += 1

    # assign AFTER loop
    data["facility"] = facilities

    # write ONCE (important)
    write_excel("facility", facilities, folder, file_name)




    # EQUIPMENT & SOURCE

    equipment_types = [
        gen_emission_equipment_type(row)
        for row in EMISSION_EQUIPMENT_TYPES
    ]

    write_excel("emission_equipment_type", equipment_types, folder, file_name)

    # Only keep equipment types that have a defined fuel mapping
    mappable_equipment = [
        eq for eq in equipment_types
        if eq["name"] in EQUIPMENT_FUEL_MAP
    ]

     # DOCUMENT & EVIDANCE
    docs = [
        gen_document_type(row)
        for row in DOCUMENT_TYPES_MASTER
    ]


    write_excel("document_type", docs, folder, file_name)










       # MASTER TABLES



    fuel_types = [
        gen_fuel_type(row)
        for row in FUEL_TYPES_MASTER
    ]
    fuel_lookup = {f["name"]: f for f in fuel_types}


   





    gas_types = [
        gen_gas_type(row)
        for row in GAS_TYPES_MASTER
    ]




    # =========================
    # STANDARD
    # =========================
    standard = [
        gen_standard(row)
        for row in STANDARDS
    ]


   




    # =========================
    # CALCULATION METHOD
    # =========================
    # 1. Generate master data
    calculation_methods = [
        gen_calculation_method(row)
        for row in CALCULATION_METHODS
    ]

    # 2. Read active gas from config
    ACTIVE_GAS_ID = CONFIG["active_gas_id"]

    # 3. Build mapping
    gas_method_map = {}
    for method in calculation_methods:
        gas_method_map.setdefault(
            method["gas_type_id"], []
        ).append(method)

    # 4. Validate
    if ACTIVE_GAS_ID not in gas_method_map:
        raise ValueError(
            f"No calculation method found for gas_type_id {ACTIVE_GAS_ID}"
        )

    # 5. Select method
    active_calculation_method = gas_method_map[ACTIVE_GAS_ID][0]







    write_excel("calculation_method", calculation_methods, folder, file_name)





    write_excel("fuel_type", fuel_types, folder, file_name)
    write_excel("gas_type", gas_types, folder, file_name)
    write_excel("standard", standard, folder, file_name)
   
    # write_excel("data_source", data_sources, folder, file_name)


    # =========================
    # EMISSION SOURCE
    # =========================
   
    emission_sources = []
    source_id = 1


    # 3-LEVEL HIERARCHY: facility → equipment_type → sources
    # Each facility gets 2–4 distinct equipment types.
    # Each equipment type within a facility gets 2–4 emission sources.

    MIN_EQUIP_PER_FACILITY   = 2
    MAX_EQUIP_PER_FACILITY   = 4
    MIN_SOURCES_PER_EQUIP    = 2
    MAX_SOURCES_PER_EQUIP    = 4

    # Track which (facility, equipment_type) combos were used for fuel_consumption
    facility_equipment_sources = {}   # (facility_id, equipment_type_id) → [source, ...]

    for facility in facilities:
        # Pick a distinct set of equipment types for this facility
        num_equip = random.randint(MIN_EQUIP_PER_FACILITY, MAX_EQUIP_PER_FACILITY)
        selected_equipment = random.sample(
            mappable_equipment,
            min(num_equip, len(mappable_equipment))
        )

        equip_source_counter = {}   # equipment_type_id → local counter for naming

        for equipment in selected_equipment:
            eq_id   = equipment["id"]
            eq_name = equipment["name"]
            equip_source_counter[eq_id] = 0

            num_sources = random.randint(MIN_SOURCES_PER_EQUIP, MAX_SOURCES_PER_EQUIP)

            for _ in range(num_sources):
                equip_source_counter[eq_id] += 1
                local_num = equip_source_counter[eq_id]

                src = gen_emission_source(
                    source_id,
                    facility["id"],
                    equipment,
                )
                # Override name to reflect hierarchy clearly: EquipName-FacilityId-LocalNum
                src["name"] = f"{eq_name}-{facility['id']:02d}-{local_num:02d}"
                src["source_code"] = f"SRC-{facility['id']}-{eq_id}-{local_num}"

                emission_sources.append(src)

                facility_equipment_sources.setdefault(
                    (facility["id"], eq_id), []
                ).append(src)

                source_id += 1

    write_excel("emission_source", emission_sources, folder, file_name)


    # =========================
    # GROUP SOURCES BY FACILITY
    # =========================

    sources_by_facility = {}

    for src in emission_sources:
        sources_by_facility.setdefault(
            src["facility_id"], []
        ).append(src)






        # EMISSION FACTOR
    # =========================
    # EMISSION FACTOR (YEARLY VERSIONED)
    # =========================

    

    START_YEAR = 2022
    END_YEAR = 2026

    factors = []
    factor_id = 1

    for fuel in fuel_types:
        for year in range(START_YEAR, END_YEAR + 1):
            factors.append(
                gen_emission_factor_yearly(
                    factor_id,
                    fuel["id"],
                    ACTIVE_GAS_ID,
                    CONFIG["active_standard_id"],
                    active_calculation_method["id"],
                    year
                )
            )
            factor_id += 1

    write_excel("emission_factor", factors, folder, file_name)




      # REPORTING PERIOD (3–4 YEARS)
    periods, pid = [], 1
    for y in range(start_year, now.year + 1):
        for m in range(1, 13):
            if y == now.year and m > now.month-1:
                break
            periods.append(gen_reporting_period(pid, y, m))
            pid += 1
    write_excel("reporting_period", periods, folder, file_name)






    # FUEL CONSUMPTION — one record per source per period (quarterly cadence)
    # Group reporting periods by (year, quarter) → pick 3–4 quarters per facility
    fuel_cons = []
    fc_id = 1

    # Build a lookup: period_id → period dict
    period_by_id = {p["id"]: p for p in periods}

    # Group periods by (year, quarter)
    from collections import defaultdict
    quarters_map = defaultdict(list)   # (year, quarter) → [period, ...]
    for p in periods:
        quarters_map[(p["year"], p["quarter"])].append(p)

    all_quarters = sorted(quarters_map.keys())   # chronological order

    for facility_id, sources in sources_by_facility.items():

        # Each facility gets all available complete quarters
        # (partial current quarter is excluded for clean OLAP data)
        facility_quarters = [
            q for q in all_quarters
            if len(quarters_map[q]) == 3    # only fully completed quarters (3 months)
        ]

        for (year, quarter) in facility_quarters:
            quarter_periods = quarters_map[(year, quarter)]   # up to 3 months

            for src in sources:
                # Look up fuel via equipment_type_id → equipment name → EQUIPMENT_FUEL_MAP
                eq_type_id = src["equipment_type_id"]
                eq_obj = next((e for e in mappable_equipment if e["id"] == eq_type_id), None)
                possible_fuels = EQUIPMENT_FUEL_MAP.get(eq_obj["name"]) if eq_obj else None

                if possible_fuels:
                    fuel_name = random.choice(possible_fuels)
                    fuel = fuel_lookup[fuel_name]
                else:
                    fuel = random.choice(fuel_types)

                doc = random.choice(docs)

                # One fuel consumption record per month within the quarter
                for period in quarter_periods:
                    fuel_cons.append(
                        gen_fuel_consumption(
                            fc_id,
                            facility_id,
                            src["id"],
                            fuel["id"],
                            period,
                            doc["id"]
                        )
                    )
                    fc_id += 1



    write_excel("fuel_consumption", fuel_cons, folder, file_name)






 
   


    # =========================
    # SCOPE 1 EMISSION — MONTHLY GRAIN
    # =========================
    # One emission record per fuel_consumption row (i.e. per source per month).
    # fuel_consumption and scope1_emission will always have equal row counts.

    emissions = []
    emission_id = 1

    for fc in fuel_cons:
        period = period_by_id[fc["reporting_period_id"]]

        factor = get_factor_for_period(
            factors,
            fc["fuel_type_id"],
            ACTIVE_GAS_ID,
            period["year"]
        )

        emissions.append(
            gen_scope1_emission(
                emission_id,
                fc,
                period,
                factor
            )
        )
        emission_id += 1

    write_excel("scope1_emission", emissions, folder, file_name)



    # emissions = []
    # existing_keys = set()
    # emission_id = 1

    # for fc in fuel_cons:

    #     key = (
    #         fc["facility_id"],
    #         fc["emission_source_id"],
    #         fc["reporting_period_id"]
    #     )

    #     # Skip if already created
    #     if key in existing_keys:
    #         continue

    #     factor = random.choice(factors)

    #     emissions.append(
    #         gen_scope1_emission(
    #             emission_id,
    #             fc,
    #             factor["id"],
    #             factor["gas_type_id"],
    #             factor["calculation_method_id"]
    #         )
    #     )

    #     existing_keys.add(key)
    #     emission_id += 1











    evid = [
        gen_esg_evidance(i + 1, e, random.choice(docs)["id"])
        for i, e in enumerate(emissions)
    ]
    write_excel("esg_evidance", evid, folder, file_name)






   
   


   


   


    print("\n🎉 ESG Scope-1 dataset generated successfully (last 3–4 years)")
    print("\n📥 Loading generated Excel data into SQL Server...")
    load_data()



if __name__ == "__main__":
    main()


