import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import hashlib
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from src.utils.db import get_engine
from src.transformations.error_handling import global_error_handler
from src.utils.source_file_validator import parse_and_validate_filename, validate_headers


@global_error_handler('ingest')
def main(file_path):
    engine = get_engine()

    file_name = os.path.basename(file_path)
    # 1. Validate filename and extract metadata
    try:
        filename_metadata = parse_and_validate_filename(file_name)
    except Exception as e:
        print(f"Filename validation failed: {e}")
        return
    # 2. Read headers from the file (assume Excel for now)
    try:
        # Load and map columns based on file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.csv':
            headers = pd.read_csv(file_path, nrows=0).columns.tolist()
        elif file_extension == '.xlsx':
            headers = pd.read_excel(file_path, nrows=0).columns.tolist()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Only .csv and .xlsx files are supported.")
        
    except Exception as e:
        print(f"Failed to read headers from file: {e}")
        return
    # 3. Validate headers
    try:
        validate_headers(headers, filename_metadata['contract'], filename_metadata['period'])
    except Exception as e:
        print(f"Header validation failed: {e}")
        return
    # 4. Calculate file hash
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()
    # 5. Idempotency check and log
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM meta.ingestion_log WHERE file_hash = :hash"), {"hash": file_hash})
        if result.scalar() > 0:
            print(f"File {file_name} already ingested (hash: {file_hash})")
            return
        # Insert log
        conn.execute(text("""
            INSERT INTO meta.ingestion_log (file_name, file_hash, ingest_time, status, dataset_name, period)
            VALUES (:file_name, :file_hash, :datetime_now, 'INGESTED', :dataset, :period)
        """), {
            "file_name": file_name,
            "file_hash": file_hash,
            "datetime_now": datetime.now(),
            "dataset": filename_metadata["dataset"],
            "period": filename_metadata["period"]
        })
        
        file_id_result = conn.execute(text("select id from meta.ingestion_log WHERE file_hash = :hash"), {"hash": file_hash})
        row = file_id_result.fetchone()
        if row is None:
            print("Error! File id from database is not received")
            return
        file_id = row[0]
        print(f"Ingested {file_name} (hash: {file_hash}) file id - {file_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a new source file.")
    parser.add_argument("--file-path", required=True, help="Path to the input file in data/landed/")
    args = parser.parse_args()
    main(args.file_path)
