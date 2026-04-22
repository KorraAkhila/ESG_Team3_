use ESG_OLAP



----CO2 EMISSION YTD---

SELECT
    FORMAT(ROUND(SUM(s.EmissionValue) / 1000000.0, 2), 'N2') + ' kt'
    AS CO2_Emission_YTD
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE t.PeriodStartDate
BETWEEN DATEFROMPARTS(YEAR(GETDATE()), 1, 1)
AND GETDATE();


----- CO2 EMISSION PYTD---


DECLARE @LastCompletedMonth DATE = EOMONTH(GETDATE(), -2);

SELECT
    FORMAT(
        SUM(f.EmissionValue) / 1000000.0,
        '0.0'
    ) + ' kt' AS CO2_Emission_PYTD

FROM FactScope1Emissions f
JOIN DimTimeperiod t
    ON t.TimeKey = f.TimeKey

WHERE
    -- Previous Year
    YEAR(t.PeriodStartDate) = YEAR(@LastCompletedMonth) - 1

    -- From Jan 1 (YTD)
    AND t.PeriodStartDate >= DATEFROMPARTS(YEAR(@LastCompletedMonth) - 1, 1, 1)

    -- Till same month last year
    AND t.PeriodStartDate <= EOMONTH(DATEADD(YEAR, -1, @LastCompletedMonth));








   ----CO2_EMISSION_QTD---

SELECT
    FORMAT(ROUND(SUM(s.EmissionValue) / 1000000.0, 2), 'N2') + ' kt'
    AS CO2_Emission_QTD
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE t.PeriodStartDate
BETWEEN DATEADD(QUARTER, DATEDIFF(QUARTER, 0, GETDATE()), 0)
AND GETDATE();


---- CO2  Emission MTD---

SELECT
    FORMAT(ROUND(SUM(s.EmissionValue) / 1000000.0, 2), 'N2') + ' kt'
    AS  CO2_Emission_MTD
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE t.PeriodStartDate
BETWEEN DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) - 1, 0)
AND EOMONTH(GETDATE(), -1);


----- Co2 Emission by Year,Quarter,Month (2022) ----

SELECT 
    YEAR(t.PeriodStartDate) AS Year,
    DATEPART(QUARTER, t.PeriodStartDate) AS Quarter,
    MONTH(t.PeriodStartDate) AS Month,
    SUM(s.EmissionValue) / 1000000.0 AS Scope1_Emission_MKg
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE YEAR(t.PeriodStartDate) = 2022
GROUP BY 
    YEAR(t.PeriodStartDate),
    DATEPART(QUARTER, t.PeriodStartDate),
    MONTH(t.PeriodStartDate)
ORDER BY 
    Quarter, Month;



----- Co2 Emission by Year,Quarter,Month (2023) ----
SELECT 
    YEAR(t.PeriodStartDate) AS Year,
    DATEPART(QUARTER, t.PeriodStartDate) AS Quarter,
    MONTH(t.PeriodStartDate) AS Month,
    SUM(s.EmissionValue) / 1000000.0 AS Scope1_Emission_MKg
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE YEAR(t.PeriodStartDate) = 2023
GROUP BY 
    YEAR(t.PeriodStartDate),
    DATEPART(QUARTER, t.PeriodStartDate),
    MONTH(t.PeriodStartDate)
ORDER BY 
    Quarter, Month;


    ----- Co2 Emission by Year,Quarter,Month (2024) ----
SELECT 
    YEAR(t.PeriodStartDate) AS Year,
    DATEPART(QUARTER, t.PeriodStartDate) AS Quarter,
    MONTH(t.PeriodStartDate) AS Month,
    SUM(s.EmissionValue) / 1000000.0 AS Scope1_Emission_MKg
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE YEAR(t.PeriodStartDate) = 2024
GROUP BY 
    YEAR(t.PeriodStartDate),
    DATEPART(QUARTER, t.PeriodStartDate),
    MONTH(t.PeriodStartDate)
ORDER BY 
    Quarter, Month;


    ----- Co2 Emission by Year,Quarter,Month (2025) ----
