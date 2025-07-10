---
id: TASK-2025-026
title: "Refactor ingest.py and validate.py for File-Based Staging"
status: done
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-10
updated: 2025-07-10
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-pipeline-step-ingest, ARCH-pipeline-step-validate]
audit_log:

{date: 2025-07-10, user: "@AI-DocArchitect", action: "created with status backlog"}
{date: 2025-07-10, user: "@AI-Assistant", action: "marked as done after refactoring ingest.py and validate.py for file-based staging"}
---
## Description
Refactor the ingest.py and validate.py scripts to align with the new file-based staging architecture.

## Acceptance Criteria
- ingest.py is modified to only perform in-place validation of a source file's name and headers in data/landed/, logging the result to meta.ingestion_log. It no longer copies files or loads data.
- validate.py is modified to read a raw source file from data/landed/, apply column mappings, validate the data with Pandera, and write a clean Parquet file to data/stage/cleaned/. 