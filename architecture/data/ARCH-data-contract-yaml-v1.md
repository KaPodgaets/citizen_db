---
id: ARCH-data-contract-yaml
title: "Data Contracts (YAML Column Mapping)"
type: data_model
layer: domain
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-09
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
- version: '2024-01-01'
  column_mapping:
    'תעודת זהות': 'citizen_id'
    # ... etc
```

## Behavior
The `ingest.py` script, via the `src/utils/parsing.py` utility, reads the appropriate YAML file for the dataset being processed. It determines the correct `column_mapping` to use by finding the latest version in the file whose date is on or before the date specified in the source filename. This mapping dictionary is then used to rename the columns of the pandas DataFrame before it's loaded into the `raw` database layer.

## Evolution
### Historical
- v1: Initial design. 