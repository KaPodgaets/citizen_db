import argparse
import os
import pandas as pd
import pandera as pa
from sqlalchemy import text
from src.utils.db import get_engine
from schemas.citizens_schema import citizens_schema
from src.transformations.error_handling import global_error_handler

@global_error_handler('validate')
def main(file_id):
    engine = get_engine()
    with engine.connect() as conn:
        # Get file info from ingestion_log
        result = conn.execute(text("SELECT file_name FROM meta.ingestion_log WHERE id = :id"), {"id": file_id})
        row = result.fetchone()
        if not row:
            print(f"No file found for file_id {file_id}")
            return
        file_name = row[0]
        file_path = os.path.join("data/land", file_name)
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist")
            return
        # Load and validate
        df = pd.read_excel(file_path)
        try:
            validated_df = citizens_schema.validate(df)
            os.makedirs("data/stage/clean", exist_ok=True)
            parquet_path = os.path.join("data/stage/clean", file_name + ".parquet")
            validated_df.to_parquet(parquet_path)
            status = "PASS"
            error_report = None
            print(f"Validation passed. Parquet written to {parquet_path}")
        except pa.errors.SchemaError as e:
            status = "FAIL"
            error_report = str(e)
            print(f"Validation failed: {e}")
        # Log result
        conn.execute(text("""
            INSERT INTO meta.validation_log (file_id, status, error_report)
            VALUES (:file_id, :status, :error_report)
        """), {"file_id": file_id, "status": status, "error_report": error_report})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a landed file by file_id.")
    parser.add_argument("--file-id", required=True, type=int, help="File ID from ingestion_log")
    args = parser.parse_args()
    main(args.file_id)
