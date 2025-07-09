-- Idempotent DDL for raw schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'raw')
    EXEC('CREATE SCHEMA raw');
GO

-- Citizens raw table: all columns as NVARCHAR(MAX) for resilience
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'citizens' AND schema_id = SCHEMA_ID('raw'))
BEGIN
    CREATE TABLE raw.citizens (
        citizen_id NVARCHAR(MAX) NOT NULL,
        first_name NVARCHAR(MAX) NOT NULL,
        last_name NVARCHAR(MAX) NOT NULL,
        birth_date NVARCHAR(MAX) NULL,
        street_name NVARCHAR(MAX) NULL,
        street_code NVARCHAR(MAX) NULL,
        building_number NVARCHAR(MAX) NULL,
        apartment_number NVARCHAR(MAX) NULL
    );
END
GO

-- Add more raw tables for other datasets as needed