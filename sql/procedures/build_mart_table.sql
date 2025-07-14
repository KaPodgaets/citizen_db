-- sql/procedures/build_mart_table.sql

/*-----------------------------------------------------------
DESCRIPTION
av-bait - main (base) table for mart

-----------------------------------------------------------*/

/*-----------------------------------------------------------
Refresh mart.citizen  (atomic swap pattern)
-----------------------------------------------------------*/
SET XACT_ABORT ON;
BEGIN TRY
BEGIN TRAN;

------------------------------------------------------------
-- 1. Ensure work table exists & is empty
------------------------------------------------------------
IF OBJECT_ID('tempdb..#citizens_work') IS NOT NULL
    DROP TABLE #citizens_work;

/* Work table mirrors target */
CREATE TABLE #citizens_work
(
    citizen_id            INT           PRIMARY KEY,
    first_name            NVARCHAR(255),
    last_name             NVARCHAR(255),
    age                   INT,
    street_name           NVARCHAR(255),
    street_code           NVARCHAR(50),
    building_number       NVARCHAR(20),
    apartment_number      NVARCHAR(20),
    family_index_number   INT,
    has_phone             BIT,
    has_mobile_phone      BIT,
    is_welfare_patient    BIT,
    is_new_imigrant       BIT,
    has_breath_troubles   BIT,
    is_hazramim           BIT,
    phone1                NVARCHAR(20),
    phone2                NVARCHAR(20),
    phone3                NVARCHAR(20)
);

------------------------------------------------------------
-- 2. Populate work table
------------------------------------------------------------

with base as (
    select
        citizen_id
        , first_name
        , last_name
        , age
        , street_name
        , street_code
        , building_number
        , apartment_number
        , family_index_number
    from core.av_bait avb
    where is_current = 1
), welfare_patients_cte as (
    select
        citizen_id
        , 1 as is_welfare_patient
    from core.welfare_patients
    where is_current = 1
    group by citizen_id
), phones as (
    select 
        citizen_id
        , phone_number
        , type
        , ROW_NUMBER() OVER (
            PARTITION BY citizen_id
            ORDER BY type DESC, phone_number
        ) as rn
    from core.phone_numbers
)

INSERT INTO #citizens_work (
    citizen_id,
    first_name,
    last_name,
    age,
    street_name,
    street_code,
    building_number,
    apartment_number,
    family_index_number,
    has_phone,
    has_mobile_phone,
    is_welfare_patient,
    is_new_imigrant,
    has_breath_troubles,
    is_hazramim,
    phone1,
    phone2,
    phone3
)
SELECT
    b.citizen_id,
    b.first_name,
    b.last_name,
    b.age,
    b.street_name,
    b.street_code,
    b.building_number,
    b.apartment_number,
    b.family_index_number,
    /* phone flags */
    CASE WHEN COUNT(p.phone_number) > 0 THEN 1 ELSE 0 END AS has_phone,
    CASE WHEN SUM(CASE WHEN p.type = 'mobile' THEN 1 ELSE 0 END) > 0
         THEN 1 ELSE 0 END as has_mobile_phone,
    /* flags */
    MAX(CASE WHEN COALESCE(w.citizen_id, 0) > 0 THEN 1 ELSE 0 END) AS is_welfare_patient,
    0 as is_new_imigrant,           -- TODO: join to core.absorption
    0 as has_breath_troubles,       -- TODO: join to core.absorption
    0 as is_hazramim,               -- TODO: join to core.absorption
    /* phones */
    MAX(CASE WHEN p.rn = 1 THEN p.phone_number END) AS phone1,
    MAX(CASE WHEN p.rn = 2 THEN p.phone_number END) AS phone2,
    MAX(CASE WHEN p.rn = 3 THEN p.phone_number END) AS phone3
FROM base as b
LEFT JOIN welfare_patients_cte AS w ON b.citizen_id = w.citizen_id
LEFT JOIN phones AS p ON b.citizen_id = p.citizen_id
GROUP BY
    b.citizen_id, b.first_name, b.last_name, b.age,
    b.street_name, b.street_code, b.building_number,
    b.apartment_number, b.family_index_number,
    w.is_welfare_patient;


------------------------------------------------------------
-- 3. Swap work → production (minimises lock time)
------------------------------------------------------------
TRUNCATE TABLE mart.citizens;
INSERT INTO mart.citizens
SELECT * FROM #citizens_work;

COMMIT;   -- success
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK;
    THROW;
END CATCH;