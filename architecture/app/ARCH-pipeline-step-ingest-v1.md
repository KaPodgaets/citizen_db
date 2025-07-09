---
id: ARCH-pipeline-step-ingest
title: "Pipeline Step: Ingestion"
type: component
layer: application
owner: "@team-data"
version: v1
status: planned
created: 2025-07-09
updated: 2025-07-09
tags: [python, ingest, etl]
depends_on: [ARCH-database-schemas]
referenced_by: []
---
## Context
The Ingestion step is the first active stage of the pipeline. Its purpose is to securely land raw source files into the system's controlled environment and register them for further processing, ensuring that each file is processed exactly once.

## Structure
This component is implemented as a single-responsibility script: `ingest.py`.

## Behavior
The script processes new Excel files from a designated input location. For each file, it calculates a SHA256 hash. It checks the `meta.ingestion_log` table to see if a file with the same hash has already been processed. If the hash is new, the script copies the file to the `data/land/` directory and inserts a new record into the log table with the file's metadata and hash. This check for hash uniqueness makes the ingestion process idempotent.

## Evolution
### Planned
- Initial implementation as described.

### Historical
- v1: Initial design. 