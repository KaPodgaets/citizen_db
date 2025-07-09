-- Idempotent DDL for meta schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'meta')
    EXEC('CREATE SCHEMA meta');
GO

-- etl_audit table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'etl_audit' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    CREATE TABLE meta.etl_audit (
        id INT IDENTITY PRIMARY KEY,
        event_time DATETIME2 DEFAULT SYSDATETIME(),
        step NVARCHAR(100),
        status NVARCHAR(20),
        message NVARCHAR(MAX)
    );
END
GO

-- ingestion_log table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ingestion_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    CREATE TABLE meta.ingestion_log (
        id INT IDENTITY PRIMARY KEY,
        file_name NVARCHAR(255),
        file_hash CHAR(64),
        ingest_time DATETIME2 DEFAULT SYSDATETIME(),
        status NVARCHAR(20)
    );
END
GO

-- validation_log table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'validation_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    CREATE TABLE meta.validation_log (
        id INT IDENTITY PRIMARY KEY,
        file_id INT,
        validation_time DATETIME2 DEFAULT SYSDATETIME(),
        status NVARCHAR(20),
        error_report NVARCHAR(MAX)
    );
END
GO

-- dataset_version table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'dataset_version' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    CREATE TABLE meta.dataset_version (
        id INT IDENTITY PRIMARY KEY,
        dataset_name NVARCHAR(255),
        version_number INT,
        created_at DATETIME2 DEFAULT SYSDATETIME(),
        description NVARCHAR(255),
        is_active BIT DEFAULT 1
    );
END
GO 