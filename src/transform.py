import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sqlalchemy import MetaData, Table, insert, update, text
from src.transformations.cleansing import clean_phone_number, clean_email
from src.transformations.error_handling import global_error_handler
from src.utils.db import get_engine
import argparse


@global_error_handler('transform')
def main(dataset: str, period: str, rollback_version: int = None):
    engine = get_engine()
    metadata = MetaData()

    if rollback_version:
        # TODO: The rollback logic needs to be aligned with the dataset/period orchestration
        rollback_core_table(rollback_version, engine)
        print(f'Rollback to version {rollback_version} complete.')
        return

    # Dynamic table names based on dataset
    staging_table_name = dataset
    core_schema = "core"
    core_table_name = f"{core_schema}.{dataset}" # Assumption

    # Load data from staging
    with engine.connect() as conn:
        staging_df = pd.read_sql(
            text(f"SELECT * FROM stage.{staging_table_name} WHERE _data_period = :period"),
            conn,
            params={"period": period}
        )
        core_df = pd.read_sql(text(f"SELECT * FROM {core_table_name} WHERE is_current = 1"), conn)

    # SCD-2 logic: identify new, changed, unchanged records
    # (This is a simplified example. Adjust keys/columns as needed.)
    # TODO: Key and attribute columns should be defined per-dataset in a config file
    key_cols = ['citizen_id']
    attr_cols = ['street_name', 'street_code', 'age', 'building_number', 
                 'apartment_number', 'family_index_number']

    merged = pd.merge(staging_df, core_df, on=key_cols, how='left', suffixes=('', '_core'))

    # New records: not in core
    new_records = merged[merged['citizen_id'].isna()]

    # Changed records: in core, but attributes differ
    changed_records = merged[(~merged['citizen_id'].isna()) & (
        (merged[attr_cols] != merged[[f'{c}_core' for c in attr_cols]]).any(axis=1)
    )]

    # Unchanged records: in core, attributes same (not needed for SCD-2 update)

    with engine.begin() as conn:
        core_table = Table(dataset, metadata, schema=core_schema, autoload_with=engine)
        # Insert new records
        if not new_records.empty:
            to_insert = new_records[key_cols + attr_cols].copy()
            conn.execute(insert(core_table), to_insert.to_dict('records'))

        # Update changed records (expire old, insert new)
        if not changed_records.empty:
            # Expire old versions
            old_ids = changed_records['id_core'].tolist()
            conn.execute(update(core_table).where(core_table.c.id.in_(old_ids)).values(is_current=False))

            # Insert new versions
            to_insert = changed_records[key_cols + attr_cols].copy()
            conn.execute(insert(core_table), to_insert.to_dict('records'))

    print('SCD-2 transformation complete.')

def rollback_core_table(version_number, engine):
    # Example: revert core table to only records from the specified version
    # This assumes core table has a version_number column or can be joined to dataset_version
    # Adjust logic as needed for your schema
    with engine.begin() as conn:
        result = conn.execute(text("SELECT dataset_name FROM meta.dataset_version WHERE version_number = :vnum"), {"vnum": version_number}).fetchone()
        if not result:
            print(f"No dataset found for version {version_number}")
            return
        dataset_name = result[0]
        # Example: delete all core records for this dataset and version (customize as needed)
        core_table_name = f"core.{dataset_name}"
        conn.execute(text(f"DELETE FROM core.{core_table_name} WHERE business_key IN (SELECT business_key FROM core.{core_table_name} WHERE version_number = :vnum)"), {"vnum": version_number})
        # Optionally, restore previous records if you keep history elsewhere

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform pipeline with SCD-2 logic or rollback.")
    parser.add_argument("--dataset", type=str, help="Dataset name to process (e.g., 'citizens').")
    parser.add_argument("--period", type=str, help="Period to process (e.g., '2025-07').")
    parser.add_argument("--rollback", type=int, help="Rollback to a specific version number")
    args = parser.parse_args()
    if args.rollback:
        main(dataset=None, period=None, rollback_version=args.rollback)
    elif args.dataset and args.period:
        main(dataset=args.dataset, period=args.period)
    else:
        parser.error("Either --rollback or both --dataset and --period are required.")
