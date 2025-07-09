---
id: ARCH-pipeline-step-validate
title: "Pipeline Step: Validation"
type: component
layer: application
owner: "@team-data"
version: v1
status: planned
created: 2025-07-09
updated: 2025-07-09
tags: [python, validation, pandera, etl, data-quality]
depends_on: [ARCH-database-schemas, ARCH-data-contract-pandera]
referenced_by: []
---
## Context
The Validation step acts as a crucial quality gate, ensuring that no malformed or invalid data proceeds to the transformation stage. It checks landed data against predefined data contracts.

## Structure
This component consists of the `validate.py` script and the Pandera schema definitions it uses, located in the `schemas/` directory.

## Behavior
The script takes a `file_id` corresponding to a record in `meta.ingestion_log`. It reads the raw file from `data/land/` and validates its structure and content against the appropriate Pandera schema. The results of the validation (success or failure, with error details) are logged to the `meta.validation_log` table. If validation is successful, the script writes a clean, standardized dataset as a Parquet file to the `data/stage/clean/` directory, ready for transformation.

## Evolution
### Planned
- Initial implementation as described.

### Historical
- v1: Initial design. 