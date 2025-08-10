flowchart TD
    A[Data Files] --> B{Data integration}
    B --> C[Data Warehouse]
    C --> D[Power BI]
    C --> E[xlsx file]
    E --> F[HAMAL Web App]
    F -->|Daily update| B

    C@{ shape: database}


---

flowchart TD
    A[קבצי נתונים ממערכות מידע] --> B{עבוד נתונים}
    B --> C[מחסן נתונים]
    C -->|עדכון אוטומטי| D[Power BI]
    C -->|גישה ישרת| E[.xlsx file]
    E -->|עלית נתונים ידני| F[HAMAL Web App]
    F -->|עדכון יומי ידני| B

    C@{ shape: database}