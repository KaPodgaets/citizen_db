-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stage')
    EXEC('CREATE SCHEMA stage');
GO

-- Citizens stage table: types match validated/cleaned data
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'hamal' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    CREATE TABLE stage.hamal (
        citizen_fid INT NOT NULL,
        file_name NVARCHAR(100) NOT NULL,
        is_answered_the_call  BIT NOT NULL,
        is_lonely BIT NOT NULL,
        is_address_wrong BIT NOT NULL,
        new_street_name NVARCHAR(100) NULL,
        new_building_number NVARCHAR(10) NULL,
        new_appartment_number NVARCHAR(10) NULL,
        has_mamad BIT NOT NULL,
        has_miklat_prati BIT NOT NULL,
        has_miklat_ziburi BIT NOT NULL,
        has_mobility_restriction BIT NOT NULL,
        is_dead BIT NOT NULL,
        is_left_the_city_permanent BIT NOT NULL,
        has_temporary_address BIT NOT NULL,
        is_temporary_abroad BIT NOT NULL,
        temporary_street_name NVARCHAR(100) NULL,
        temporary_building_number NVARCHAR(10) NULL,
        temporary_appartment NVARCHAR(10) NULL,
        appearance_count INT NULL,
        calcenter_case_number NVARCHAR(10) NULL,
        is_final_status BIT NOT NULL,
        is_actual_hamal_batch BIT NOT NULL,
        _data_period NVARCHAR(7) NOT NULL,
        _source_parquet_path NVARCHAR(1024) NOT NULL
    );
END
GO


-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'core')
    EXEC('CREATE SCHEMA core');
GO


-- av_bait core table: types match validated/cleaned data
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'hamal' AND schema_id = SCHEMA_ID('core'))
BEGIN
    CREATE TABLE core.hamal (
        citizen_fid INT NOT NULL,
        file_name NVARCHAR(100) NOT NULL,
        is_answered_the_call  BIT NOT NULL,
        is_lonely BIT NOT NULL,
        is_address_wrong BIT NOT NULL,
        new_street_name NVARCHAR(100) NULL,
        new_building_number NVARCHAR(10) NULL,
        new_appartment_number NVARCHAR(10) NULL,
        has_mamad BIT NOT NULL,
        has_miklat_prati BIT NOT NULL,
        has_miklat_ziburi BIT NOT NULL,
        has_mobility_restriction BIT NOT NULL,
        is_dead BIT NOT NULL,
        is_left_the_city_permanent BIT NOT NULL,
        has_temporary_address BIT NOT NULL,
        is_temporary_abroad BIT NOT NULL,
        temporary_street_name NVARCHAR(100) NULL,
        temporary_building_number NVARCHAR(10) NULL,
        temporary_appartment NVARCHAR(10) NULL,
        appearance_count INT NULL,
        calcenter_case_number NVARCHAR(10) NULL,
        is_final_status BIT NOT NULL,
        is_current INT NOT NULL,
        is_actual_hamal_batch BIT NOT NULL
    );
END
GO


