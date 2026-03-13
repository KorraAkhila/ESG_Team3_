Create database ESG_SCOPE1_OLAP
use ESG_SCOPE1_OLAP


-- 1. Create Dimension: Facility
<<<<<<< HEAD
--CREATE TABLE DimFacility (
--    Id INT PRIMARY KEY,
--    FacilityId INT NOT NULL,
--    FacilityName NVARCHAR(255) NOT NULL,
--    FacilityTypeId INT,
--    FacilityTypeName NVARCHAR(255),
--    OrganizationId INT,
--    OrganizationName NVARCHAR(255),
--    Location NVARCHAR(500),
--    CreatedDate DATETIME2 DEFAULT GETDATE(),
--    CreatedBy NVARCHAR(255),
--    UpdatedBy NVARCHAR(255),
--    UpdatedDate DATETIME2
--);
=======
CREATE TABLE DimFacility (
    Id INT PRIMARY KEY,
    FacilityId INT NOT NULL,
    FacilityName NVARCHAR(255) NOT NULL,
    FacilityTypeId INT,
    FacilityTypeName NVARCHAR(255),
    OrganizationId INT,
    OrganizationName NVARCHAR(255),
    Location NVARCHAR(500),
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    CreatedBy NVARCHAR(255),
    UpdatedBy NVARCHAR(255),
    UpdatedDate DATETIME2
);
>>>>>>> 430e410 (Initial commit)

-- 2. Create Dimension: Emission Source (Equipment)
CREATE TABLE DimEmissionSource (
    Id INT PRIMARY KEY,
    EmissionSourceId INT NOT NULL,
    EmissionSourceName NVARCHAR(255) NOT NULL,
    EmissionSourceCode NVARCHAR(255),
    EquipmentCategoryId INT,
    EquipmentCategory NVARCHAR(255),
    EquipmentCapacity DECIMAL(18, 4),
    CapacityUnit NVARCHAR(50),
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    CreatedBy NVARCHAR(255),
    UpdatedBy NVARCHAR(255),
    UpdatedDate DATETIME2
);

-- 3. Create Dimension: Fuel Type
CREATE TABLE DimFuelType (
    Id INT PRIMARY KEY,
    FuelTypeId INT NOT NULL,
    FuelTypeName NVARCHAR(100) NOT NULL,
    FuelUnit NVARCHAR(255),
    GasTypeId INT,
    GasName NVARCHAR(255),
    GasUnit NVARCHAR(255),
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    CreatedBy NVARCHAR(255),
    UpdatedBy NVARCHAR(255),
    UpdatedDate DATETIME2
);

-- 4. Create Dimension: Time Period
CREATE TABLE DimTimeperiod (
    TimeKey INT PRIMARY KEY, -- Usually formatted as YYYYMM
    PeriodStartDate DATE,
    PeriodEndDate DATE,
    Year INT,
    Month INT,
    MonthName NVARCHAR(255),
    Quarter NVARCHAR(20),
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    CreatedBy NVARCHAR(255),
    UpdatedBy NVARCHAR(255),
    UpdatedDate DATETIME2
);

-- 5. Create Fact Table: Scope 1 Emissions
CREATE TABLE FactScope1Emissions (
    Id INT PRIMARY KEY,
    DimFacilityId INT NOT NULL,
<<<<<<< HEAD
    DimEmissionTypeId INT NOT NULL,
=======
    DimEmissionSourceId INT NOT NULL,
>>>>>>> 430e410 (Initial commit)
    DimFuelTypeId INT NOT NULL,
    TimeKey INT NOT NULL,
    FuelQuantity DECIMAL(18, 6),
    EmissionValue DECIMAL(18, 6),
    GasTypeId INT,
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    CreatedBy NVARCHAR(255),
    UpdatedDate DATETIME2,
    UpdatedBy NVARCHAR(255),

    -- Foreign Key Constraints
    CONSTRAINT FK_Fact_Facility FOREIGN KEY (DimFacilityId) 
        REFERENCES DimFacility(Id),
<<<<<<< HEAD
    CONSTRAINT FK_Fact_EmissionType FOREIGN KEY (DimEmissionTypeId) 
        REFERENCES DimEmissionType(Id),
=======
    CONSTRAINT FK_Fact_EmissionSource FOREIGN KEY (DimEmissionSourceId) 
        REFERENCES DimEmissionSource(Id),
>>>>>>> 430e410 (Initial commit)
    CONSTRAINT FK_Fact_FuelType FOREIGN KEY (DimFuelTypeId) 
        REFERENCES DimFuelType(Id),
    CONSTRAINT FK_Fact_TimePeriod FOREIGN KEY (TimeKey) 
        REFERENCES DimTimeperiod(TimeKey)
);

