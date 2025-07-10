---
id: TASK-2025-012
title: "Task 1.3: Implement Validate Script"
status: done
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-09
updated: 2025-07-10
parents: [TASK-2025-002]
children: []
arch_refs: [ARCH-pipeline-step-validate]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "marked as done (validate.py implemented)"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "description updated to reflect refactoring to DB-centric flow"}
  - {date: 2025-07-10, user: "@AI-DocArchitect", action: "status: refactoring -> done. Updated to reflect raw file to Parquet transformation."}
---
## Description
Implement the validate.py script to perform data transformation and quality checks. It reads a raw source file, applies column mappings, validates it against a Pandera schema, and outputs a clean, typed Parquet file.

## Acceptance Criteria
The script takes a file_id as input. It reads the source file from data/landed/. It applies column mappings from the versioned YAML contract. It validates the resulting DataFrame against its Pandera schema. On success, it writes a Parquet file to data/stage/cleaned/. The result (pass or fail with errors), including the output Parquet path on success, is logged to meta.validation_log. 