-- core_schema.sql: Idempotent DDL for the historized core layer (SCD-2)

-- Example: citizen_core table (customize columns as needed)
CREATE TABLE IF NOT EXISTS citizen_core (
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