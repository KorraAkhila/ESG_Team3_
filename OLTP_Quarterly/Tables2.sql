

CREATE TABLE organization ( id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1
);

select * from organization 

----facility_type----

CREATE TABLE facility_type (
    id int PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1

);



select * from facility_type





-----facility---

CREATE TABLE facility (
    id INT PRIMARY KEY,
     name VARCHAR(255),
    organization_id INT NOT NULL,
    facility_type_id INT NOT NULL,
    location VARCHAR(255),
    email varchar(225),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1,

    CONSTRAINT fk_fac_org
        FOREIGN KEY (organization_id) REFERENCES organization(id),

    CONSTRAINT fk_fac_type
        FOREIGN KEY (facility_type_id) REFERENCES facility_type(id)
);



select * from facility


------emission_equipment_type------

CREATE TABLE emission_equipment_type (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1
);

select * from  emission_equipment_type

-----document_type------

CREATE TABLE document_type (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
     is_active BIT DEFAULT 1
);
select * from  document_type

----standard---

CREATE TABLE standard (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    issuing_authority VARCHAR(255),
    version VARCHAR(100),
    description VARCHAR(255),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1
);


select * from  standard

----gas_type---

CREATE TABLE gas_type (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1
);

select * from  gas_type

-----calculation_method----

CREATE TABLE calculation_method (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    formula VARCHAR(255),
    standard_id INT NOT NULL,
    gas_type_id INT NOT NULL,
    unit_of_measure VARCHAR(255),
    description VARCHAR(255),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1,

    CONSTRAINT fk_calc_standard
        FOREIGN KEY (standard_id) REFERENCES standard(id),

    CONSTRAINT fk_calc_gas
        FOREIGN KEY (gas_type_id) REFERENCES gas_type(id)
);

select * from  calculation_method

----fuel_type----

CREATE TABLE fuel_type (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1
);


select * from fuel_type


----emission_source--

CREATE TABLE emission_source (
    id INT PRIMARY KEY,
    facility_id INT NOT NULL,
    equipment_type_id INT NOT NULL,
    
    name VARCHAR(255),
    source_code VARCHAR(100),
    capacity DECIMAL(18,2),
    capacity_unit VARCHAR(50),
    is_mobile_source BIT,
    installation_date DATE,
    decommission_date DATE NULL,
    description VARCHAR(255),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1,

    CONSTRAINT fk_es_facility
        FOREIGN KEY (facility_id) REFERENCES facility(id),

    CONSTRAINT fk_es_equipment
        FOREIGN KEY (equipment_type_id) REFERENCES emission_equipment_type(id),

    
);

select * from emission_source

---- emission_factor---

CREATE TABLE emission_factor (
    id INT PRIMARY KEY,
    fuel_type_id INT NOT NULL,
    gas_type_id INT NOT NULL,
    factor_value DECIMAL(18,6),
    standard_id INT NOT NULL,
    calculation_method_id INT NOT NULL,
    effective_from DATE,
    effective_to DATE,
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1,

    CONSTRAINT fk_ef_fuel
        FOREIGN KEY (fuel_type_id) REFERENCES fuel_type(id),

    CONSTRAINT fk_ef_gas
        FOREIGN KEY (gas_type_id) REFERENCES gas_type(id),

    CONSTRAINT fk_ef_standard
        FOREIGN KEY (standard_id) REFERENCES standard(id),

    CONSTRAINT fk_ef_method
        FOREIGN KEY (calculation_method_id) REFERENCES calculation_method(id)
);


select * from emission_factor

-----reporting_period ----

CREATE TABLE reporting_period (
    id INT PRIMARY KEY,
    start_date DATE,
    end_date DATE,
    year INT,
    month INT,
    quarter INT,
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1,
);

select * from reporting_period

----fuel_consumption--

CREATE TABLE fuel_consumption (
    id INT PRIMARY KEY,
    facility_id INT NOT NULL,
    fuel_type_id INT NOT NULL,
    emission_source_id int not NULL,
    reporting_period_id INT NOT NULL,
    document_type_id INT NOT NULL,
    quantity_consumed DECIMAL(18,2),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1,

    CONSTRAINT fk_fc_facility
        FOREIGN KEY (facility_id) REFERENCES facility(id),

    CONSTRAINT fk_fc_fuel
        FOREIGN KEY (fuel_type_id) REFERENCES fuel_type(id),

    CONSTRAINT fk_fc_emission
        FOREIGN KEY (emission_source_id) REFERENCES emission_source(id),

    CONSTRAINT fk_fc_period
        FOREIGN KEY (reporting_period_id) REFERENCES reporting_period(id),

    CONSTRAINT fk_fc_doc
        FOREIGN KEY (document_type_id) REFERENCES document_type(id)
);