<<<<<<< HEAD











CREATE TABLE FactScope1Emissions
(
    -- Surrogate Key
    Id BIGINT IDENTITY(1,1) PRIMARY KEY,

    -- Dimension Foreign Keys
    DimFacilityId INT NOT NULL,
    DimEmissionTypeId INT NOT NULL,
    DimFuelTypeId INT NOT NULL,
    TimeKey INT NOT NULL,

    -- Measures
    FuelQuantity DECIMAL(18,4) NOT NULL,
    EmissionValue DECIMAL(18,6) NOT NULL,

    -- Additional Attribute
    GasTypeId INT NULL,

    -- Audit Columns
    CreatedBy VARCHAR(100) NOT NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),

    -- Foreign Key Constraints
    CONSTRAINT FK_Fact_Facility
        FOREIGN KEY (DimFacilityId)
        REFERENCES DimFacility(Id),

    CONSTRAINT FK_Fact_EmissionType
        FOREIGN KEY (DimEmissionTypeId)
        REFERENCES DimEmissionType(Id),

    CONSTRAINT FK_Fact_FuelType
        FOREIGN KEY (DimFuelTypeId)
        REFERENCES DimFuelType(Id),

    CONSTRAINT FK_Fact_Time
        FOREIGN KEY (TimeKey)
        REFERENCES DimTimeperiod(TimeKey),

    -- Prevent duplicate fact rows
    CONSTRAINT UQ_FactScope1
    UNIQUE
    (
        DimFacilityId,
        DimEmissionTypeId,
        DimFuelTypeId,
        TimeKey
    )
);












Drop table FactScope1Emissions
select Name from sys.tables
=======
>>>>>>> 430e410 (Initial commit)
-- Create Indexes for Power BI performance
CREATE INDEX IX_Fact_Facility ON FactScope1Emissions(DimFacilityId);
CREATE INDEX IX_Fact_EmissionSource ON FactScope1Emissions(DimEmissionSourceId);
CREATE INDEX IX_Fact_FuelType ON FactScope1Emissions(DimFuelTypeId);
CREATE INDEX IX_Fact_TimeKey ON FactScope1Emissions(TimeKey);

Select * from FactScope1Emissions











<<<<<<< HEAD
=======

>>>>>>> 430e410 (Initial commit)
---✅ SQL — Calculate Scope-1 emission value (year-based factor)

---This query calculates emission dynamically (without using stored scope1_emission).
select * from facility
SELECT
    f.id AS facility_id,
    f.name,

    es.id AS emission_source_id,
    es.name,

    fc.id AS fuel_consumption_id,
    fc.quantity_consumed,

    rp.id AS reporting_period_id,
    rp.year AS reporting_year,

    ef.id AS emission_factor_id,
    ef.factor_value,

    -- FINAL CALCULATION
    fc.quantity_consumed * ef.factor_value AS calculated_emission_value

FROM facility f

JOIN emission_source es
    ON es.facility_id = f.id

JOIN fuel_consumption fc
    ON fc.emission_source_id = es.id

    JOIN reporting_period rp
        ON rp.id = fc.reporting_period_id

    -- YEAR BASED FACTOR MATCH
    JOIN emission_factor ef
        ON ef.fuel_type_id = fc.fuel_type_id
        AND rp.year BETWEEN YEAR(ef.effective_from)
                        AND YEAR(ef.effective_to)
        AND ef.calculation_method_id = 1
        AND ef.is_active = 1



--⭐ If you want to compare with stored Scope-1 values
select * from scope1_emission

