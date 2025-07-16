import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import subprocess
import yaml
from sqlalchemy import text
from src.utils.db import get_engine
from datetime import datetime


def trigger_validation():
    """Finds ingested files with status 'INGESTED' and triggers the validation script for each."""
    engine = get_engine()
    with engine.connect() as conn:
        query = text("""
            SELECT id 
            FROM meta.ingestion_log 
            WHERE 
                status = 'INGESTED' 
                AND id NOT IN (
                    SELECT file_id 
                    FROM meta.validation_log 
                    where status != 'PASS')
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
    """Identifies new work for the transform step and creates PENDING records."""
    engine = get_engine()
    
    with engine.connect() as conn:
        # Find successful stage loads that don't have a PASS record in transform_log
        # Join through: stage_load_log -> validation_log -> ingestion_log to get dataset info
        query = text("""
            SELECT il.dataset, il.period
            FROM meta.stage_load_log sll
            JOIN meta.validation_log vl ON sll.validation_log_id = vl.id
            JOIN meta.ingestion_log il ON vl.file_id = il.id
            LEFT JOIN meta.transform_log tl ON il.dataset = tl.dataset AND il.period = tl.period
            WHERE sll.status = 'PASS' AND tl.status IS NULL
        """)
        new_work = conn.execute(query).fetchall()

        if not new_work:
            print("No new transform tasks to create.")
            return

        for dataset, period in new_work:
            # Check if a 'FAIL' record already exists to avoid creating duplicates
            check_query = text("SELECT id FROM meta.transform_log WHERE dataset = :d AND period = :p")
            existing = conn.execute(check_query, {"d": dataset, "p": period}).fetchone()
            
            if not existing:
                insert_query = text("""
                    INSERT INTO meta.transform_log (dataset, period, status, retry_count)
                    VALUES (:dataset, :period, 'PENDING', 0)
                """)
                conn.execute(insert_query, {"dataset": dataset, "period": period})
                conn.commit()
                print(f"Created PENDING transform task for {dataset}/{period}")


def trigger_transforms():
    """Triggers the transform script for PENDING tasks or failed tasks that can be retried."""
    engine = get_engine()
    with open("datasets_config.yml", 'r', encoding='utf-8') as f:
        datasets_config = yaml.safe_load(f)
    
    # Find tasks that need to be run
    query = text("SELECT id, dataset, period FROM meta.transform_log WHERE status = 'PENDING' OR (status = 'FAIL' AND retry_count < 1)")
    tasks_to_run = engine.connect().execute(query).fetchall()

    for task_id, dataset, period in tasks_to_run:
        script_path = datasets_config.get(dataset, {}).get('transform_script')
        if not script_path:
            error_msg = f"Transform script not defined for dataset '{dataset}' in datasets_config.yml"
            print(error_msg)
            with engine.begin() as conn:
                update_query = text("UPDATE meta.transform_log SET status = 'FAIL', error_message = :err, retry_count = 99 WHERE id = :id")
                conn.execute(update_query, {"err": error_msg, "id": task_id})
            continue

        print(f"Triggering transform for {dataset}/{period} (Task ID: {task_id})")
        proc = subprocess.run(
            ['python', script_path, '--dataset', dataset, '--period', period],
            capture_output=True, text=True
        )

        with engine.begin() as conn:
            if proc.returncode == 0:
                # Success
                update_query = text("UPDATE meta.transform_log SET status = 'PASS', last_attempt_timestamp = :now, error_message = NULL WHERE id = :id")
                conn.execute(update_query, {"now": datetime.now(), "id": task_id})
                print(f"Transform for {dataset}/{period} SUCCEEDED.")
            else:
                # Failure
                error_msg = proc.stderr or proc.stdout
                print(f"Transform for {dataset}/{period} FAILED. Error:\n{error_msg}")
                update_query = text("""
                    UPDATE meta.transform_log 
                    SET status = 'FAIL', retry_count = retry_count + 1, last_attempt_timestamp = :now, error_message = :err
                    WHERE id = :id
                """)
                conn.execute(update_query, {"now": datetime.now(), "err": error_msg, "id": task_id})
                print(f"See meta.transform_log (ID: {task_id}) for details.")


def trigger_publish():
    """Triggers the publish script of datamart layer """
    print("[orchestrator] : Triggering publish script (publish.py)")
    subprocess.run(['python', 'src/publish.py'], check=True)


if __name__ == "__main__":
    print("--- Pipeline Orchestrator Starting ---")
    trigger_validation() # In a real scenario, ingestion would be separate. For now, assume files are ingested.
    trigger_stage_load()
    prepare_transforms()
    trigger_transforms()
    trigger_publish()
    print("--- Pipeline Orchestrator Finished ---")
