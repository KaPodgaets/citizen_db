---
id: TASK-2025-020
title: "Task 0.6: Modify stage Schema and Remove raw Schema"
status: done
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-09
updated: 2025-07-10
parents: [TASK-2025-001]
children: []
arch_refs: [ARCH-database-schemas]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-Assistant", action: "marked done after implementing raw and stage DDL scripts"}
  - {date: 2025-07-10, user: "@AI-DocArchitect", action: "Task updated to reflect removal of raw schema and modification of stage schema."}
---
## Description
Refactor the database schemas to support the new file-based staging architecture. This involves removing the raw schema and modifying the stage schema to support period-aware loading.

## Acceptance Criteria
The raw schema and all its associated tables are dropped from the database. All tables in the stage schema are modified to include a _data_period VARCHAR(7) column, with a database index on this column. DDL scripts are updated to reflect these changes. 