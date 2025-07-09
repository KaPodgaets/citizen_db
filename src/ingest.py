import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import hashlib
import os
import shutil
from sqlalchemy import text
from src.utils.db import get_engine
from src.transformations.error_handling import global_error_handler

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

@global_error_handler('ingest')
def main(file_path):
    engine = get_engine()
    file_hash = calculate_sha256(file_path)
    file_name = os.path.basename(file_path)
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM meta.ingestion_log WHERE file_hash = :hash"), {"hash": file_hash})
        if result.scalar() > 0:
            print(f"Error! File {file_name} already ingested (hash: {file_hash})")
            return
        
        # Copy file to data/stage/
        os.makedirs("data/stage", exist_ok=True)
        dest_path = os.path.join("data/stage", file_name)
        shutil.copy2(file_path, dest_path)
        # Insert log
        conn.execute(text("""
            INSERT INTO meta.ingestion_log (file_name, file_hash, status)
            VALUES (:file_name, :file_hash, 'INGESTED')
        """), {"file_name": file_name, "file_hash": file_hash})
        # get file id
        file_id_result = conn.execute(text("select id from meta.ingestion_log WHERE file_hash = :hash"), {"hash": file_hash})
        row = file_id_result.fetchone()
        if row == None:
            print(f"Error! File id from database is not recieved")
            return
        file_id = row[0]
        print(f"Ingested {file_name} (hash: {file_hash}) file id - {file_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a new source file.")
    parser.add_argument("--file-path", required=True, help="Path to the input file")
    args = parser.parse_args()
    main(args.file_path)
