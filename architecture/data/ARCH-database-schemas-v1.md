---
id: ARCH-database-schemas
title: "Database Schemas (MS SQL)"
type: data_model
layer: infrastructure
owner: "@team-data"
version: v1
status: planned
created: 2025-07-09
updated: 2025-07-09
tags: [sql, ddl, mssql, data-model, metadata]
depends_on: []
referenced_by: []
---
## Context
This component defines the entire database structure within MS SQL Server, which is the backbone for both data storage and pipeline control. The schemas are separated by function into a four-layer data architecture.

## Structure
The database definitions are managed as version-controlled, idempotent DDL scripts located in `sql/ddl/`. There are scripts for each of the core schemas:
- **`meta_schema.sql`**: Defines tables for auditing and pipeline control. This schema enables idempotency, operational monitoring, and data versioning. Key tables include:
  - `etl_audit`: General log for all pipeline events and errors.
  - `ingestion_log`: Tracks each raw file landed, its hash, and ingestion time to prevent duplicates.
  - `validation_log`: Stores the PASS/FAIL status and detailed error reports for each file validation attempt.
  - `dataset_version`: Manages versions of processed datasets, enabling rollback and time-travel queries.
- **`core_schema.sql`**: Defines tables for the historized, normalized data layer. These tables will implement Slowly Changing Dimension (SCD) Type 2 patterns to track changes over time.
- **`mart_schema.sql`**: Defines the denormalized tables and views for the analytics layer, typically in a star schema optimized for BI tools.

## Behavior
The DDL scripts are designed to be run to set up or update the database. The Python application interacts with the tables defined by these scripts but does not have permissions to alter the schemas themselves, ensuring a clean separation of concerns and enhancing security.

## Evolution
### Planned
- Initial creation of DDL scripts for all three schemas.

### Historical
- v1: Initial design. 