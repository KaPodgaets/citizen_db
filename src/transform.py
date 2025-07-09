import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, text
from src.transformations.cleansing import clean_phone_number, clean_email
from src.transformations.error_handling import global_error_handler
import argparse

# Placeholder: configure your database URI
DATABASE_URI = 'postgresql://user:password@localhost:5432/citizen_db'
engine = create_engine(DATABASE_URI)
metadata = MetaData()

# Placeholder: define your table names
STAGING_TABLE = 'staging_citizen'
CORE_TABLE = 'citizen_core'

@global_error_handler('transform')
def main(rollback_version=None):
    if rollback_version:
        rollback_core_table(rollback_version)
        print(f'Rollback to version {rollback_version} complete.')
        return
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

def rollback_core_table(version_number):
    # Example: revert core table to only records from the specified version
    # This assumes core table has a version_number column or can be joined to dataset_version
    # Adjust logic as needed for your schema
    with engine.begin() as conn:
        # Find dataset_name for this version
        result = conn.execute(text("SELECT dataset_name FROM meta.dataset_version WHERE version_number = :vnum AND is_active = 1"), {"vnum": version_number})
        row = result.fetchone()
        if not row:
            print(f"No active dataset version {version_number} found.")
            return
        dataset_name = row[0]
        # Example: delete all core records for this dataset and version (customize as needed)
        conn.execute(text(f"DELETE FROM {CORE_TABLE} WHERE business_key IN (SELECT business_key FROM {CORE_TABLE} WHERE version_number = :vnum)"), {"vnum": version_number})
        # Optionally, restore previous records if you keep history elsewhere

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform pipeline with SCD-2 logic or rollback.")
    parser.add_argument("--rollback", type=int, help="Rollback to a specific version number")
    args = parser.parse_args()
    main(rollback_version=args.rollback)
