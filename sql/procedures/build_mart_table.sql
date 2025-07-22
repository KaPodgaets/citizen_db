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
    fake_citizen_id       BIGINT NOT NULL,
    citizen_id            INT           PRIMARY KEY,
    first_name            NVARCHAR(255),
    last_name             NVARCHAR(255),
    age                   INT,
    street_name           NVARCHAR(255),
    street_code           NVARCHAR(50),
    building_number       NVARCHAR(20),
    apartment_number      NVARCHAR(20),
    family_index_number   INT,
    is_living_alone       BIT NOT NULL,
    is_elder_pair         BIT NOT NULL,
    has_phone             BIT,
    has_mobile_phone      BIT,
    is_welfare_patient    BIT,
    is_new_imigrant       BIT,
    has_breath_troubles   BIT,
    is_hazramim           BIT,
    phone1                NVARCHAR(20),
    phone2                NVARCHAR(20),
    phone3                NVARCHAR(20),
    is_in_hamal_batch     BIT,
    file_name_hamal       NVARCHAR(255),
    is_dead_hamal         BIT,
    is_left_the_city_permanent BIT,
    is_answered_the_call  BIT,
    has_final_status        BIT,
    is_lonely               BIT,
    is_address_wrong        BIT,
    new_street_name         NVARCHAR(100) NULL,
    new_building_number     NVARCHAR(10) NULL,
    new_appartment_number   NVARCHAR(10) NULL,
    has_mamad               BIT,
    has_miklat_prati        BIT,
    has_miklat_ziburi       BIT,
    has_mobility_restriction BIT,
    has_temporary_address   BIT,
    is_temporary_abroad     BIT,
    temporary_street_name   NVARCHAR(100) NULL,
    temporary_building_number NVARCHAR(10) NULL,
    temporary_appartment    NVARCHAR(10) NULL,
    appearance_count        INT NULL,
    calcenter_case_number   NVARCHAR(10) NULL,
    is_final_status         BIT
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
        , is_living_alone
        , is_elder_pair
    from core.av_bait avb
    where is_current = 1
), fake_ids as (
    select citizen_id
    , fake_citizen_id
    from core.fake_citizen_ids
), welfare_patients_cte as (
    select
        citizen_id
        , 1 as is_welfare_patient
    from core.welfare_patients
    where is_current = 1
    group by citizen_id
), new_immigrants_cte as (
    select
        citizen_id
        , 1 as is_new_imigrant
    from core.new_immigrants
    where is_current = 1
    group by citizen_id
), hazramim_cte as (
    select 
        citizen_id
        , 1 as is_hazramim
    from 
        core.hazramim
    where is_current = 1
), breath_troubles_cte as (
    select 
        citizen_id
        , 1 as is_breath_trobles
    from 
        core.breath_troubles
    where is_current = 1
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
), hamal_cte as (
    select  
        h.citizen_fid as fake_citizen_id
        , fid.citizen_id as citizen_id
        , file_name
        , is_dead
        , 1 as is_in_hamal_batch
        , is_left_the_city_permanent
        , is_answered_the_call
        , has_final_status
        , is_lonely
        , is_address_wrong
        , new_street_name
        , new_building_number
        , new_appartment_number
        , has_mamad
        , has_miklat_prati
        , has_miklat_ziburi
        , has_mobility_restriction
        , has_temporary_address
        , is_temporary_abroad
        , temporary_street_name
        , temporary_building_number
        , temporary_appartment
        , appearance_count
        , calcenter_case_number
        , is_final_status
    from core.hamal h
    LEFT JOIN core.fake_citizen_ids AS fid ON h.citizen_fid = fid.fake_citizen_id
    where 
        is_current = 1
)

