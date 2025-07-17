-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stage')
    EXEC('CREATE SCHEMA stage');
GO

-- Citizens stage table: types match validated/cleaned data
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'av_bait' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    CREATE TABLE stage.av_bait (
        citizen_id INT NOT NULL,
        first_name NVARCHAR(255) NULL,
        last_name NVARCHAR(255) NOT NULL,
        age INT NOT NULL,
        street_name NVARCHAR(255) NULL,
        street_code NVARCHAR(50) NULL,
        building_number NVARCHAR(20) NULL,
        apartment_number NVARCHAR(20) NULL,
        family_index_number INT NOT NULL,
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
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'av_bait' AND schema_id = SCHEMA_ID('core'))
BEGIN
    CREATE TABLE core.av_bait (
        citizen_id INT NOT NULL,
        first_name NVARCHAR(255) NULL,
        last_name NVARCHAR(255) NOT NULL,
        age INT NOT NULL,
        street_name NVARCHAR(255) NULL,
        street_code NVARCHAR(50) NULL,
        building_number NVARCHAR(20) NULL,
        apartment_number NVARCHAR(20) NULL,
        family_index_number INT NOT NULL,
        is_living_alone BIT NOT NULL,
        is_elder_pair BIT NOT NULL,
        is_current INT NOT NULL
    );
END
GO