--This verifies correctness.

SELECT
    se.id AS scope1_id,
    fc.quantity_consumed,
    ef.factor_value,

    -- stored value
    se.emission_value AS stored_emission,

    -- recalculated value
    fc.quantity_consumed * ef.factor_value AS recalculated_emission,

    -- difference
    se.emission_value -
    (fc.quantity_consumed * ef.factor_value) AS difference

FROM scope1_emission se

JOIN fuel_consumption fc
    ON se.fuel_consumption_id = fc.id

JOIN reporting_period rp
    ON se.reporting_period_id = rp.id

JOIN emission_factor ef
    ON ef.id = se.emission_factor_id

    select organization_id ,count(*) as total from facility group by organization_id order by total desc







SELECT 
    se.id AS Id,
    se.facility_id AS DimFacilityId,
    se.emission_source_id AS DimEmissionSourceId,
    fc.fuel_type_id AS DimFuelTypeId,
    (YEAR(rp.end_date) * 100 + MONTH(rp.end_date)) AS TimeKey,
    fc.quantity_consumed AS FuelQuantity,
    se.emission_value AS EmissionValue,
    fc.quantity_consumed AS QuantityConsumed,
    se.gas_type_id AS GasTypeId
FROM scope1_emission se
JOIN fuel_consumption fc ON se.fuel_consumption_id = fc.id
JOIN reporting_period rp ON se.reporting_period_id = rp.id
WHERE se.is_active = 'True'






<<<<<<< HEAD
CREATE TABLE DimEmissionType
(
    Id INT IDENTITY(1,1) PRIMARY KEY,
    EmissionTypeId INT NOT NULL,
    EmissionTypeName VARCHAR(150) NOT NULL,
    CreatedDate DATETIME DEFAULT GETDATE(),
    CreatedBy VARCHAR(100),
    UpdatedDate DATETIME,
    UpdatedBy VARCHAR(100)
);

Drop table DimEmissionType
=======


>>>>>>> 430e410 (Initial commit)

SELECT
    
    se.facility_id,
    sum(fc.quantity_consumed) as quantity_consumed,
    sum(ef.factor_value) factor_value,

    -- stored value
    sum(se.emission_value) AS stored_emission,

    -- recalculated value
    sum(fc.quantity_consumed * ef.factor_value) AS recalculated_emission,

    -- difference
    sum(se.emission_value -
    (fc.quantity_consumed * ef.factor_value)) AS difference

FROM scope1_emission se

JOIN fuel_consumption fc
    ON se.fuel_consumption_id = fc.id

JOIN reporting_period rp
    ON se.reporting_period_id = rp.id

JOIN emission_factor ef
    ON ef.id = se.emission_factor_id
Group by se.facility_id;



CREATE TABLE audit_log (
    audit_id INT IDENTITY(1,1) PRIMARY KEY,
    process_name VARCHAR(100),
    table_name VARCHAR(100),
    status VARCHAR(20),              -- SUCCESS / FAILED
    error_message VARCHAR(MAX),
    rows_affected INT,
    execution_time DATETIME DEFAULT GETDATE()
);

<<<<<<< HEAD
drop table FactScope1Emissions
=======

>>>>>>> 430e410 (Initial commit)

ALTER TABLE audit_log
ADD run_id UNIQUEIDENTIFIER NOT NULL
    CONSTRAINT DF_audit_log_run_id DEFAULT NEWID();

    select * from audit_log

<<<<<<< HEAD
    select * from log_row_error

    trunCATE TABLE audit_log

    select name from sys.tables

=======
    trunCATE TABLE audit_log

>>>>>>> 430e410 (Initial commit)
    select * from FactScope1Emissions

    SELECT * FROM DimFuelType

    SELECT * FROM DimTimePeriod

<<<<<<< HEAD
    SELECT * FROM DimEmissionType

    select * from DimFacility
=======
    SELECT * FROM DimEmissionSource




    SELECT 
    --MIN(se.id) AS Id,
    --ROW_NUMBER() OVER (ORDER BY se.facility_id) AS Id,

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
>>>>>>> 430e410 (Initial commit)
