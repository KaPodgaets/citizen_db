---
id: ARCH-data-contract-yaml
title: "Data Contracts (YAML Column Mapping)"
type: data_model
layer: domain
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-10
tags: [yaml, schema, validation, contract]
depends_on: [ARCH-data-contract-validation-pydantic]
referenced_by: []
---
## Context
This component provides the mechanism for mapping column names from source Excel files (often in Hebrew) to the standardized English column names used within the database. This mapping is versioned to handle changes in source file layouts over time. It is the first transformation applied during the ingestion process.

## Structure
The contracts are stored in the `contracts/` directory. There is one YAML file per dataset (e.g., `contracts/citizens.yml`).

Each file contains a list of all historical versions for that dataset. The structure is validated by a Pydantic model (`ARCH-data-contract-validation-pydantic`).

Example (`contracts/citizens.yml`):
```yaml
'2024-01-01':
  'תעודת זהות': citizen_id
  'שם פרטי': first_name
  'שם משפחה': last_name
  # ... etc
```

## Behavior
These contracts are used in the early stages of the pipeline:
- ingest.py: Uses the keys of the column_mapping dictionary as the list of required headers for its initial header validation step.
- validate.py: After a file has been ingested, this script reads the appropriate YAML file for the dataset. It determines the correct column_mapping to use based on the file's period and renames the DataFrame columns before validating the data with Pandera.

## Evolution
### Historical
- v1: Initial design.
  - 2025-07-10: Role clarified. The contracts are now used for header validation in the ingest step and for column renaming in the validate step. 