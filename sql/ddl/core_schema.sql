-- Idempotent DDL for core schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'core')
    EXEC('CREATE SCHEMA core');
GO
-- Example: citizen_core table (customize columns as needed)
CREATE TABLE IF NOT EXISTS core.citizen (
    id SERIAL PRIMARY KEY,
    business_key VARCHAR(255) NOT NULL,
    attribute1 VARCHAR(255),
    attribute2 VARCHAR(255),
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add more tables/views as required for the core layer below
-- ... 