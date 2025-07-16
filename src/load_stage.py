import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import pandas as pd
from sqlalchemy import text
from src.utils.db import get_engine


def main(validation_log_id: int):
    """
    Loads a validated Parquet file into the corresponding stage database table.
    Implements a transactional "delete-then-append" for period-level idempotency.
    """
    engine = get_engine()
    
    # Retrieve metadata for the validated file
    with engine.connect() as conn:
        query = text("""
            SELECT
                il.file_name,
                il.dataset,
                il.period
            FROM meta.validation_log vl
            JOIN meta.ingestion_log il ON vl.file_id = il.id
            WHERE vl.id = :validation_log_id AND vl.status = 'PASS'
        """)
        result = conn.execute(query, {"validation_log_id": validation_log_id}).fetchone()

    if not result:
        print(f"No 'PASS' record found in meta.validation_log for id {validation_log_id}")
        return

    file_name, dataset, period = result
    base_file_name = os.path.splitext(file_name)[0]
    parquet_path = os.path.join("data/stage/cleaned", f"{base_file_name}.parquet")
    
    if not os.path.exists(parquet_path):
        print(f"Error: Parquet file not found at {parquet_path}")
        # Log failure
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO meta.stage_load_log (validation_log_id, status, error_message)
                VALUES (:validation_log_id, 'FAIL', :error_message)
            """), {"validation_log_id": validation_log_id, "error_message": f"Parquet file not found: {parquet_path}"})
        return

    try:
        df = pd.read_parquet(parquet_path)
        # Add metadata columns for traceability and period-aware loading
        df['_data_period'] = period
        df['_source_parquet_path'] = parquet_path

        target_table = dataset
        
        with engine.begin() as conn:
            # 1. Delete existing data for the period (idempotency)
            # We keep only 1 (the last) version of dataset+period key
            conn.execute(text(f"DELETE FROM stage.{target_table} WHERE _data_period = :period"), {"period": period})
            
            # 2. Append new data
            df.to_sql(target_table, conn, schema='stage', if_exists='append', index=False)

            # 3. Log success
            conn.execute(text("""
                INSERT INTO meta.stage_load_log (validation_log_id, status)
                VALUES (:validation_log_id, 'PASS')
            """), {"validation_log_id": validation_log_id})

        print(f"Successfully loaded {parquet_path} into stage.{target_table} for period {period}.")

    except Exception as e:
        print(f"Failed to load {parquet_path} to stage: {e}")
        # Log failure
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO meta.stage_load_log (validation_log_id, status, error_message)
                VALUES (:validation_log_id, 'FAIL', :error_message)
            """), {"validation_log_id": validation_log_id, "error_message": str(e)})
        # Re-raise the exception to make the pipeline step fail
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load a validated Parquet file into a database stage table.",
        epilog="This script performs a transactional delete-then-append operation based on the data period."
    )
    parser.add_argument("--validation-log-id", required=True, type=int, help="The ID from meta.validation_log for the file to load.")
    args = parser.parse_args()
    main(args.validation_log_id) 