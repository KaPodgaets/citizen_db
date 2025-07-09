import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, insert, update
from src.transformations.cleansing import clean_phone_number, clean_email

# Placeholder: configure your database URI
DATABASE_URI = 'postgresql://user:password@localhost:5432/citizen_db'
engine = create_engine(DATABASE_URI)
metadata = MetaData()

# Placeholder: define your table names
STAGING_TABLE = 'staging_citizen'
CORE_TABLE = 'citizen_core'

# Load data from staging
with engine.connect() as conn:
    staging_df = pd.read_sql_table(STAGING_TABLE, conn)
    core_df = pd.read_sql_table(CORE_TABLE, conn)

# Apply cleansing functions
staging_df['phone'] = clean_phone_number(staging_df['phone'])
staging_df['email'] = clean_email(staging_df['email'])

# SCD-2 logic: identify new, changed, unchanged records
# (This is a simplified example. Adjust keys/columns as needed.)
key_cols = ['business_key']
attr_cols = ['attribute1', 'attribute2', 'phone', 'email']

merged = pd.merge(staging_df, core_df, on=key_cols, how='left', suffixes=('', '_core'))

# New records: not in core
new_records = merged[merged['id_core'].isna()]

# Changed records: in core, but attributes differ
changed_records = merged[(~merged['id_core'].isna()) & (
    (merged[attr_cols] != merged[[f'{c}_core' for c in attr_cols]]).any(axis=1)
)]

# Unchanged records: in core, attributes same (not needed for SCD-2 update)

with engine.begin() as conn:
    core_table = Table(CORE_TABLE, metadata, autoload_with=engine)
    # Insert new records
    if not new_records.empty:
        to_insert = new_records[key_cols + attr_cols].copy()
        to_insert['valid_from'] = pd.Timestamp.now()
        to_insert['valid_to'] = None
        to_insert['is_current'] = True
        conn.execute(insert(core_table), to_insert.to_dict(orient='records'))
    # Expire old records and insert changed as new
    for _, row in changed_records.iterrows():
        # Expire old
        conn.execute(update(core_table)
            .where(core_table.c.business_key == row['business_key'])
            .where(core_table.c.is_current == True)
            .values(valid_to=pd.Timestamp.now(), is_current=False))
        # Insert new
        new_row = {col: row[col] for col in key_cols + attr_cols}
        new_row['valid_from'] = pd.Timestamp.now()
        new_row['valid_to'] = None
        new_row['is_current'] = True
        conn.execute(insert(core_table), new_row)

print('SCD-2 transformation complete.')
