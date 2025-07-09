---
id: TASK-2025-013
title: "Task 2.1: Implement SQL DDL for core and mart Schemas"
status: done
priority: medium
type: feature
estimate: M
assignee: 
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-003]
children: []
arch_refs: [ARCH-database-schemas]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-Assistant", action: "marked done after implementing idempotent DDL scripts for core and mart schemas"}
---
## Description
Create the target tables for the transformed data in both the `core` (historized) and `mart` (analytics) layers.

## Acceptance Criteria
Idempotent DDL scripts named `sql/ddl/core_schema.sql` and `sql/ddl/mart_schema.sql` are created. These scripts can be run successfully to create all required tables and views. 