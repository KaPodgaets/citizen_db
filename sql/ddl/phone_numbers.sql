-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'core')
    EXEC('CREATE SCHEMA core');
GO

-- Citizens stage table: types match validated/cleaned data
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'phone_numbers' AND schema_id = SCHEMA_ID('core'))
BEGIN
    CREATE TABLE core.phone_numbers (
        phone_id INT IDENTITY(1,1) PRIMARY KEY,
        citizen_id INT NOT NULL,
        phone_number NVARCHAR(20) NOT NULL,
        type NVARCHAR(20) NOT NULL,
        dataset_name NVARCHAR(50) NOT NULL,
    );
END
GO