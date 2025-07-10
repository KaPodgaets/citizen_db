---
id: ARCH-pipeline-step-ingest
title: "Pipeline Step: Ingestion"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-10
tags: [python, ingest, etl, validation, yaml, file-system]
depends_on: [ARCH-database-schemas, ARCH-data-contract-yaml, ARCH-pipeline-utilities]
referenced_by: []
---
## Context
The Ingestion step is the primary quality gate and entry point for all source data. It validates a source file's metadata (filename, headers) in-place and registers it in the system for downstream processing. It ensures that only files conforming to basic structural and naming conventions are allowed into the pipeline.

## Structure
This component is implemented in `ingest.py`. It operates on files located in the `data/landed/` directory and relies on several utilities and contracts:
- `datasets_config.yml`: A root configuration file defining known datasets and their properties.
- `src/utils/parsing.py`: For parsing filenames and validating headers.
- `src/utils/db.py`: For all database interactions.
- `contracts/*.yml`: Versioned YAML files for mapping source column names to target column names.

## Behavior
The script performs a multi-stage validation process for a source file located in `data/landed/`:
1.  **Filename Parsing & Validation**: It parses the filename (e.g., `citizens_2025-07_v-01.xlsx`) into dataset, period, version, and extension. It validates these components against rules defined in `datasets_config.yml`.
2.  **Header Validation**: It reads only the headers from the source file and validates that all required columns (as defined by the keys in the relevant YAML contract) are present.
3.  **Idempotency Check**: It calculates a SHA256 hash of the file and checks `meta.ingestion_log` to prevent re-processing the same file content.
4.  **No File Movement**: The script does *not* copy or move the source file. It remains in `data/landed/`.
5.  **Metadata Logging**: On success, it records the file details, hash, and parsed metadata (dataset, period, version) into `meta.ingestion_log` with a status indicating it's ready for the next step (validation).

## Evolution
### Historical
- v1: Initial design. Refactored from a simple file-copy mechanism to a full-fledged, database-centric ELT step. 
  - **2025-07-10**: Major refactoring. Removed database loading responsibility. Role changed to in-place validator of filename and headers, preparing for a file-based staging (Parquet) workflow. 