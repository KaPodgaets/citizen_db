-- Idempotent DDL for mart schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'mart')
    EXEC('CREATE SCHEMA mart');
GO
-- Example: citizen_mart_fact table (customize columns as needed)
CREATE TABLE IF NOT EXISTS mart.citizen_fact (
    id SERIAL PRIMARY KEY,
    business_key VARCHAR(255) NOT NULL,
    attribute1 VARCHAR(255),
    attribute2 VARCHAR(255),
    snapshot_date DATE NOT NULL,
    metric1 NUMERIC,
    metric2 NUMERIC
);

-- Add more fact/dimension tables or views as required for the mart layer below
-- ... 