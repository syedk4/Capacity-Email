import pandas as pd
from datetime import datetime, timedelta

def read_capacity_data():
    """
    Read your Excel file and display its structure
    """
    try:
        # Update this path to your actual Excel file
        file_path = "CapacityUpdate.xlsx"  # I see this file in your explorer
        
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        print("✓ File read successfully!")
        print(f"Shape: {df.shape} (rows: {df.shape[0]}, columns: {df.shape[1]})")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 5 rows:")
        print(df.head())
        
        # Show data types
        print(f"\nData types:")
        print(df.dtypes)
        
        return df
        
    except FileNotFoundError:
        print("❌ File not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

if __name__ == "__main__":
    data = read_capacity_data()
