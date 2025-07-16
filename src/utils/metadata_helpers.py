import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from sqlalchemy import text
from datetime import datetime
from src.transformations.error_handling import global_error_handler


@global_error_handler('transform')
def set_new_active_dataset_version(conn, dataset: str, period: str, version: int):
    with conn:
        # 1. Check is there already dataset
        find_old_versions_sql = text("""
            SELECT id FROM meta.dataset_version
            WHERE dataset = :dataset AND is_active = 1
        """)
        current_dataset_version_raw = conn.execute(find_old_versions_sql, {"dataset": dataset}).fetchall()
        id_of_current_dataset = [row[0] for row in current_dataset_version_raw]
        
        # If current version exists, set is_current = 0
        if id_of_current_dataset:
            update_current_sql = text("""
                UPDATE meta.dataset_version 
                SET is_active = 0 
                WHERE id = :id
            """)
            conn.execute(update_current_sql, {"id": id_of_current_dataset[0]})
            print(f"Set is_active = 0 for previous version ID: {id_of_current_dataset[0]}")

        # 2. Create a new current period record for dataset
        insert_version_sql = text("""
            INSERT INTO meta.dataset_version (dataset, period, version, created_at, is_active)
            VALUES (:dataset, :period, :version, :now, 1)
        """)
        conn.execute(insert_version_sql, {"dataset": dataset, "period": period, "version": version, "now": datetime.now()})