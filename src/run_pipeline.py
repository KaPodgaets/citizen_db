import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import subprocess
from sqlalchemy import text
from src.utils.db import get_engine
from datetime import datetime


def trigger_validation():
    """Finds ingested files and triggers the validation script for each."""
    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT id FROM meta.ingestion_log 
            WHERE id NOT IN (SELECT file_id FROM meta.validation_log)
        """)
        ingested_files = conn.execute(query).fetchall()
        for row in ingested_files:
            file_id = row[0]
            print(f"Triggering validation for file_id: {file_id}")
            subprocess.run(['python', 'src/validate.py', '--file-id', str(file_id)], check=True)


def trigger_stage_load():
    """Finds validated files and triggers the stage loading script for each."""
    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT id FROM meta.validation_log 
            WHERE status = 'PASS' AND id NOT IN (SELECT validation_log_id FROM meta.stage_load_log)
        """)
        validated_files = conn.execute(query).fetchall()
        for row in validated_files:
            validation_log_id = row[0]
            print(f"Triggering stage load for validation_log_id: {validation_log_id}")
            subprocess.run(['python', 'src/load_stage.py', '--validation-log-id', str(validation_log_id)], check=True)


def prepare_transforms():
    """Identifies new dataset/period combinations from staging and creates PENDING tasks."""
    engine = get_engine()
    with engine.begin() as conn:
        # Find dataset-periods that were successfully staged but not yet transformed
        query = text("""
            WITH StagedWork AS (
                SELECT DISTINCT il.dataset_name, il.period
                FROM meta.stage_load_log sll
                JOIN meta.validation_log vl ON sll.validation_log_id = vl.id
                JOIN meta.ingestion_log il ON vl.file_id = il.id
                WHERE sll.status = 'PASS'
            )
            SELECT sw.dataset_name, sw.period
            FROM StagedWork sw
            LEFT JOIN meta.transform_log tl ON sw.dataset_name = tl.dataset_name AND sw.period = tl.period
            WHERE tl.id IS NULL OR tl.status = 'FAIL';
        """)
        new_work = conn.execute(query).fetchall()

        for dataset_name, period in new_work:
            # Check if a 'FAIL' record already exists to avoid creating duplicates
            check_query = text("SELECT id FROM meta.transform_log WHERE dataset_name = :d AND period = :p")
            exists = conn.execute(check_query, {"d": dataset_name, "p": period}).fetchone()
            if not exists:
                print(f"Creating PENDING transform task for {dataset_name}/{period}")
                insert_query = text("""
                    INSERT INTO meta.transform_log (dataset_name, period, status, retry_count, last_attempt_timestamp)
                    VALUES (:dataset, :period, 'PENDING', 0, :now)
                """)
                conn.execute(insert_query, {"dataset": dataset_name, "period": period, "now": datetime.now()})


def trigger_transforms():
    """Triggers the transform script for PENDING tasks or failed tasks that can be retried."""
    engine = get_engine()
    
    # Find tasks that need to be run
    query = text("SELECT id, dataset_name, period FROM meta.transform_log WHERE status = 'PENDING' OR (status = 'FAIL' AND retry_count < 1)")
    tasks_to_run = engine.connect().execute(query).fetchall()

    for task_id, dataset, period in tasks_to_run:
        print(f"Triggering transform for {dataset}/{period} (Task ID: {task_id})")
        proc = subprocess.run(
            ['python', 'src/transform.py', '--dataset', dataset, '--period', period],
            capture_output=True, text=True
        )

        with engine.begin() as conn:
            if proc.returncode == 0:
                # Success
                update_query = text("UPDATE meta.transform_log SET status = 'PASS', last_attempt_timestamp = :now WHERE id = :id")
                conn.execute(update_query, {"now": datetime.now(), "id": task_id})
                print(f"Transform for {dataset}/{period} SUCCEEDED.")
            else:
                # Failure
                error_msg = proc.stderr or proc.stdout
                update_query = text("""
                    UPDATE meta.transform_log 
                    SET status = 'FAIL', retry_count = retry_count + 1, last_attempt_timestamp = :now, error_message = :err
                    WHERE id = :id
                """)
                conn.execute(update_query, {"now": datetime.now(), "err": error_msg, "id": task_id})
                print(f"Transform for {dataset}/{period} FAILED. See meta.transform_log for details.")


if __name__ == "__main__":
    print("--- Pipeline Orchestrator Starting ---")
    # trigger_validation() # In a real scenario, ingestion would be separate. For now, assume files are ingested.
    trigger_stage_load()
    prepare_transforms()
    trigger_transforms()
    print("--- Pipeline Orchestrator Finished ---")
