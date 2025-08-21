import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import argparse

import pandas as pd
from sqlalchemy import text

from src.transformations.error_handling import global_error_handler
from src.utils.db import get_engine
from src.utils.metadata_helpers import set_new_active_dataset_version


@global_error_handler('transform')
def main(dataset: str, period: str, version: int):
    print(f"[transform] start task for dataset: {dataset}")
    engine = get_engine()
    core_schema = "core"

    with engine.begin() as conn:
        # 2. Load from stage, add version id, insert into core
        staging_table_name = dataset
        stage_df = pd.read_sql(
            text(
                f"SELECT * FROM stage.{staging_table_name} WHERE _data_period = :period"
            ),
            conn,
            params={"period": period}
        )

        if stage_df.empty:
            print(
                f"[WAR]: No data found in stage.{staging_table_name}" + 
                f" for period {period}. Nothing to transform."
            )
            return
        
        # Step 2: Load current core data (only current)
        core_df = pd.read_sql(f"SELECT * FROM {core_schema}.{dataset}", conn)

        # 3. Drop duplicates if any (based on citizen_fid + file_name)
        stage_df['key'] = stage_df['citizen_fid'].astype(str) + '|' + stage_df['file_name']  # noqa: E501
        core_df['key'] = core_df['citizen_fid'].astype(str) + '|' + core_df['file_name']

        # 4. Filter out replaced keys from core
        incoming_keys = set(stage_df['key'])
        remaining_core_df = core_df[~core_df['key'].isin(incoming_keys)]

        # 5. Prepare new rows
        new_rows = stage_df.copy()

        new_rows['is_current'] = 0  # will compute next

        # 6. Combine remaining old records and new incoming ones
        full_df = pd.concat([remaining_core_df, new_rows], ignore_index=True)

        # 7. Identify current records: latest period per citizen_fid
        full_df['_data_period'] = pd.to_datetime(full_df['_data_period'], format='%Y-%m')  # noqa: E501
        full_df.sort_values(['citizen_fid', '_data_period'], inplace=True)
        full_df['is_current'] = 0  # reset

        latest_period_idx = full_df.groupby('citizen_fid')['_data_period'].idxmax()
        full_df.loc[latest_period_idx, 'is_current'] = 1

        # 8. Drop helper column(s)
        full_df = full_df.drop(columns=['key'])
       
        # 9. Delete all from core and reload
        conn.execute(text("DELETE FROM core.hamal"))
        
        
        # WARNING! it's important here to modify tables exactly as in ddl sql script is
        metadata_cols_to_drop = ['_data_period', '_source_parquet_path']
        existing_cols_to_drop = [col for col in metadata_cols_to_drop if col in stage_df.columns]  # noqa: E501
        if existing_cols_to_drop:
            transformed_df_to_core = full_df.drop(columns=existing_cols_to_drop)

        try:
            transformed_df_to_core.to_sql(name='hamal', con=conn, schema='core', if_exists='append', index=False)  # noqa: E501
        except Exception as e:
            raise Exception(f'[ERR]: Error while inserting data into core.hamal. {e}')

        print(f"[LOG]: Transformed hamal table with {len(transformed_df_to_core)} rows; {len(latest_period_idx)} marked as is_current = 1")  # noqa: E501
        
        # 1. Change data in meta table dataset_version (new record with is_active = 1)
        set_new_active_dataset_version(dataset, period, version)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform data from stage to core for a specific dataset and period using a rebuild strategy.")  # noqa: E501
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name to process (e.g., 'av_bait').")  # noqa: E501
    parser.add_argument("--period", type=str, required=True, help="Period to process (e.g., '2025-07').")  # noqa: E501
    parser.add_argument("--version", type=int, required=True, help="Version to process (should be just int, e.g. 1)")  # noqa: E501
    args = parser.parse_args()
    main(dataset=args.dataset, period=args.period, version=args.version) 