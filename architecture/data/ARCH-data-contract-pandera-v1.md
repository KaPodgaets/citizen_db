---
id: ARCH-data-contract-pandera
title: "Data Contracts (Pandera Schemas)"
type: data_model
layer: domain
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-09
tags: [pandera, schema, validation, data-quality]
depends_on: []
referenced_by: []
---
## Context
Data contracts are formal agreements on the structure and quality of data. This component uses the Pandera library to define and enforce contracts on data *after* it has been loaded into the `raw` layer and had its columns standardized. It serves as the second major quality gate, focusing on data types, nullability, and content constraints (e.g., value ranges).

## Structure
Each data source will have a corresponding Python module in the `schemas/` directory (e.g., `citizens_schema.py`). These modules contain Pandera `DataFrameSchema` objects that define the data contract.

## Behavior
The schemas specify column names, data types, nullability, and custom validation checks (e.g., regex patterns for phone numbers, value ranges for IDs). These schema objects are imported and used by the `validate.py` script to validate raw dataframes loaded from source files.

### Historical
- v1: Initial design. 