---
id: TASK-2025-002
title: "Phase 1: Ingestion & Validation"
status: done
priority: high
type: feature
estimate: L
assignee:
created: 2025-07-09
updated: 2025-07-10
parents: []
children: [TASK-2025-010, TASK-2025-024, TASK-2025-011, TASK-2025-012, TASK-2025-025]
arch_refs: [ARCH-pipeline-step-ingest, ARCH-pipeline-step-validate, ARCH-data-contract-pandera, ARCH-data-contract-yaml]
audit_log:

{date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}

{date: 2025-07-09, user: "@AI-DocArchitect", action: "marked as done (all child tasks complete)"}

{date: 2025-07-09, user: "@AI-DocArchitect", action: "updated to reflect refactoring to DB-centric flow"}

{date: 2025-07-10, user: "@AI-DocArchitect", action: "Updated to reflect new file-based staging flow with Parquet and period-aware loading."}

Description

This parent task covers the development of the first part of the ELT pipeline: reliably validating source files, transforming them into a clean intermediate format (Parquet), and loading them into the database stage layer.

Acceptance Criteria

All child tasks are completed. The pipeline can successfully process a source file from data/landed/. The ingest.py script validates its name and headers. The validate.py script creates a validated Parquet file in data/stage/cleaned/. The load_stage.py script loads this Parquet file into the correct stage database table using period-aware, transactional logic. All steps are logged to the meta tables. 