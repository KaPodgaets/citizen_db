---
id: ARCH-data-contract-pandera
title: "Data Contract: Pandera Schema"
type: data_model
layer: domain
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-10
tags: [pandera, schema, validation, data-quality]
depends_on: []
referenced_by: []
---
## Context
Data contracts are formal agreements on the structure and quality of data. This component uses the Pandera library to define and enforce contracts on data read from source files during the `validate` step. It serves as a major quality gate, focusing on data types, nullability, and content constraints (e.g., value ranges) after column names have been standardized.

## Structure
Each data source will have a corresponding Python module in the `schemas/` directory (e.g., `citizens_schema.py`). These modules contain Pandera `DataFrameSchema` objects that define the data contract.

## Behavior
The schemas specify column names, data types, nullability, and custom validation checks (e.g., regex patterns for phone numbers, value ranges for IDs). These schema objects are imported and used by the `validate.py` script to validate raw dataframes loaded from source files.

## Evolution
### Historical
- v1: Initial design. 