SELECT 
    YEAR(t.PeriodStartDate) AS Year,
    DATEPART(QUARTER, t.PeriodStartDate) AS Quarter,
    MONTH(t.PeriodStartDate) AS Month,
    SUM(s.EmissionValue) / 1000000.0 AS Scope1_Emission_MKg
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE YEAR(t.PeriodStartDate) = 2025
GROUP BY 
    YEAR(t.PeriodStartDate),
    DATEPART(QUARTER, t.PeriodStartDate),
    MONTH(t.PeriodStartDate)
ORDER BY 
    Quarter, Month;



    ----- Co2 Emission by Year,Quarter,Month (2026) ----
SELECT 
    YEAR(t.PeriodStartDate) AS Year,
    DATEPART(QUARTER, t.PeriodStartDate) AS Quarter,
    MONTH(t.PeriodStartDate) AS Month,
    SUM(s.EmissionValue) / 1000000.0 AS Scope1_Emission_MKg
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE YEAR(t.PeriodStartDate) = 2026
GROUP BY 
    YEAR(t.PeriodStartDate),
    DATEPART(QUARTER, t.PeriodStartDate),
    MONTH(t.PeriodStartDate)
ORDER BY 
    Quarter, Month;


    ---- CO2 EMission By Facility Type ---

WITH Top5 AS (
    SELECT TOP 5
        DF.FacilityTypeName,
        SUM(f.EmissionValue) AS Scope1_Emission_kg
    FROM FactScope1Emissions f
    JOIN DimFacility DF
        ON DF.Id = f.DimFacilityId
    GROUP BY DF.FacilityTypeName
    ORDER BY Scope1_Emission_kg DESC
)

SELECT
    FacilityTypeName,
    FORMAT(Scope1_Emission_kg / 1000000.0, '0.0') + ' kt' AS [Co2_Emission_kt],
    -- Formatted as a percentage string
    FORMAT(
        (Scope1_Emission_kg * 1.0) / SUM(Scope1_Emission_kg) OVER (),
        'P2'
    ) AS Pct_of_Top5
FROM Top5
ORDER BY Scope1_Emission_kg DESC;



----- Top 3 CO2 Emission by organizaion -----

WITH OrgEmission AS (
    SELECT
        f.OrganizationName,

        -- Organization Short Name (same as DAX logic)
        CASE
            WHEN CHARINDEX(' ', f.OrganizationName) = 0
                THEN f.OrganizationName
            ELSE
                (
                    SELECT STRING_AGG(LEFT(value,1), '')
                    FROM STRING_SPLIT(f.OrganizationName, ' ')
                )
        END AS OrganizationShortName,

        SUM(s.EmissionValue) / 1000000.0 AS Emission_MKg

    FROM FactScope1Emissions s
    JOIN DimFacility f
        ON s.DimFacilityId = f.Id
    JOIN DimTimeperiod t
        ON s.TimeKey = t.TimeKey

    GROUP BY
        f.OrganizationName
)

SELECT TOP 3
    OrganizationShortName,
    Emission_MKg
FROM OrgEmission
ORDER BY
    Emission_MKg DESC;




    ----- Top 5 CO2 Emission by city -----

WITH CityEmission AS (
    SELECT
        -- Extract City (same as DAX logic)
        CASE
            WHEN CHARINDEX(',', f.Location) > 0
                THEN LEFT(f.Location, CHARINDEX(',', f.Location) - 1)
            ELSE f.Location
        END AS City,

        SUM(s.EmissionValue) / 1000000.0 AS Emission_MKg

    FROM FactScope1Emissions s
    JOIN DimFacility f
        ON s.DimFacilityId = f.Id
    JOIN DimTimeperiod t
        ON s.TimeKey = t.TimeKey

    GROUP BY
        CASE
            WHEN CHARINDEX(',', f.Location) > 0
                THEN LEFT(f.Location, CHARINDEX(',', f.Location) - 1)
            ELSE f.Location
        END
)

SELECT TOP 5
    City,
    Emission_MKg
FROM CityEmission
ORDER BY
    Emission_MKg DESC;





    ---- CO2 EMission By Facility ---

