import argparse
import pandas as pd
from sqlalchemy import text
from src.utils.db import get_engine
import sys


def main(filepath):
    # Load Excel file
    df = pd.read_excel(filepath)

    # Validate columns
    required_columns = {'citizen_id', 'fake_citizen_id'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        print(f"[FAIL] Missing required columns in file: {missing}")
        sys.exit(1)

    # Validate types
    if not pd.api.types.is_integer_dtype(df['citizen_id']):
        print("[FAIL] citizen_id column must be of integer type")
        sys.exit(1)
    if not pd.api.types.is_integer_dtype(df['fake_citizen_id']):
        print("[FAIL] fake_citizen_id column must be of integer type")
        sys.exit(1)

    # Check for duplicates in citizen_id
    dup_citizen_id = df[df.duplicated('citizen_id', keep=False)]
    if not dup_citizen_id.empty:
        print("[FAIL] Duplicate citizen_id values found:")
        for val in dup_citizen_id['citizen_id'].unique():
            print(f"    citizen_id={val}")
        sys.exit(1)

    # Check for duplicates in fake_citizen_id
    dup_fake_citizen_id = df[df.duplicated('fake_citizen_id', keep=False)]
    if not dup_fake_citizen_id.empty:
        print("[FAIL] Duplicate fake_citizen_id values found:")
        for val in dup_fake_citizen_id['fake_citizen_id'].unique():
            print(f"    fake_citizen_id={val}")
        sys.exit(1)

    engine = get_engine()
    with engine.connect() as conn:
        # Fetch all existing ids from the table
        existing_citizen_ids = set(row[0] for row in conn.execute(text("SELECT citizen_id FROM core.fake_citizen_ids")).fetchall())
        existing_fake_citizen_ids = set(row[0] for row in conn.execute(text("SELECT fake_citizen_id FROM core.fake_citizen_ids")).fetchall())

        # Check for overlaps in-memory
        overlap_citizen_id = set(df['citizen_id']) & existing_citizen_ids
        overlap_fake_citizen_id = set(df['fake_citizen_id']) & existing_fake_citizen_ids

        if overlap_citizen_id:
            print("[FAIL] citizen_id values already exist in fake_citizen_ids table:")
            for val in overlap_citizen_id:
                print(f"    citizen_id={val}")
            sys.exit(1)
        if overlap_fake_citizen_id:
            print("[FAIL] fake_citizen_id values already exist in fake_citizen_ids table:")
            for val in overlap_fake_citizen_id:
                print(f"    fake_citizen_id={val}")
            sys.exit(1)

        # Insert data
        df.to_sql('fake_citizen_ids', conn, if_exists='append', index=False)
        print(f"[PASS] Successfully inserted {len(df)} records into fake_citizen_ids table.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill fake_citizen_ids table from snapshot Excel file.")
    parser.add_argument('--filepath', required=True, help='Path to the Excel snapshot file')
    args = parser.parse_args()
    main(args.filepath) 