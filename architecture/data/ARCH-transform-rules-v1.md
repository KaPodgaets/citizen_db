---
id: ARCH-transform-rules
title: "Data Cleansing Transformation Rules"
type: component
layer: domain
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-09
tags: [python, transformation, business-logic, cleansing]
depends_on: []
referenced_by: []
---
## Context
This component defines the business rules and data cleansing logic applied during the transformation step. Each function is implemented as a pure, testable Python function in the `src/transformations/` directory.

## Structure
Each function is designed to be pure and testable, typically accepting a pandas Series or DataFrame and returning a modified version. The `transform.py` script imports and applies these functions to the staged data during the transformation process.

## Evolution
### Historical
- v1: Initial design. 