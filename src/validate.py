import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import pandas as pd
import yaml
from sqlalchemy import text
from datetime import datetime
from src.utils.db import get_engine
from src.utils.yaml_parser import parse_contract, get_closest_mapping_before
from src.transformations.error_handling import global_error_handler
from pandera.errors import SchemaError

@global_error_handler('validate')
def main(file_id):
    engine = get_engine()
    with engine.begin() as conn:
        # Get file info from ingestion_log
        result = conn.execute(text("SELECT file_name, dataset, period FROM meta.ingestion_log WHERE id = :id"), {"id": file_id})
        row = result.fetchone()
        if not row:
            print(f"No file found for file_id {file_id}")
            return
        file_name, dataset, period = row
        file_path = os.path.join("data/land", file_name)
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist")
            return
        
        # Load contract config
        with open("datasets_config.yml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        contract_path = config[dataset]['contract']
        # Load and map columns based on file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.csv':
            # Read all columns as strings initially
            df = pd.read_csv(file_path, dtype=str)
        elif file_extension == '.xlsx':
            # Read all columns as strings initially
            df = pd.read_excel(file_path, dtype=str)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Only .csv and .xlsx files are supported.")

        # read yaml file to get contracts as raw string
        with open(contract_path, encoding="utf-8") as f:
            raw_contract = yaml.safe_load(f)

        period_as_date = datetime.strptime(period + "-01", "%Y-%m-%d").date()
        contract = parse_contract(raw_contract)
        contract_version = get_closest_mapping_before(contract, period_as_date)

        # Rename columns according to contract
        df = df.rename(columns=contract_version.mapping)

        # Import the correct schema
        schema_module = f"schemas.{dataset}_schema"
        schema = __import__(schema_module, fromlist=[f"{dataset}_schema"]).__dict__[f"{dataset}_schema"]
        
        try:
            # Cast columns to proper data types according to schema
            validated_df = df.copy()

            for column_name, column_schema in schema.columns.items():
                if column_name in validated_df.columns:
                    try:
                        # Get the expected data type from schema
                        expected_dtype = column_schema.dtype
                        
                        # Handle different Pandera data types
                        if str(expected_dtype) == 'Int' or str(expected_dtype) == 'int64':
                            # Convert to int, handling NaN values
                            validated_df[column_name] = pd.to_numeric(validated_df[column_name], errors='coerce').astype('Int64')
                        elif str(expected_dtype) == 'Float64' or str(expected_dtype) == 'float64':
                            # Convert to float
                            validated_df[column_name] = pd.to_numeric(validated_df[column_name], errors='coerce')
                        elif str(expected_dtype) == 'String' or str(expected_dtype) == 'object':
                            # Ensure string type
                            validated_df[column_name] = validated_df[column_name].astype(str)
                        elif str(expected_dtype) == 'Bool' or str(expected_dtype) == 'boolean':
                            # check that there is no values except true and false (in different variations)
                            raw_values = validated_df[column_name].dropna().unique()
                            unexpected = set(raw_values) - {'true', 'false','True', 'False', 'TRUE', 'FALSE', '1', '0'}
                            if unexpected:
                                print(f"Warning: Unexpected boolean values in '{column_name}': {unexpected}")
                            
                            # Convert to boolean
                            validated_df[column_name] = (validated_df[column_name]
                                .astype(str)
                                .str.strip()  # remove leading/trailing whitespace
                                .str.replace(r'_x000D_', '', regex=True)  # remove Excel control codes
                                .str.lower()  # normalize case
                                .map({
                                    'true': True, 'false': False,
                                    '1': True, '0': False,
                                    }).astype('boolean')
                            )
                        else:
                            # For other types, try to convert using pandas
                            validated_df[column_name] = validated_df[column_name].astype(str(expected_dtype))
                            
                        # print(f"Successfully cast column '{column_name}' to {expected_dtype}")
                        
                    except Exception as cast_error:
                        raise ValueError(f"Failed to cast column '{column_name}' to expected type {expected_dtype}: {cast_error}")
                else:
                    print(f"Warning: Column '{column_name}' from schema not found in data")
            
            # Validate the DataFrame with the schema
            validated_df = schema.validate(validated_df)
            
            # Only keep columns defined in the schema
            columns_to_save = list(schema.columns.keys())
            validated_df = validated_df[columns_to_save]
            
            os.makedirs("data/stage/cleaned", exist_ok=True)
            # Remove .xlsx extension from file_name before saving as .parquet
            base_file_name = os.path.splitext(file_name)[0]
            parquet_path = os.path.join("data/stage/cleaned", base_file_name + ".parquet")
            
            # remove _x00D in the end of strings (from excel)
            validated_df = validated_df.replace({'_x000D_': ''}, regex=True)
            
            # save to parquet
            validated_df.to_parquet(parquet_path)
            status = "PASS"
            error_report = None
            print(f"Validation passed. Parquet written to {parquet_path}")
            
        except (SchemaError, ValueError) as e:
            status = "FAIL"
            error_report = str(e)
            print(f"Validation failed: {e}")
        # Log result
        conn.execute(text("""
            INSERT INTO meta.validation_log (file_id, status, error_report)
            VALUES (:file_id, :status, :error_report)
        """), {"file_id": file_id, "status": status, "error_report": error_report})

def check_unique_values_of_boolean_col(raw_values: numpy.ndarray, column_name: str) -> None:
    
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a landed file by file_id.")
    parser.add_argument("--file-id", required=True, type=int, help="File ID from ingestion_log")
    args = parser.parse_args()
    main(args.file_id)
