import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pandas as pd
from sqlalchemy import MetaData, Table, text
import argparse

from src.transformations.error_handling import global_error_handler
from src.utils.db import get_engine
from src.utils.phone_validation import process_israeli_phone_numbers
from src.utils.metadata_helpers import set_new_active_dataset_version

@global_error_handler('transform')
def main(dataset: str, period: str, version: int):
    print(f"[transform] start task for dataset: {dataset}")
    engine = get_engine()
    metadata = MetaData()
    core_schema = "core"

    with engine.begin() as conn:
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
        
        # Convert is_left_the_city from string to boolean and filter out rows where it is True
        if 'is_left_the_city' in staging_df.columns:
            # Convert to boolean: treat 'true', 'True', '1', 1 as True; else False
            staging_df['is_left_the_city'] = staging_df['is_left_the_city'].astype(str).str.lower().isin(['כן', '1'])
            # Drop rows where is_left_the_city is True
            staging_df = staging_df[~staging_df['is_left_the_city']]
        
        # Drop the records with duplicated value in column 'citizen_id' and print in terminal the warning about it
        if 'citizen_id' in staging_df.columns:
            duplicated = staging_df[staging_df.duplicated('citizen_id', keep=False)]
            if not duplicated.empty:
                print(f"Warning: Dropping {duplicated.shape[0]} records with duplicated citizen_id values.")
                # Optionally, print the duplicated citizen_ids:
                print("Duplicated citizen_ids:", duplicated['citizen_id'].unique())
            staging_df = staging_df.drop_duplicates(subset=['citizen_id'], keep='first')
        
        # WARNING! it's important here to modify tables exactly as in ddl sql script is
        metadata_cols_to_drop = ['_data_period', '_source_parquet_path', 'is_left_the_city']
        existing_cols_to_drop = [col for col in metadata_cols_to_drop if col in staging_df.columns]
        if existing_cols_to_drop:
            staging_df_to_core = staging_df.drop(columns=existing_cols_to_drop)

        phone_cols_to_drop = ['citizen_phone_number_1', 'citizen_phone_number_2']
        existing_cols_to_drop = [col for col in phone_cols_to_drop if col in staging_df.columns]
        if existing_cols_to_drop:
            staging_df_to_core = staging_df_to_core.drop(columns=existing_cols_to_drop)
        
        staging_df_to_core['is_current'] = 1
        
        # 1. Change data in meta table dataset_version (new record with is_active = 1)
        set_new_active_dataset_version(dataset, period, version)
        
        # 2. delete data from core table
        try:
            core_table = Table(dataset, metadata, schema=core_schema, autoload_with=conn)
            delete_stmt = core_table.delete()
            conn.execute(delete_stmt)
            print("[transform] Deleted data for from core table")
        except Exception as e:
            print(f"Could not delete old data, perhaps schema not updated yet? Error: {e}")

       
        staging_df_to_core.to_sql(name=dataset, con=conn, schema=core_schema, if_exists='append', index=False)
        print(f"Inserted {len(staging_df)} records into {core_schema}.{dataset}")

        # Process phone numbers and add to core.phone_numbers (only citizen_id and phones)
        selected_columns = ['citizen_id'] + phone_cols_to_drop
        available_columns = [col for col in selected_columns if col in staging_df.columns]
        phone_df = staging_df[available_columns]
        
        
        # Transform to citizen_id, phone_number format by melting the DataFrame
        if not phone_df.empty and len(available_columns) > 1:  # Check if we have phone columns
            # Melt the DataFrame to convert phone columns to rows
            phone_df = phone_df.melt(
                id_vars=['citizen_id'], 
                value_vars=phone_cols_to_drop,
                var_name='phone_type', 
                value_name='phone_number'
            )

            # Remove rows where phone_number is null/empty
            phone_df = phone_df.dropna(subset=['phone_number'])
            phone_df = phone_df[phone_df['phone_number'].astype(str).str.strip() != '']
            
            # Apply Israeli phone number validation and formatting using utility function
            phone_df = process_israeli_phone_numbers(phone_df)
            
            
            print(f"Created phone DataFrame with {len(phone_df)} valid Israeli phone records")
        else:
            print("No phone columns found or DataFrame is empty")
            return
        
        phone_df['dataset'] = dataset


        # clean core.phone_numbers from previous data
        delete_query_sql = text("""
            DELETE FROM core.phone_numbers WHERE dataset = :dataset
        """)
        conn.execute(delete_query_sql, {"dataset": dataset})
        # append new data
        phone_df.to_sql(name="phone_numbers", con=conn, schema=core_schema, if_exists='append', index=False)

        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform data from stage to core for a specific dataset and period using a rebuild strategy.")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name to process (e.g., 'av_bait').")
    parser.add_argument("--period", type=str, required=True, help="Period to process (e.g., '2025-07').")
    parser.add_argument("--version", type=int, required=True, help="Version to process (should be just int, e.g. 1)")
    args = parser.parse_args()
    main(dataset=args.dataset, period=args.period, version=args.version) 