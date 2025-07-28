import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pandas as pd
from sqlalchemy import text

from src.utils.db import get_engine
from src.utils.fake_id_utils import (
    run_update_fake_id_table,
    save_fake_id_table_as_snapshot,
)
from src.utils.metadata_helpers import set_new_active_dataset_version


def delete_from_core_table(
        core_schema: str,
        dataset: str,
        period: str,
        version: int) -> None:
    engine = get_engine()

    with engine.begin() as conn:
        try:
            conn.execute(text(f"DELETE FROM {core_schema}.{dataset}"))
            print("Deleted data for from core table")
        except Exception as e:
            print(
                f"Could not delete old data, perhaps schema not updated yet? Error: {e}"
            )


def main(dataset: str, period: str, version: int):
    core_schema = "core"

    # 3. Load from stage
    engine = get_engine()
    with engine.begin() as conn:
        staging_table_name = dataset
        try:
            staging_df = pd.read_sql(
                text(f"SELECT * FROM stage.{staging_table_name} WHERE _data_period = :period"),
                conn,
                params={"period": period}
            )
        except Exception:
            print(f"""[ERROR] Can not read sql table stage.{dataset}""")

        if staging_df.empty:
            print(f"No data found in stage.{staging_table_name} for period {period}. Nothing to transform.")
            return

    cols_to_drop = ['_data_period', '_source_parquet_path']
    existing_cols_to_drop = [col for col in cols_to_drop if col in staging_df.columns]
    if existing_cols_to_drop:
        pre_core_df = staging_df.drop(columns=existing_cols_to_drop)
    
    pre_core_df['is_current'] = 1

    # Add is_living_alone: 1 if family_index_number is unique, else 0
    family_counts = pre_core_df['family_index_number'].value_counts()
    pre_core_df['is_living_alone'] = pre_core_df['family_index_number'].map(lambda x: 1 if family_counts[x] == 1 else 0)

    # Add elders_pair: 1 if family_index_number group has exactly 2 records and both age >= 65, else 0
    def elders_pair_logic(df):
        group = df.groupby('family_index_number')
        # Boolean Series: True if group has 2 records and both age >= 65
        elders_pair_mask = group['age'].transform(lambda ages: int((len(ages) == 2) and all(ages >= 70)))
        return elders_pair_mask
    pre_core_df['is_elder_pair'] = elders_pair_logic(pre_core_df)
    
    # 1. Change data in meta table dataset_version (new record with is_active = 1)
    set_new_active_dataset_version(dataset, period, version)

    # 2. delete data from core table
    delete_from_core_table(core_schema, dataset, period, version)
    
    # staging_df.to_sql(name=dataset, con=conn, schema=core_schema, if_exists='append', index=False)
    pre_core_df.to_sql(dataset, engine, schema=core_schema, if_exists='append', index=False)
    print(f"Inserted {len(pre_core_df)} records into {core_schema}.{dataset}")

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
    # main(dataset='av_bait', period='2025-06', version=2)
    