-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stage')
    EXEC('CREATE SCHEMA stage');
GO

-- Citizens stage table: types match validated/cleaned data
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'welfare_patients' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    CREATE TABLE stage.welfare_patients (
        head_family_citizen_id INT NOT NULL,
        citizen_id INT NOT NULL,
        street_name NVARCHAR(255) NULL,
        street_code NVARCHAR(50) NULL,
        building_number NVARCHAR(20) NULL,
        apartment_number NVARCHAR(20) NULL,
        mobile_phone_number NVARCHAR(20) NULL,
        home_phone_number NVARCHAR(20) NULL,
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
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'welfare_patients' AND schema_id = SCHEMA_ID('core'))
BEGIN
    CREATE TABLE core.welfare_patients (
        head_family_citizen_id INT NOT NULL,
        citizen_id INT NOT NULL,
        street_name NVARCHAR(255) NULL,
        street_code NVARCHAR(50) NULL,
        building_number NVARCHAR(20) NULL,
        apartment_number NVARCHAR(20) NULL,
        mobile_phone_number NVARCHAR(20) NULL,
        home_phone_number NVARCHAR(20) NULL,
        is_current INT NOT NULL
    );
END
GO