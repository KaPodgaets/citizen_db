-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stage')
    EXEC('CREATE SCHEMA stage');
GO

-- Citizens stage table: types match validated/cleaned data
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'new_immigrants' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    CREATE TABLE stage.new_immigrants (
        citizen_id INT NOT NULL,
        citizen_phone_number_1 NVARCHAR(200) NULL,
        citizen_phone_number_2 NVARCHAR(200) NULL,
        is_left_the_city NVARCHAR(200) NULL,
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
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'new_immigrants' AND schema_id = SCHEMA_ID('core'))
BEGIN
    CREATE TABLE core.new_immigrants (
        citizen_id INT PRIMARY KEY,
        is_current INT NOT NULL
    );
END
GO