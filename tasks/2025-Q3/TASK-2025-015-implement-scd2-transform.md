---
id: TASK-2025-015
title: "Task 2.3: Implement SCD-2 Logic in transform.py"
status: backlog
priority: medium
type: feature
estimate: L
assignee: 
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-003]
children: []
arch_refs: [ARCH-pipeline-step-transform]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-Assistant", action: "marked done after implementing SCD-2 logic in transform.py"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "description updated to reflect refactoring to DB-centric flow"}
---
## Description
Implement the core transformation logic to build the historized `core` data layer. This involves correctly identifying new, changed, and unchanged records.

## Acceptance Criteria
The `transform.py` script imports and applies cleansing functions from `src/transformations`. It reads data from the `stage` database tables, uses pandas to determine changes against the `core` tables, and then uses SQLAlchemy Core to execute efficient bulk INSERT/UPDATE operations to apply SCD-2 logic. 