INSERT INTO #citizens_work (
    fake_citizen_id,
    citizen_id,
    first_name,
    last_name,
    age,
    street_name,
    street_code,
    building_number,
    apartment_number,
    family_index_number
    , is_living_alone
    , is_elder_pair
    , has_phone,
    has_mobile_phone,
    is_welfare_patient,
    is_new_imigrant,
    has_breath_troubles,
    is_hazramim,
    phone1,
    phone2,
    phone3,
    is_in_hamal_batch,
    file_name_hamal,
    is_dead_hamal,
    is_left_the_city_permanent,
    is_answered_the_call,
    has_final_status,
    is_lonely,
    is_address_wrong,
    new_street_name,
    new_building_number,
    new_appartment_number,
    has_mamad,
    has_miklat_prati,
    has_miklat_ziburi,
    has_mobility_restriction,
    has_temporary_address,
    is_temporary_abroad,
    temporary_street_name,
    temporary_building_number,
    temporary_appartment,
    appearance_count,
    calcenter_case_number,
    is_final_status
)
SELECT
    fid.fake_citizen_id,
    b.citizen_id,
    b.first_name,
    b.last_name,
    b.age,
    b.street_name,
    b.street_code,
    b.building_number,
    b.apartment_number,
    b.family_index_number
    , b.is_living_alone
    , b.is_elder_pair
    /* phone flags */
    , CASE WHEN COUNT(p.phone_number) > 0 THEN 1 ELSE 0 END AS has_phone,
    CASE WHEN SUM(CASE WHEN p.type = 'mobile' THEN 1 ELSE 0 END) > 0
         THEN 1 ELSE 0 END as has_mobile_phone,
    /* flags */
    MAX(CASE WHEN COALESCE(w.citizen_id, 0) > 0 THEN 1 ELSE 0 END) AS is_welfare_patient,
    MAX(CASE WHEN COALESCE(ni.citizen_id, 0) > 0 THEN 1 ELSE 0 END) AS is_new_imigrant,
    MAX(CASE WHEN COALESCE(bt.citizen_id, 0) > 0 THEN 1 ELSE 0 END) AS has_breath_troubles,
    MAX(CASE WHEN COALESCE(h.citizen_id, 0) > 0 THEN 1 ELSE 0 END) AS is_hazramim,
    /* phones */
    MAX(CASE WHEN p.rn = 1 THEN p.phone_number END) AS phone1,
    MAX(CASE WHEN p.rn = 2 THEN p.phone_number END) AS phone2,
    MAX(CASE WHEN p.rn = 3 THEN p.phone_number END) AS phone3,
    /* hamal data */
    MAX(CASE WHEN COALESCE(hml.is_in_hamal_batch, 0) > 0 THEN 1 ELSE 0 END) AS is_in_hamal_batch,
    hml.file_name as file_name_hamal
    , COALESCE(hml.is_dead, 0) as is_dead
    , COALESCE(hml.is_left_the_city_permanent, 0) as is_left_the_city_permanent
    , COALESCE(hml.is_answered_the_call, 0) as is_answered_the_call
    , COALESCE(hml.has_final_status, 0) as has_final_status
    , COALESCE(hml.is_lonely, 0) as is_lonely
    , COALESCE(hml.is_address_wrong, 0) as is_address_wrong
    , hml.new_street_name
    , hml.new_building_number
    , hml.new_appartment_number
    , COALESCE(hml.has_mamad, 0) as has_mamad
    , COALESCE(hml.has_miklat_prati, 0) as has_miklat_prati
    , COALESCE(hml.has_miklat_ziburi, 0) as has_miklat_ziburi
    , COALESCE(hml.has_mobility_restriction, 0) as has_mobility_restriction
    , COALESCE(hml.has_temporary_address, 0) as has_temporary_address
    , COALESCE(hml.is_temporary_abroad, 0) as is_temporary_abroad
    , hml.temporary_street_name
    , hml.temporary_building_number
    , hml.temporary_appartment
    , hml.appearance_count
    , hml.calcenter_case_number
    , hml.is_final_status
FROM base as b
LEFT JOIN fake_ids AS fid ON b.citizen_id = fid.citizen_id
LEFT JOIN welfare_patients_cte AS w ON b.citizen_id = w.citizen_id
LEFT JOIN new_immigrants_cte AS ni ON b.citizen_id = ni.citizen_id
LEFT JOIN hazramim_cte AS h ON b.citizen_id = h.citizen_id
LEFT JOIN breath_troubles_cte AS bt ON b.citizen_id = bt.citizen_id
LEFT JOIN phones AS p ON b.citizen_id = p.citizen_id
LEFT JOIN hamal_cte AS hml ON b.citizen_id = hml.citizen_id
GROUP BY
    fid.fake_citizen_id, b.citizen_id, b.first_name, b.last_name, b.age,
    b.street_name, b.street_code, b.building_number,
    b.apartment_number, b.family_index_number, b.is_living_alone, b.is_elder_pair,
    w.is_welfare_patient, 
    hml.file_name, hml.is_dead, hml.is_left_the_city_permanent, hml.is_answered_the_call,
    hml.has_final_status, hml.is_lonely, hml.is_address_wrong, hml.new_street_name,
    hml.new_building_number, hml.new_appartment_number, hml.has_mamad, hml.has_miklat_prati,
    hml.has_miklat_ziburi, hml.has_mobility_restriction, hml.has_temporary_address,
    hml.is_temporary_abroad, hml.temporary_street_name, hml.temporary_building_number,
    hml.temporary_appartment, hml.appearance_count, hml.calcenter_case_number;


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