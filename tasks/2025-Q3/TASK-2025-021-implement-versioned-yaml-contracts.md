---
id: TASK-2025-021
title: "Task 0.7: Implement Versioned YAML Contracts for Column Mapping"
status: done
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-001]
children: []
arch_refs: [ARCH-data-contract-yaml]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-Assistant", action: "marked done after implementing versioned YAML contract for citizens"}
---
## Description
Create the system for managing source-to-target column mappings using versioned YAML files. This decouples mapping logic from the application code.

## Acceptance Criteria
A `contracts/` directory is created. For each dataset, a single YAML file (e.g., `citizens.yml`) is created containing a list of versioned `column_mapping` objects. 