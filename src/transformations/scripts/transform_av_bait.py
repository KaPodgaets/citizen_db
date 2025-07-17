import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pandas as pd
import argparse
from sqlalchemy import MetaData, Table, text

from src.transformations.error_handling import global_error_handler
from src.utils.db import get_engine
from src.utils.metadata_helpers import set_new_active_dataset_version
from src.utils.fake_id_utils import run_update_fake_id_table, save_fake_id_table_as_snapshot

@global_error_handler('transform')
def main(dataset: str, period: str, version: int):
    engine = get_engine()
    metadata = MetaData()
    core_schema = "core"

    with engine.begin() as conn:
        # 1. Change data in meta table dataset_version (new record with is_active = 1)
        set_new_active_dataset_version(dataset, period, version)
        
        # 2. delete data from core table
        try:
            core_table = Table(dataset, metadata, schema=core_schema, autoload_with=conn)
            delete_stmt = core_table.delete()
            conn.execute(delete_stmt)
            print("Deleted data for from core table")
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
        
        staging_df['is_current'] = 1
        
        staging_df.to_sql(name=dataset, con=conn, schema=core_schema, if_exists='append', index=False)
        print(f"Inserted {len(staging_df)} records into {core_schema}.{dataset}")

        # update fake_citizen_id table
        run_update_fake_id_table()
        save_fake_id_table_as_snapshot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform data from stage to core for a specific dataset and period using a rebuild strategy.")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name to process (e.g., 'av_bait').")
    parser.add_argument("--period", type=str, required=True, help="Period to process (e.g., '2025-07').")
    parser.add_argument("--version", type=int, required=True, help="Version to process (should be just int, e.g. 1)")
    args = parser.parse_args()
    main(dataset=args.dataset, period=args.period, version=args.version) 