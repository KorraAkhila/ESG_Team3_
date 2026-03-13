 

# Import dimension load functions
from load_dim_facility import load_dim_facility
# from load_dim_emission_source import load_dim_emission_source
from load_dim_emission_Type import load_dim_emission_type
from load_dim_fuel_type import load_dim_fuel_type
from load_dim_timeperiod import load_dim_timeperiod

# Import fact load function
from load_fact_scope1 import load_fact_scope1

# Import uuid library to generate unique Run ID
import uuid

# Import warnings module
import warnings

# Ignore unnecessary UserWarning messages during execution
warnings.filterwarnings("ignore", category=UserWarning)

# Generate a unique ID for this ETL execution
# Example: 550e8400-e29b-41d4-a716-446655440000
# This ID is used for audit logging
RUN_ID = uuid.uuid4()



# This block runs only if this file is executed directly
# It will NOT run if this file is imported into another file
if __name__ == "__main__":




    # ===============================
    # 3️⃣ LOAD FACT TABLE
    # ===============================



    # Load Scope 1 Emissions fact table
    # Uses dimension keys already loaded above
    load_fact_scope1(RUN_ID)





    # ===============================
    # 2️⃣ LOAD DIMENSIONS FIRST
    # ===============================
    # Dimensions must be loaded before facts
    # Because fact table depends on dimension keys (Foreign Keys)


    # # Load Facility dimension
    # load_dim_facility(RUN_ID)
    
    # # Load Emission Source dimension
    # load_dim_emission_type(RUN_ID)
   

    # # Load Fuel Type dimension
    # load_dim_fuel_type(RUN_ID)
    

    # # Load Time dimension
    # load_dim_timeperiod(RUN_ID)
    



    


    # Print completion message
    print("✅ ETL Completed Successfully")
    