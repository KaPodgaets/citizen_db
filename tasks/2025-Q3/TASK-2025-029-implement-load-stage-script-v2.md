---
id: TASK-2025-029
title: "Task 1.2: Implement load_stage.py Script (v2)"
status: done
priority: high
type: feature
estimate: L
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-027]
children: []
arch_refs: [ARCH-pipeline-step-load-stage]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-13, user: "@AI-Roboticist", action: "marked as done"}
---
## Description
Create the `load_stage.py` script, the component responsible for moving validated data from Parquet files into the database staging area. The script must be transactional and idempotent at the data-period level.

## Acceptance Criteria
- The `src/load_stage.py` script is created and accepts a `--validation-log-id` argument.
- It retrieves file path, period, and dataset info from the meta tables using the provided ID.
- It adds `_data_period` and `_source_parquet_path` columns to the DataFrame before loading.
- It performs a transactional "delete-then-append" operation into the correct `stage` table for the given period.
- On success or failure, it inserts a corresponding record into `meta.stage_load_log`. 