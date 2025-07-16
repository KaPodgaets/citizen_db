-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'mart')
    EXEC('CREATE SCHEMA mart');
GO

-- Citizens mart table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'citizens' AND schema_id = SCHEMA_ID('mart'))
BEGIN
CREATE TABLE mart.citizens (
    fake_citizen_id BIGINT NOT NULL,
    citizen_id INT NOT NULL,
    first_name NVARCHAR(255) NULL,
    last_name NVARCHAR(255) NOT NULL,
    age INT NOT NULL,
    street_name NVARCHAR(255) NULL,
    street_code NVARCHAR(50) NULL,
    building_number NVARCHAR(20) NULL,
    apartment_number NVARCHAR(20) NULL,
    family_index_number INT NOT NULL,
    has_phone BIT NOT NULL,
    has_mobile_phone BIT NOT NULL,
    is_welfare_patient BIT NOT NULL,
    is_new_imigrant BIT NOT NULL,
    has_breath_troubles BIT NOT NULL,
    is_hazramim BIT NOT NULL,
    /* from table phones */
    phone1 NVARCHAR(20) NULL,
    phone2 NVARCHAR(20) NULL,
    phone3 NVARCHAR(20) NULL,
    /* hamal data */
    is_in_hamal_batch BIT NOT NULL,
    file_name_hamal NVARCHAR(255) NULL,
    is_dead_hamal BIT NULL,
    is_left_the_city_permanent BIT NOT NULL,
    is_answered_the_call  BIT NOT NULL,
    has_final_status BIT NOT NULL,
    is_lonely BIT NOT NULL,
    is_address_wrong BIT NOT NULL,
    new_street_name NVARCHAR(100) NULL,
    new_building_number NVARCHAR(10) NULL,
    new_appartment_number NVARCHAR(10) NULL,
    has_mamad BIT NOT NULL,
    has_miklat_prati BIT NOT NULL,
    has_miklat_ziburi BIT NOT NULL,
    has_mobility_restriction BIT NOT NULL,
    has_temporary_address BIT NOT NULL,
    is_temporary_abroad BIT NOT NULL,
    temporary_street_name NVARCHAR(100) NULL,
    temporary_building_number NVARCHAR(10) NULL,
    temporary_appartment NVARCHAR(10) NULL,
    appearance_count INT NULL,
    calcenter_case_number NVARCHAR(10) NULL
)
END
GO



        
    
        