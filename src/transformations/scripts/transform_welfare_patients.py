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

        # WARNING! it's important here to modify tables exactly as in ddl sql script is
        metadata_cols_to_drop = ['_data_period', '_source_parquet_path']
        existing_cols_to_drop = [col for col in metadata_cols_to_drop if col in staging_df.columns]
        if existing_cols_to_drop:
            staging_df_to_core = staging_df.drop(columns=existing_cols_to_drop)

        phone_cols_to_drop = ['mobile_phone_number', 'home_phone_number']
        existing_cols_to_drop = [col for col in phone_cols_to_drop if col in staging_df.columns]
        if existing_cols_to_drop:
            staging_df_to_core = staging_df_to_core.drop(columns=existing_cols_to_drop)
        
        staging_df_to_core['is_current'] = 1
        
        # Transform data types to match core table schema
        # Convert FLOAT columns to NVARCHAR for core table compatibility
        float_columns_to_convert = ['street_code', 'building_number', 'apartment_number']
        for col in float_columns_to_convert:
            if col in staging_df_to_core.columns:
                # Convert FLOAT to string, handling NaN values
                staging_df_to_core[col] = staging_df_to_core[col].astype(str)
                # Replace 'nan' strings with None for NULL values
                staging_df_to_core[col] = staging_df_to_core[col].replace('nan', None)
        
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