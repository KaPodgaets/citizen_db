---
id: ARCH-data-contract-validation-pydantic
title: "Data Contract Structural Validation (Pydantic)"
type: data_model
layer: domain
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-09
tags: [pydantic, schema, validation, data-quality, contract, yaml]
depends_on: []
referenced_by: []
---
## Context
To ensure the reliability and maintainability of the versioned YAML contracts (`ARCH-data-contract-yaml`), their structure must be formally defined and validated. This component uses Pydantic models to serve as the schema for the contract files themselves, preventing runtime errors due to typos or structural mistakes in the contracts.

## Structure
This component is implemented as a set of Pydantic `BaseModel` classes in `src/models/contracts.py`.
- `ContractVersion`: Defines the schema for a single version entry, requiring a `version` string (YYYY-MM-DD) and a `column_mapping` dictionary.
- `ContractFile`: Defines the top-level structure of the YAML file, requiring a `versions` key that holds a list of `ContractVersion` objects.

## Behavior
The `src/utils/parsing.py` utility imports these models. When a YAML contract file is loaded, its content is parsed into the corresponding Pydantic model. Pydantic automatically validates that the data conforms to the defined schema (correct keys, types, and formats). If validation fails, a `ValidationError` is raised, which is caught by the `ingest.py` script to provide a clear error message to the user.

## Evolution
### Historical
- v1: Initial design. 