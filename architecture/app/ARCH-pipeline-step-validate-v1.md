---
id: ARCH-pipeline-step-validate
title: "Pipeline Step: Validation"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-10
tags: [python, validation, pandera, etl, data-quality, parquet, file-system]
depends_on: [ARCH-database-schemas, ARCH-data-contract-pandera, ARCH-data-contract-yaml]
referenced_by: []
---
## Context
The Validation step is a crucial quality gate that transforms raw source files into clean, typed, and validated Parquet files. This step ensures that no structurally or content-invalid data proceeds to the database loading stage. It combines column mapping with data type and content validation.

## Structure
This component consists of the `validate.py` script. It uses Pandera schema definitions from the `schemas/` directory and YAML column mapping contracts from the `contracts/` directory.

## Behavior
The script is triggered with a `file_id` corresponding to a record in `meta.ingestion_log`.
1.  It reads the raw source file (e.g., `.xlsx`) from the `data/landed/` directory.
2.  It applies column renaming based on the appropriate versioned YAML contract.
3.  It validates the resulting DataFrame's data types and content against the relevant Pandera schema.
4.  On success, it saves the clean, validated DataFrame as a Parquet file in the `data/stage/cleaned/` directory.
5.  The result of the validation (pass or fail with error details) and the path to the output Parquet file (on success) are logged to the `meta.validation_log` table.

## Evolution
### Historical
- v1: Initial design. 
  - **2025-07-10**: Major refactoring. Changed from reading from a `raw` DB schema to reading from source files in `data/landed/` and writing to Parquet files. Now responsible for column mapping as well as Pandera validation. 