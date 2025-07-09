-- mart_schema.sql: Idempotent DDL for the analytics-ready mart layer

-- Example: citizen_mart_fact table (customize columns as needed)
CREATE TABLE IF NOT EXISTS citizen_mart_fact (
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