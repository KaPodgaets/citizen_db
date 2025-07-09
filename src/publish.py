from sqlalchemy import create_engine, text

# Placeholder: configure your database URI
DATABASE_URI = 'postgresql://user:password@localhost:5432/citizen_db'
engine = create_engine(DATABASE_URI)

# Example mart table and core source
MART_TABLE = 'citizen_mart_fact'
CORE_TABLE = 'citizen_core'

# Example: SQL to truncate and reload mart table from core
TRUNCATE_SQL = f'TRUNCATE TABLE {MART_TABLE};'
INSERT_SQL = f'''
INSERT INTO {MART_TABLE} (business_key, attribute1, attribute2, snapshot_date, metric1, metric2)
SELECT business_key, attribute1, attribute2, CURRENT_DATE, 0, 0
FROM {CORE_TABLE}
WHERE is_current = TRUE;
'''

with engine.begin() as conn:
    conn.execute(text(TRUNCATE_SQL))
    conn.execute(text(INSERT_SQL))

print('Mart population complete.')
