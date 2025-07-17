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
        count = result.scalar()
        if count is not None and count > 0:
            print(f"[WAR]: File {file_name} already ingested (hash: {file_hash}). That means there is no changes in data")
            return
        # Also check for duplicate (dataset, period, version)
        result = conn.execute(text("SELECT COUNT(*) FROM meta.ingestion_log WHERE dataset = :dataset AND period = :period AND version = :version"), {"dataset": filename_metadata["dataset"], "period": filename_metadata["period"], "version": filename_metadata["version"]})
        count = result.scalar()
        if count is not None and count > 0:
            print(f"""[WAR]: A record with 
                    dataset={filename_metadata['dataset']},
                    period={filename_metadata['period']},
                    version={filename_metadata['version']}
                    already exists in ingestion_log.""")
            return
        # Check if the new file's version is less than the max version for the same dataset and period
        max_version_result = conn.execute(text("SELECT MAX(version) FROM meta.ingestion_log WHERE dataset = :dataset AND period = :period"), {"dataset": filename_metadata["dataset"], "period": filename_metadata["period"]})
        max_version_row = max_version_result.fetchone()
        if max_version_row and max_version_row[0] is not None:
            max_version = max_version_row[0]
            if filename_metadata["version"] < max_version:
                print(f"""
                    [WAR]: The version of the new file ({filename_metadata['version']})
                    is less than the max version ({max_version}) 
                    for dataset={filename_metadata['dataset']} and period={filename_metadata['period']}.
                    File will not be ingested.""")
                return
        
        # Insert log
        conn.execute(text("""
            INSERT INTO meta.ingestion_log (file_name, file_hash, ingest_time, status, dataset, period, version)
            VALUES (:file_name, :file_hash, :datetime_now, 'INGESTED', :dataset, :period, :version)
        """), {
            "file_name": file_name,
            "file_hash": file_hash,
            "datetime_now": datetime.now(),
            "dataset": filename_metadata["dataset"],
            "period": filename_metadata["period"],
            "version": filename_metadata["version"]
        })
        
        file_id_result = conn.execute(text("select id from meta.ingestion_log WHERE file_hash = :hash"), {"hash": file_hash})
        row = file_id_result.fetchone()
        if row is None:
            print("Error! File id from database is not received")
            return
        file_id = row[0]
        print(f"Ingested {file_name} (hash: {file_hash}) file id - {file_id}")

        # Mark previous records with the same dataset and period as OBSOLET
        update_obsolet_sql = text("""
            UPDATE meta.ingestion_log
            SET status = 'OBSOLET'
            WHERE dataset = :dataset AND period = :period AND file_hash != :file_hash
        """)
        conn.execute(update_obsolet_sql, {"dataset": filename_metadata["dataset"], "period": filename_metadata["period"], "file_hash": file_hash})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a new source file.")
    parser.add_argument("--file-path", required=True, help="Path to the input file in data/landed/")
    args = parser.parse_args()
    main(args.file_path)
