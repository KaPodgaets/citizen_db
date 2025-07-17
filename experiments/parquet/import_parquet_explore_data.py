import pandas as pd
from pathlib import Path

def explore_parquet_files():
    """
    Import and explore parquet files from data/stage/cleaned folder
    """
    # Path to the cleaned parquet files
    parquet_dir = Path("data/stage/cleaned")
    
    # Check if directory exists
    if not parquet_dir.exists():
        print(f"Directory {parquet_dir} does not exist!")
        return
    
    # Find all parquet files
    parquet_files = list(parquet_dir.glob("*.parquet"))
    
    if not parquet_files:
        print(f"No parquet files found in {parquet_dir}")
        return
    
    print(f"Found {len(parquet_files)} parquet file(s):")
    for file in parquet_files:
        print(f"  - {file.name}")
    
    # Explore each parquet file
    for parquet_file in parquet_files:
        print(f"\n{'='*60}")
        print(f"EXPLORING: {parquet_file.name}")
        print(f"{'='*60}")
        
        try:
            # Read the parquet file
            df = pd.read_parquet(parquet_file)
            
            # Basic information
            print("\n📊 BASIC INFO:")
            print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            # Column information
            print("\n📋 COLUMNS:")
            for i, col in enumerate(df.columns, 1):
                dtype = df[col].dtype
                null_count = df[col].isnull().sum()
                null_pct = (null_count / len(df)) * 100
                print(f"  {i:2d}. {col:<20} | {str(dtype):<15} | {null_count:>4} nulls ({null_pct:5.1f}%)")
            
            # Data types summary
            print("\n🔍 DATA TYPES SUMMARY:")
            dtype_counts = df.dtypes.value_counts()
            for dtype, count in dtype_counts.items():
                print(f"  {dtype}: {count} columns")
            
            # Sample data
            print("\n📝 SAMPLE DATA (first 5 rows):")
            print(df.head().to_string())
            
            # Statistical summary for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                print("\n📈 NUMERIC COLUMNS SUMMARY:")
                print(df[numeric_cols].describe())
            
            # Unique values for categorical columns (first 10 unique values)
            categorical_cols = df.select_dtypes(include=['object', 'string']).columns
            if len(categorical_cols) > 0:
                print("\n🏷️  CATEGORICAL COLUMNS (first 10 unique values):")
                for col in categorical_cols:
                    unique_vals = df[col].dropna().unique()
                    print(f"  {col}: {len(unique_vals)} unique values")
                    if len(unique_vals) <= 10:
                        print(f"    Values: {list(unique_vals)}")
                    else:
                        print(f"    First 10: {list(unique_vals[:10])}")
            
            # Check for duplicates
            duplicates = df.duplicated().sum()
            print(f"\n🔄 DUPLICATES: {duplicates} duplicate rows found")
            
            # File size information
            file_size = parquet_file.stat().st_size
            print(f"\n💾 FILE SIZE: {file_size / 1024:.2f} KB")
            
        except Exception as e:
            print(f"❌ Error reading {parquet_file.name}: {e}")

def explore_specific_parquet_file(filename):
    """
    Explore a specific parquet file by name
    """
    parquet_file = Path("data/stage/cleaned") / filename
    
    if not parquet_file.exists():
        print(f"File {parquet_file} does not exist!")
        return
    
    print(f"Exploring specific file: {parquet_file}")
    explore_parquet_files()  # This will find and explore the specific file

if __name__ == "__main__":
    print("🔍 PARQUET FILE EXPLORER")
    print("=" * 60)
    
    # Explore all parquet files
    explore_parquet_files()
    
    # Example: To explore a specific file, uncomment and modify the line below:
    # explore_specific_parquet_file("your_file_name.parquet")
