---
id: TASK-2025-027
title: "Refactor DB Schema for Period-Aware Loading"
status: backlog
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-10
updated: 2025-07-10
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-database-schemas]
audit_log:

{date: 2025-07-10, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Update the database schema to support the new period-aware loading logic. This involves removing the now-redundant raw schema and modifying the stage schema.

## Acceptance Criteria
- An SQL migration script is created and applied that drops the raw schema and all its tables.
- The script adds a _data_period VARCHAR(7) column to every table in the stage schema.
- The script adds a database index on the _data_period column for each stage table to ensure efficient deletes. 