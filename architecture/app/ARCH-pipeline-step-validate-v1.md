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
depends_on: [ARCH-database-schemas, ARCH-data-contract-pandera, ARCH-data-contract-yaml]
referenced_by: []
---
## Context
The Validation step acts as a crucial data quality gate after initial ingestion, ensuring that no structurally or content-invalid data proceeds to the core transformation stage. It checks data that has been loaded into the `raw` layer against formal data contracts.

## Structure
This component consists of the `validate.py` script and the Pandera schema definitions it uses, located in the `schemas/` directory.

## Behavior
The script takes a `file_id` corresponding to a record in `meta.ingestion_log`. It reads the corresponding data from the appropriate `raw` schema table. It then validates this data against the appropriate Pandera schema defined in the `schemas/` directory. The results of the validation (success or failure, with error details) are logged to the `meta.validation_log` table. If validation is successful, the script bulk-loads the clean, validated, and correctly-typed data into the corresponding `stage` schema table, ready for transformation.

### Historical
- v1: Initial design. 