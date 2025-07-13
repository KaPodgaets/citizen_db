-- Idempotent DDL for mart schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'mart')
    EXEC('CREATE SCHEMA mart');
GO
-- Example: citizen_mart_fact table (customize columns as needed)
CREATE TABLE IF NOT EXISTS mart.citizen (
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
    phone1 NVARCHAR(20) NULL,
    phone2 NVARCHAR(20) NULL,
    phone3 NVARCHAR(20) NULL
);