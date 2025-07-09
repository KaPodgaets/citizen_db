---
id: ARCH-transform-rules
title: "Data Cleansing Transformation Rules"
type: component
layer: domain
owner: "@team-data"
version: v1
status: planned
created: 2025-07-09
updated: 2025-07-09
tags: [python, transformation, business-logic, cleansing]
depends_on: []
referenced_by: []
---
## Context
This component isolates complex, domain-specific data cleansing and transformation logic from the main pipeline orchestration scripts. This separation improves modularity, testability, and maintainability of the business rules.

## Structure
The rules are implemented as pure Python functions within modules in the `src/transformations/` directory. For example:
- `citizen_rules.py`: Functions for cleansing citizen data (e.g., name parsing, address standardization).
- `phone_rules.py`: Functions for phone number validation and formatting.

## Behavior
Each function is designed to be pure and testable, typically accepting a pandas Series or DataFrame and returning a modified version. The `transform.py` script imports and applies these functions to the staged data during the transformation process.

## Evolution
### Planned
- Initial implementation of cleansing rules for citizen and phone data.

### Historical
- v1: Initial design. 