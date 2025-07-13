---
id: TASK-2025-038
title: "Phase 3: Update Core and Meta Table DDLs for Rebuild Strategy"
status: done
priority: medium
type: feature
estimate: M
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-data-model-core]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-13, user: "@AI-Roboticist", action: "marked as done"}
---
## Description
Align the database schema with the new metadata-driven loading strategy by updating the DDL scripts.

## Acceptance Criteria
- DDL scripts are updated.
- All tables in the `core` schema are altered to remove SCD-2 columns (`is_current`, `valid_from`, `valid_to`, etc.).
- A non-nullable `dataset_version_id` (INTEGER, Foreign Key to `meta.dataset_version.id`) column is added to every `core` table.
- The `meta.dataset_version` table is confirmed to have the necessary columns (`id`, `dataset_name`, `period`, `load_timestamp`). 