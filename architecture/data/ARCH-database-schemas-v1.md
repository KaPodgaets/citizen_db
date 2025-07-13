---
id: ARCH-database-schemas
title: "Database Schemas (MS SQL)"
type: data_model
layer: infrastructure
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-13
tags: [sql, ddl, mssql, data-model, metadata]
depends_on: []
referenced_by: []
---
## Context
This component defines the entire database structure within MS SQL Server, which is the backbone for both data storage and pipeline control. The schemas are separated by function into a multi-layered data architecture.

## Structure
The database definitions are managed as version-controlled, idempotent DDL scripts located in sql/ddl/. There are scripts for each of the schemas:

meta: Defines tables for auditing and pipeline control (`etl_audit`, `ingestion_log`, `validation_log`, `dataset_version`). This schema enables idempotency, operational monitoring, and data versioning. It will be enhanced with tables for `stage_load_log` and `transform_log` to support more granular, resilient orchestration.
- stage: Holds data that has been validated and loaded from Parquet files. Data in this layer is cleaned, correctly typed, and ready for transformation. All tables in this schema include an indexed `_data_period` column and a `_source_parquet_path` column to support idempotent, period-level reloads and enhance traceability.
core: The historized, normalized data layer. These tables implement Slowly Changing Dimension (SCD) Type 2 patterns to track changes over time. **Note: This SCD-2 model is being deprecated in favor of a simpler, versioned model described in `ARCH-data-model-core-v2.md`.**
mart: The denormalized analytics layer, typically in a star schema optimized for BI tools.

## Behavior
The DDL scripts are designed to be run to set up or update the database. The Python application interacts with the tables defined by these scripts but does not have permissions to alter the schemas themselves, ensuring a clean separation of concerns and enhancing security.

## Evolution
### Historical
- v1: Initial design.
- **2025-07-13**: Added `meta.stage_load_log` and `meta.transform_log` for enhanced auditing and resilient orchestration. Added `_source_parquet_path` to stage tables for traceability.
- **2025-07-10**: The `raw` schema was removed in favor of a file-based staging approach using Parquet. The `stage` schema is now loaded from these Parquet files and all its tables have been modified to include an indexed `_data_period` column. 