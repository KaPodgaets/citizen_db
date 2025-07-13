---
id: ARCH-data-model-core
title: "Data Model: Core Schema (v2 - Versioned)"
type: data_model
layer: infrastructure
owner: "@team-data"
version: v2
status: planned
created: 2025-07-13
updated: 2025-07-13
tags: [sql, ddl, mssql, data-model, metadata, lineage]
depends_on: [ARCH-database-schemas]
referenced_by: []
---
## Context
This document describes the planned v2 data model for the `core` schema, which replaces the previous SCD-2 implementation. The new model simplifies the schema and enhances data lineage by explicitly linking every data row to a specific load event via a versioning table.

## Structure
The data model change affects all tables in the `core` schema and relies on the `meta.dataset_version` table.

### `meta.dataset_version` Table
This table is central to the new design.
- `id` (PK, INT, IDENTITY)
- `dataset_name` (VARCHAR)
- `period` (VARCHAR)
- `load_timestamp` (DATETIME)
- ... (other potential metadata)

### `core.*` Tables
All tables in the `core` schema will be modified as follows:

**Columns to be ADDED:**
- `dataset_version_id` (INTEGER, NOT NULL, FK to `meta.dataset_version.id`): Links every row to a specific load batch.

**Columns to be REMOVED:**
- `is_current`
- `valid_from`
- `valid_to`
- `version_number`
- Any other columns related to the SCD-2 implementation.

## Behavior
With this model, updating data for a specific period (e.g., '2025-07') becomes a simple, atomic "delete and replace" operation. Instead of managing complex start/end dates, the old data is identified by its `dataset_version_id` and deleted, while new data is inserted with a new `dataset_version_id`. This makes the data loading process idempotent and much easier to reason about.

## Evolution
### Planned
- v2: This model is planned to replace the v1 SCD-2 model. 