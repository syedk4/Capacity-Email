import pandas as pd

print('📊 EXCEL FILE SHEET ANALYSIS')
print('='*70)
print('File: CapacityUpdate.xlsx')
print()

# Check default sheet (first sheet)
df_default = pd.read_excel('CapacityUpdate.xlsx')
print('🔍 DEFAULT SHEET (what the application currently reads):')
print('   Sheet: Monthly (first sheet - default when no sheet_name specified)')
print(f'   Shape: {df_default.shape}')
print(f'   Columns: {list(df_default.columns)}')
print()

# Show all sheets
excel_file = pd.ExcelFile('CapacityUpdate.xlsx')
print('📋 ALL SHEETS IN FILE:')
print()

for i, sheet_name in enumerate(excel_file.sheet_names, 1):
    df = pd.read_excel('CapacityUpdate.xlsx', sheet_name=sheet_name)
    print(f'{i}. Sheet: "{sheet_name}"')
    print(f'   Shape: {df.shape} (rows: {df.shape[0]}, columns: {df.shape[1]})')
    print(f'   Columns: {list(df.columns)}')
    if df.shape[0] > 0:
        print(f'   First few rows:')
        print(df.head(3).to_string(index=False))
    print()
    print('-'*70)
    print()