WITH Top5 AS (
    SELECT TOP 5
        DF.FacilityName,
        SUM(f.EmissionValue) AS Scope1_Emission_kg
    FROM FactScope1Emissions f
    JOIN DimFacility DF
        ON DF.Id = f.DimFacilityId
    GROUP BY DF.FacilityName
    ORDER BY Scope1_Emission_kg DESC
)

SELECT
    FacilityName,

    -- Formatted as a percentage string----
    FORMAT(
        (Scope1_Emission_kg * 1.0) / SUM(Scope1_Emission_kg) OVER (),
        'P2'
    ) AS Pct_of_Top5
FROM Top5
ORDER BY Scope1_Emission_kg DESC;



----- Top 5 co2 emission by fuels ----

select top 5 dt.FuelTypeName, FORMAT(ROUND(SUM(s.EmissionValue) / 1000000.0, 1), 'N2') + ' kt'
as total_fuelemision_consumed from FactScope1Emissions s
join DimFuelType dt on
dt.Id=s.DimFuelTypeId
group by dt.FuelTypeName
order by SUM(s.EmissionValue) / 1000000.0 desc






select * from DimEmissionType
select * from DimFacility
select * from DimFuelType
select * from DimTimeperiod
select * from FactScope1Emissions



-----------
SELECT COUNT(*) 
FROM FactScope1Emissions s
JOIN DimTimeperiod t
ON s.TimeKey = t.TimeKey
WHERE t.PeriodStartDate 
BETWEEN DATEADD(QUARTER, DATEDIFF(QUARTER, 0, GETDATE()), 0)
AND GETDATE();

---------- Max date from table   feb table data till feb (QTD) ----
SELECT 
    FORMAT(
        ROUND(SUM(ISNULL(s.EmissionValue,0)) / 1000000.0, 2), 
        'N2'
    ) + ' kt' AS CO2_Emission_QTD
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE t.PeriodStartDate
BETWEEN 
    DATEADD(QUARTER, DATEDIFF(QUARTER, 0, 
        (SELECT MAX(t2.PeriodStartDate)
         FROM FactScope1Emissions s2
         JOIN DimTimeperiod t2 ON s2.TimeKey = t2.TimeKey)
    ), 0)
AND 
    (SELECT MAX(t3.PeriodStartDate)
     FROM FactScope1Emissions s3
     JOIN DimTimeperiod t3 ON s3.TimeKey = t3.TimeKey);



     -------- MAX Dynamic MTD till feb ----

     SELECT 
    FORMAT(
        ROUND(SUM(ISNULL(s.EmissionValue,0)) / 1000000.0, 2), 
        'N2'
    ) + ' kt' AS CO2_Emission_MTD
FROM FactScope1Emissions s
JOIN DimTimeperiod t
    ON s.TimeKey = t.TimeKey
WHERE t.PeriodStartDate
BETWEEN 
    DATEADD(MONTH, DATEDIFF(MONTH, 0, 
        (SELECT MAX(t2.PeriodStartDate)
         FROM FactScope1Emissions s2
         JOIN DimTimeperiod t2 ON s2.TimeKey = t2.TimeKey)
    ), 0)
AND 
    (SELECT MAX(t3.PeriodStartDate)
     FROM FactScope1Emissions s3
     JOIN DimTimeperiod t3 ON s3.TimeKey = t3.TimeKey);

















  ----- By Bottom 3 organization------

     WITH OrgEmission AS (
    SELECT
        f.OrganizationName,
        CASE
            WHEN CHARINDEX(' ', f.OrganizationName) = 0
                THEN f.OrganizationName
            ELSE
                (
                    SELECT STRING_AGG(LEFT(value,1), '')
                    FROM STRING_SPLIT(f.OrganizationName, ' ')
                )
        END AS OrganizationShortName,
        SUM(s.EmissionValue) / 1000000.0 AS Emission_MKg
    FROM FactScope1Emissions s
    JOIN DimFacility f
        ON s.DimFacilityId = f.Id
    JOIN DimTimeperiod t
        ON s.TimeKey = t.TimeKey
    GROUP BY
        f.OrganizationName
)
SELECT TOP 3
    OrganizationShortName,
    Emission_MKg
FROM OrgEmission
ORDER BY
    Emission_MKg ASC;