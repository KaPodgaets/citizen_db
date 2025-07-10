---
id: TASK-2025-025
title: "Implement Period-Aware Stage DB Loading"
status: backlog
priority: high
type: feature
estimate: L
assignee:
created: 2025-07-10
updated: 2025-07-10
parents: [TASK-2025-002]
children: []
arch_refs: [ARCH-pipeline-step-load-stage, ARCH-database-schemas]
audit_log:

{date: 2025-07-10, user: "@AI-DocArchitect", action: "created with status done"}
---
## Description
Implement the load_stage.py script, which is responsible for loading data from validated Parquet files into the database stage tables. This script contains the critical business logic for ensuring that data loads are idempotent at the period level.

## Acceptance Criteria
A new script src/load_stage.py is created. It takes a Parquet file path, a period (e.g., '2025-06'), and a dataset name as input. Within a single database transaction, it first deletes all existing rows for that period from the target stage table, then appends the new data from the Parquet file. The entire operation is atomic; a failure will result in a rollback, leaving the database unchanged. A _data_period column is added to the DataFrame before loading.

## Definition of Done
The script is implemented, unit and integration tests are written to verify the transactional logic, and the script is integrated into the pipeline orchestration. 