---
id: TASK-2025-011
title: "Task 1.2: Implement Ingest Script"
status: refactoring
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-002]
children: []
arch_refs: [ARCH-pipeline-step-ingest, ARCH-data-contract-yaml]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "marked as done (ingest.py implemented)"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "description updated to reflect refactoring to DB-centric flow"}
---
## Description
Implement the `ingest.py` script to be the primary quality gate and entrypoint for data. The script is responsible for validating filenames, selecting and applying versioned column-mapping contracts, parsing data, and loading it transactionally into the `raw` database schema.

## Acceptance Criteria
The script correctly rejects files that fail filename validation. For valid files, it reads the XLSX, loads the correct versioned YAML contract, renames columns, parses dates, and bulk-loads the result into the appropriate `raw` table. The entire database operation is atomic. Failures at any step (e.g., missing contract, DB error) are handled gracefully with clear messages, and no partial data is left in the database. Successful ingestion is logged to `meta.ingestion_log`. 