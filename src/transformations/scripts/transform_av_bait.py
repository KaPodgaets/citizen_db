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
        # 1. Check is there already dataset
        find_old_versions_sql = text("""
            SELECT id FROM meta.dataset_version
            WHERE dataset_name = :dataset AND is_active = 1
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
            INSERT INTO meta.dataset_version (dataset_name, period, created_at, is_active)
            VALUES (:dataset, :period, :now, 1)
        """)
        conn.execute(insert_version_sql, {"dataset": dataset, "period": period, "now": datetime.now()})
        

        # 3. delete data from core table
        
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
        run_update_fake_id_table(conn)


def run_update_fake_id_table(conn):
    """We need this table to be related to HAMAL applicaiton which uses only FID values to identify citizens"""
    print('[LOG][update_fake_ids]: executing procedure `fid_update`')
    with open('sql/procedures/fid_update.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    sql_query = text(sql)
    try:
        conn.execute(sql_query)
        print('[LOG][update_fake_ids]: `table fake_id was updated succesfully`')
    except Exception as e:
        raise Exception(f'[ERR][update_fake_ids] : {e}')

def save_fake_id_table_as_snapshot(conn):
    """Saving xlsx file as snapshot to backfill dictionary in case of full restart the system"""
    import pandas as pd
    from datetime import datetime
    import os
    print('[LOG][fake_id_snapshot]: start snapshoting the table `fid_update`')
    sql_query = text('''
                    select 
                        citizen_id
                        , fake_citizen_id
                    from core.fake_id
                ''')
    try:
        df = pd.read_sql(sql_query, conn)
        # Ensure the directory exists
        os.makedirs('data/snapshots/', exist_ok=True)
        today_str = datetime.today().strftime('%Y-%m-%d')
        file_path = f'data/snapshots/fake_id-{today_str}.xlsx'
        df.to_excel(file_path, index=False)
        print(f'[LOG][fake_id_snapshot]: Saved snapshot to {file_path}')
    except Exception as e:
        raise Exception(f'[ERR][fake_id_snapshot] : {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform data from stage to core for a specific dataset and period using a rebuild strategy.")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name to process (e.g., 'av_bait').")
    parser.add_argument("--period", type=str, required=True, help="Period to process (e.g., '2025-07').")
    args = parser.parse_args()
    main(dataset=args.dataset, period=args.period) 