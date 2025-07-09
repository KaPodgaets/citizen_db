---
id: ARCH-pipeline-step-ingest
title: "Pipeline Step: Ingestion"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-09
tags: [python, ingest, etl, validation, yaml, mssql]
depends_on: [ARCH-database-schemas, ARCH-data-contract-yaml, ARCH-pipeline-utilities]
referenced_by: []
---
## Context
The Ingestion step is the primary quality gate and entry point for all source data. Its purpose is to validate, standardize, and load raw source files into the database, transforming them from an external format into the system's internal `raw` layer.

## Structure
This component is implemented in `ingest.py`. It relies on several utilities and contracts:
- `src/utils/parsing.py`: For handling date conversions and loading contracts.
- `src/utils/db.py`: For all database interactions.
- `contracts/*.yml`: Versioned YAML files for mapping source column names to target column names.
- `src/models/contracts.py`: Pydantic models for validating the structure of the YAML contract files.

## Behavior
The script performs a multi-stage process for each incoming Excel (`.xlsx`) file:
1.  **Filename Validation**: It enforces a strict naming convention (e.g., `citizens_2025-07_v-01.xlsx`), checking for format, snake_case, dataset name, date, and version.
2.  **Idempotency Check**: It calculates a SHA256 hash of the file and checks `meta.ingestion_log` to prevent re-processing.
3.  **Contract Loading**: It reads the corresponding YAML contract from the `contracts/` directory, selecting the correct version based on the date in the filename and validating the contract's structure with Pydantic.
4.  **Data Transformation**: It reads the Excel file into a pandas DataFrame, renames columns based on the loaded contract, and parses date columns from various formats (Excel numeric, strings) into a standard format.
5.  **Transactional Load**: It loads the processed DataFrame into the appropriate table in the `raw` database schema within a single database transaction. If the load fails, the transaction is rolled back.
6.  **Metadata Logging**: On success, it records the file details, hash, status, and contract version used into `meta.ingestion_log`.

## Evolution
### Historical
- v1: Initial design. Refactored from a simple file-copy mechanism to a full-fledged, database-centric ELT step. 