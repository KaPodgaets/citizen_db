---
id: ARCH-pipeline-step-transform
title: "Pipeline Step: Transform (v2 - Metadata-Driven Rebuild)"
type: component
layer: application
owner: "@team-data"
version: v2
status: planned
created: 2025-07-13
updated: 2025-07-13
tags: [python, transform, etl, metadata, modular]
depends_on: [ARCH-database-schemas, ARCH-data-model-core, ARCH-pipeline-utilities, ARCH-pipeline-orchestration]
referenced_by: []
---
## Context
This component represents a significant refactoring of the transformation step. It moves away from a monolithic script and complex SCD-2 logic towards a modular, configuration-driven, and idempotent design. The goal is to simplify maintenance, improve flexibility, and enhance data lineage.

## Structure
- **`src/transformations/scripts/`**: A new directory containing dataset-specific transformation scripts (e.g., `transform_av_bait.py`).
- **`datasets_config.yml`**: This configuration file will be extended with a `transform_script` key for each dataset, pointing to its specific script.
- **`src/transform.py`**: The original monolithic script will be deprecated and eventually removed.
- **`meta.dataset_version`**: A metadata table that tracks each load as a distinct version for a given dataset and period.
- **`core.*` tables**: Core tables will no longer contain SCD-2 columns. Instead, they will have a `dataset_version_id` foreign key linking each row to a specific load event in `meta.dataset_version`.

## Behavior
The transformation process for a given dataset and period will be executed by its dedicated script, triggered by the orchestrator. The script will perform the following steps within a single database transaction:
1.  **Create New Version**: A new record is created in `meta.dataset_version` for the current dataset and period, returning a unique `dataset_version_id`.
2.  **Find Old Versions**: The script identifies any previous `dataset_version_id`s for the same dataset and period.
3.  **Delete Old Data**: If old versions exist, all corresponding data is deleted from the target `core` table using the old `dataset_version_id`s.
4.  **Insert New Data**: Data is read from the `stage` table for the given period, enriched with the new `dataset_version_id`, and bulk-inserted into the `core` table.

This "rebuild from zero" approach for each period simplifies logic and makes the process idempotent and easier to debug.

## Evolution
### Planned
- v2: Initial planned design. This architecture will replace the v1 SCD-2 implementation. 