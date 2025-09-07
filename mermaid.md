flowchart TD
    A[Data Files - Excel] -->|manual| B{Data integration - Python}
    B -->|auto| C[Data Warehouse - SQL Server]
    C -->|auto| D[Power BI]
    C -->|auto| E[Prepared Data - Excel]
    E -->|manual| F[HAMAL Web App]
    F -->|manual| B

    C@{ shape: database}