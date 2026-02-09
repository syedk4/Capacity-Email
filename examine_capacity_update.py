import pandas as pd

file_path = 'CapacityUpdate.xlsx'

# Read all sheets
xl = pd.ExcelFile(file_path)
print("=" * 80)
print(f"FILE: {file_path}")
print("=" * 80)
print(f"\nSheet Names: {xl.sheet_names}\n")

# Examine each sheet
for sheet in xl.sheet_names:
    print("\n" + "=" * 80)
    print(f"SHEET: {sheet}")
    print("=" * 80)
    
    df = pd.read_excel(file_path, sheet_name=sheet)
    
    print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"\nColumns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\nFirst 15 rows:")
    print(df.head(15).to_string())
    
    print("\n")

