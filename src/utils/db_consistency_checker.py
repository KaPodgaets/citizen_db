import yaml
from sqlalchemy import text
from src.utils.db import get_engine


def check_db_consistency(dataset_config_path='datasets_config.yml'):
    engine = get_engine()
    notify = False
    with engine.connect() as conn:
        # 1. Check that all dataset_version meta table contain only datasets that are mentioned in dataset_config.yml
        with open(dataset_config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        config_datasets = set(config.keys())
        db_datasets = set(row[0] for row in conn.execute(text("SELECT DISTINCT dataset_name FROM meta.dataset_version")).fetchall())
        extra_datasets = db_datasets - config_datasets
        if extra_datasets:
            print(f"[CONSISTENCY WARNING]: The following datasets are in meta.dataset_version but not in {dataset_config_path}: {extra_datasets}")
            notify = True

        # 2. Check that there is only 1 record per dataset with is_active = 1 in dataset_version meta table
        multi_active = conn.execute(text("""
            SELECT dataset_name, COUNT(*)
            FROM meta.dataset_version
            WHERE is_active = 1
            GROUP BY dataset_name
            HAVING COUNT(*) > 1
        """)).fetchall()
        if multi_active:
            print("[CONSISTENCY WARNING]: More than one active version found for datasets:")
            for dataset, count in multi_active:
                print(f"  - {dataset}: {count} active versions")
            notify = True

        # 3. Check that there is only 1 'INGESTED' file per dataset+period in ingestion_log meta table
        multi_ingested = conn.execute(text("""
            SELECT dataset_name, period, COUNT(*)
            FROM meta.ingestion_log
            WHERE status = 'INGESTED'
            GROUP BY dataset_name, period
            HAVING COUNT(*) > 1
        """)).fetchall()
        if multi_ingested:
            print("[CONSISTENCY WARNING]: More than one 'INGESTED' file found for dataset+period:")
            for dataset, period, count in multi_ingested:
                print(f"  - {dataset} / {period}: {count} ingested files")
            notify = True

    if notify:
        print("[ACTION REQUIRED]: Database consistency issues detected. Please contact a developer.")
    else:
        print("[CONSISTENCY CHECK]: All checks passed.")


if __name__ == "__main__":
    check_db_consistency()

# Suggestions for additional checks:
# - Check that all datasets in dataset_config.yml have at least one entry in meta.dataset_version
# - Check that all 'PASS' records in validation_log have a corresponding 'INGESTED' file in ingestion_log
# - Check that for each dataset+period, the highest version is marked as is_active in dataset_version
# - Check for orphaned records (e.g., validation_log referencing non-existent ingestion_log records)
# - Check that all required tables exist in the database 