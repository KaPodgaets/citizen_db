---
id: TASK-2025-028
title: "Task 1.1: Augment DB Schema for Auditing and Traceability (v2)"
status: backlog
priority: high
type: feature
estimate: L
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-027]
children: []
arch_refs: [ARCH-database-schemas]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
To support the enhanced pipeline logic, the database schema must be updated for better auditing and traceability. This involves creating new log tables and adding metadata columns to existing stage tables.

## Acceptance Criteria
- A new idempotent SQL script (`sql/ddl/schema_updates_v2.sql`) is created.
- The script successfully creates the `meta.stage_load_log` table with columns: `id`, `validation_log_id`, `status`, `load_timestamp`, `error_message`.
- The script successfully creates the `meta.transform_log` table with columns: `id`, `dataset_name`, `period`, `status`, `retry_count`, `last_attempt_timestamp`, `error_message`.
- The script successfully alters all tables in the `stage` schema to add `_source_parquet_path` (VARCHAR) and `_data_period` (VARCHAR) columns.
- An index is added to the `_data_period` column on all stage tables to ensure efficient delete operations. 