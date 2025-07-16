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
        # Selects validation_log records with status 'PASS', whose corresponding ingestion_log record is 'INGESTED',
        # and which do not have a 'PASS' record in stage_load_log for that validation_log_id.
        query = text("""
            SELECT vl.id
            FROM meta.validation_log vl
            JOIN meta.ingestion_log il ON vl.file_id = il.id
            WHERE vl.status = 'PASS'
              AND il.status = 'INGESTED'
              AND vl.id NOT IN (
                  SELECT validation_log_id FROM meta.stage_load_log WHERE status = 'PASS'
              )
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
        # For each stage_load_log record:
        # - with status 'PASS'
        # - with status 'INGESTED' in ingestion_log table (through validation_log table)
        # - with period and version greater than period and version of record with is_active = 1 from dataset_version table for the same dataset
        query = text("""
            SELECT il.dataset_name, il.period, il.version, sll.id as stage_load_task_id
            FROM meta.stage_load_log sll
            JOIN meta.validation_log vl ON sll.validation_log_id = vl.id
            JOIN meta.ingestion_log il ON vl.file_id = il.id
            WHERE sll.status = 'PASS'
              AND il.status = 'INGESTED'
              AND (
                  il.period > (
                      SELECT dv.period FROM meta.dataset_version dv WHERE dv.dataset_name = il.dataset_name AND dv.is_active = 1
                  )
                  OR (
                      il.period = (
                          SELECT dv.period FROM meta.dataset_version dv WHERE dv.dataset_name = il.dataset_name AND dv.is_active = 1
                      )
                      AND il.version > (
                          SELECT dv.version FROM meta.dataset_version dv WHERE dv.dataset_name = il.dataset_name AND dv.is_active = 1
                      )
                  )
              )
        """)
        new_work = conn.execute(query).fetchall()

        if not new_work:
            print("No new transform tasks to create.")
            return

        failed_tasks = []
        for dataset_name, period, version, stage_load_task_id in new_work:
            # Only create a new task if there is no record for the same stage_load_task_id
            check_query = text("""
                SELECT 
                    id, status
                FROM meta.transform_log 
                WHERE stage_load_task_id = :stage_load_task_id
            """)
            existing = conn.execute(check_query, {"stage_load_task_id": stage_load_task_id}).fetchone()
            
            if not existing:
                insert_query = text("""
                    INSERT INTO meta.transform_log (dataset_name, period, version, stage_load_task_id, status, retry_count)
                    VALUES (:dataset, :period, :version, :stage_load_task_id, 'PENDING', 0)
                """)
                conn.execute(insert_query, {"dataset": dataset_name, "period": period, "version": version, "stage_load_task_id": stage_load_task_id})
                conn.commit()
                print(f"Created PENDING transform task for {dataset_name}/{period}/{version} (stage_load_task_id={stage_load_task_id})")
            else:
                # If exists and status is FAIL, add to failed_tasks
                _, status = existing
                if status == 'FAIL':
                    failed_tasks.append((dataset_name, period, version))
                    
        for dataset_name, period, version in failed_tasks:
            print(f"""
                [ALERT]: You MUST provide new data (file) for dataset '{dataset_name}' and period '{period}'
                because the actual dataset version {version} failed to transform and ran out of retries,
                but no new version was ingested.""")
        

def trigger_transforms():
    """Triggers the transform script for PENDING tasks or failed tasks that can be retried."""
    engine = get_engine()
    with open("datasets_config.yml", 'r', encoding='utf-8') as f:
        datasets_config = yaml.safe_load(f)
    
    # Find tasks that need to be run
    query = text("SELECT id, dataset, period FROM meta.transform_log WHERE status = 'PENDING' OR (status = 'FAIL' AND retry_count < 2)")
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