select * from fuel_consumption



----scope1_emission----

CREATE TABLE scope1_emission (
    id INT PRIMARY KEY,
    facility_id INT NOT NULL,
    fuel_consumption_id INT NOT NULL,
    emission_source_id INT NOT NULL,
    emission_factor_id INT NOT NULL,
    gas_type_id INT NOT NULL,
    calculation_method_id INT NOT NULL,
    emission_value DECIMAL(18,6),
    reporting_period_id INT NOT NULL,
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1,

    CONSTRAINT fk_s1_fac
        FOREIGN KEY (facility_id) REFERENCES facility(id),

    CONSTRAINT fk_s1_fc
        FOREIGN KEY (fuel_consumption_id) REFERENCES fuel_consumption(id),

    CONSTRAINT fk_s1_es
        FOREIGN KEY (emission_source_id) REFERENCES emission_source(id),

    CONSTRAINT fk_s1_factor
        FOREIGN KEY (emission_factor_id) REFERENCES emission_factor(id),

    CONSTRAINT fk_s1_gas
        FOREIGN KEY (gas_type_id) REFERENCES gas_type(id),

    CONSTRAINT fk_s1_method
        FOREIGN KEY (calculation_method_id) REFERENCES calculation_method(id),

    CONSTRAINT fk_s1_period
        FOREIGN KEY (reporting_period_id) REFERENCES reporting_period(id)
);


select * from fuel_consumption

----esg_evidance----

CREATE TABLE esg_evidance (
    id INT PRIMARY KEY,
    scope1_emission_id INT NOT NULL,
    document_type_id INT NOT NULL,
    reporting_period_id int not Null,
    file_path VARCHAR(500),
    uploaded_date DATETIME,
    uploaded_by VARCHAR(255),
    created_date DATETIME NOT NULL,
    created_by VARCHAR(255),
    updated_by VARCHAR(255) NULL,
    updated_date DATETIME NULL,
    is_active BIT DEFAULT 1,

    CONSTRAINT fk_ev_emission
        FOREIGN KEY (scope1_emission_id) REFERENCES scope1_emission(id),

    CONSTRAINT fk_ev_doc
        FOREIGN KEY (document_type_id) REFERENCES document_type(id),
    CONSTRAINT fk_ev_repo
        FOREIGN KEY (reporting_period_id) REFERENCES reporting_period(id)
);

select * from esg_evidance

select name from sys.tables


/* =========================================
   DROP ESG SCOPE 1 TABLES (FK SAFE ORDER)
   Database: esg_sample
   ========================================= */

-- Child / transactional tables
IF OBJECT_ID('dbo.esg_evidance', 'U') IS NOT NULL
    DROP TABLE dbo.esg_evidance;

IF OBJECT_ID('dbo.scope1_emission', 'U') IS NOT NULL
    DROP TABLE dbo.scope1_emission;

IF OBJECT_ID('dbo.fuel_consumption', 'U') IS NOT NULL
    DROP TABLE dbo.fuel_consumption;

IF OBJECT_ID('dbo.emission_factor', 'U') IS NOT NULL
    DROP TABLE dbo.emission_factor;

IF OBJECT_ID('dbo.reporting_period', 'U') IS NOT NULL
    DROP TABLE dbo.reporting_period;

IF OBJECT_ID('dbo.emission_source', 'U') IS NOT NULL
    DROP TABLE dbo.emission_source;

IF OBJECT_ID('dbo.facility', 'U') IS NOT NULL
    DROP TABLE dbo.facility;

-- Master / lookup tables
IF OBJECT_ID('dbo.document_type', 'U') IS NOT NULL
    DROP TABLE dbo.document_type;

IF OBJECT_ID('dbo.calculation_method', 'U') IS NOT NULL
    DROP TABLE dbo.calculation_method;

IF OBJECT_ID('dbo.standard', 'U') IS NOT NULL
    DROP TABLE dbo.standard;

IF OBJECT_ID('dbo.gas_type', 'U') IS NOT NULL
    DROP TABLE dbo.gas_type;

IF OBJECT_ID('dbo.fuel_type', 'U') IS NOT NULL
    DROP TABLE dbo.fuel_type;

IF OBJECT_ID('dbo.emission_equipment_type', 'U') IS NOT NULL
    DROP TABLE dbo.emission_equipment_type;

IF OBJECT_ID('dbo.facility_type', 'U') IS NOT NULL
    DROP TABLE dbo.facility_type;

IF OBJECT_ID('dbo.organization', 'U') IS NOT NULL
    DROP TABLE dbo.organization;

PRINT '✅ All ESG tables dropped successfully';





