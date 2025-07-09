-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stage')
    EXEC('CREATE SCHEMA stage');
GO

-- Citizens stage table: types match validated/cleaned data
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'citizens' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    CREATE TABLE stage.citizens (
        citizen_id INT NOT NULL,
        first_name NVARCHAR(255) NOT NULL,
        last_name NVARCHAR(255) NOT NULL,
        birth_date DATETIME NULL,
        street_name NVARCHAR(255) NULL,
        street_code NVARCHAR(50) NULL,
        building_number NVARCHAR(20) NULL,
        apartment_number NVARCHAR(20) NULL
    );
END
GO

-- Add more stage tables for other datasets as needed

