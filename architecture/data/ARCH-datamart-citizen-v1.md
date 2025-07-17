---
id: ARCH-datamart-citizen
title: "Datamart: Citizen"
type: data_model
layer: infrastructure
owner: "@team-data"
version: v1
status: current
created: 2025-07-13
updated: 2025-07-13
tags: [sql, ddl, mssql, data-model, mart]
depends_on: [ARCH-database-schemas]
referenced_by: []
---
## Context
This document describes the mart.citizen_datamart table. This table provides a single, comprehensive, and denormalized view of citizen information, optimized for direct analytical queries and reporting. It consolidates data from various core tables.

## Structure
The table is created and managed via DDL scripts in sql/ddl/mart_schema.sql.

| Column Name | Type | Description |
|---|---|---|
| citizen_id | INT | Primary identifier for the citizen. |
| first_name | NVARCHAR(MAX) | Citizen's first name. |
| last_name | NVARCHAR(MAX) | Citizen's last name. |
| birth_date | DATE | Citizen's date of birth. |
| age | INT | Citizen's age. |
| gender | NVARCHAR(50) | Citizen's gender. |
| street_name | NVARCHAR(MAX) | Street name of residence. |
| street_code | INT | Code for the street. |
| building_number | INT | Building number of residence. |
| apartment_number | INT | Apartment number of residence. |
| family_index_number | INT | Family index number. |
| is_welfare_patient | BIT | Flag (1 or 0) indicating if the citizen is in the welfare patients table. |
| has_phone | BIT | Flag (1 or 0) indicating if the citizen has at least one phone number. |
| has_mobile_phone | BIT | Flag (1 or 0) indicating if the citizen has a mobile phone. |
| phone_number_1 | NVARCHAR(50) | Highest priority phone number (mobile first). |
| phone_number_2 | NVARCHAR(50) | Second highest priority phone number. |
| phone_number_3 | NVARCHAR(50) | Third highest priority phone number. |

## Behavior
This table is populated by the src/publish_citizen_mart.py script. The script performs a full TRUNCATE of the table followed by an INSERT with data transformed from the core layer. This ensures the datamart is always a fresh reflection of the core data.

## Evolution
### Historical
- v1: Initial design of the citizen datamart. 