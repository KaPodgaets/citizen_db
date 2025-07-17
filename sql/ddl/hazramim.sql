-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stage')
    EXEC('CREATE SCHEMA stage');
GO

-- Citizens stage table: types match validated/cleaned data
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'hazramim' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    CREATE TABLE stage.hazramim (
        citizen_id INT NOT NULL,
        phone_number NVARCHAR(200) NULL,
        phone_number_contact_person NVARCHAR(200) NULL,
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
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'hazramim' AND schema_id = SCHEMA_ID('core'))
BEGIN
    CREATE TABLE core.hazramim (
        citizen_id INT NOT NULL,
        is_current INT NOT NULL
    );
END
GO