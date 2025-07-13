import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pandas as pd
from sqlalchemy import MetaData, Table, text
from src.transformations.error_handling import global_error_handler
from src.utils.db import get_engine
import argparse
from datetime import datetime


@global_error_handler('transform')
def main(dataset: str, period: str):
    engine = get_engine()
    metadata = MetaData()
    core_schema = "core"

    with engine.begin() as conn:
        # 1. Find previous version IDs for this dataset and period to delete them later
        find_old_versions_sql = text("""
            SELECT id FROM meta.dataset_version
            WHERE dataset_name = :dataset AND period = :period
        """)
        old_version_ids_result = conn.execute(find_old_versions_sql, {"dataset": dataset, "period": period}).fetchall()
        old_version_ids = [row[0] for row in old_version_ids_result]

        # 2. Create a new version record and get its ID
        insert_version_sql = text("""
            INSERT INTO meta.dataset_version (dataset_name, period, load_timestamp)
            VALUES (:dataset, :period, :now)
        """)
        conn.execute(insert_version_sql, {"dataset": dataset, "period": period, "now": datetime.now()})
        
        get_new_version_id_sql = text("SELECT MAX(id) FROM meta.dataset_version WHERE dataset_name = :dataset AND period = :period")
        new_version_id = conn.execute(get_new_version_id_sql, {"dataset": dataset, "period": period}).scalar()

        # 3. If old versions exist, delete their data from the core table
        if old_version_ids:
            try:
                core_table = Table(dataset, metadata, schema=core_schema, autoload_with=conn)
                delete_stmt = core_table.delete().where(core_table.c.dataset_version_id.in_(old_version_ids))
                conn.execute(delete_stmt)
                print(f"Deleted data for old versions: {old_version_ids}")
            except Exception as e:
                print(f"Could not delete old data, perhaps schema not updated yet? Error: {e}")

        # 4. Load from stage, add version id, insert into core
        staging_table_name = dataset
        staging_df = pd.read_sql(
            text(f"SELECT * FROM stage.{staging_table_name} WHERE _data_period = :period"),
            conn,
            params={"period": period}
        )

        if staging_df.empty:
            print(f"No data found in stage.{staging_table_name} for period {period}. Nothing to transform.")
            return

        cols_to_drop = ['_data_period', '_source_parquet_path']
        existing_cols_to_drop = [col for col in cols_to_drop if col in staging_df.columns]
        if existing_cols_to_drop:
            staging_df = staging_df.drop(columns=existing_cols_to_drop)
        
        staging_df['dataset_version_id'] = new_version_id
        
        staging_df.to_sql(name=dataset, con=conn, schema=core_schema, if_exists='append', index=False)
        print(f"Inserted {len(staging_df)} records into {core_schema}.{dataset} with version id {new_version_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform data from stage to core for a specific dataset and period using a rebuild strategy.")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name to process (e.g., 'new_immigrants').")
    parser.add_argument("--period", type=str, required=True, help="Period to process (e.g., '2025-07').")
    args = parser.parse_args()
    main(dataset=args.dataset, period=args.period) 