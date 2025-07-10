---
id: TASK-2025-030
title: "Create Centralized Dataset Config & Core Utilities"
status: backlog
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-10
updated: 2025-07-10
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-pipeline-utilities]
audit_log:

{date: 2025-07-10, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Establish the core configuration and utility functions to support the new pipeline logic. This includes centralizing dataset rules and creating reusable validation functions.

## Acceptance Criteria
- A new datasets_config.yml is created to define dataset-specific rules (e.g., filename patterns).
- Reusable functions parse_and_validate_filename and validate_headers are implemented in src/utils/parsing.py. 