---
id: TASK-2025-020
title: "Task 0.6: Implement SQL DDL for raw and stage Schemas"
status: done
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-001]
children: []
arch_refs: [ARCH-database-schemas]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-Assistant", action: "marked done after implementing raw and stage DDL scripts"}
---
## Description
Create the database tables for the `raw` (initial landing zone) and `stage` (validated data) layers, which are critical for the database-centric ELT workflow.

## Acceptance Criteria
Idempotent DDL scripts are created in `sql/ddl/` that define all tables for the `raw` and `stage` schemas. The scripts can be executed successfully against the target MS SQL database. 