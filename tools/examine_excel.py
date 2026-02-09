import pandas as pd

print('='*70)
print('EXAMINING EXCEL FILE - CapacityUpdate.xlsx')
print('='*70)

# Read the Monthly sheet
df = pd.read_excel('CapacityUpdate.xlsx', sheet_name='Monthly')

print('\n📊 COLUMN NAMES:')
print(df.columns.tolist())

print('\n📊 DATA SHAPE:')
print(f'Rows: {df.shape[0]}, Columns: {df.shape[1]}')

print('\n📊 FIRST 15 ROWS (RAW DATA):')
print(df.head(15).to_string())

print('\n📊 ALL COLUMN DATA:')
for col in df.columns:
    print(f'\n--- Column: {col} ---')
    print(df[col].dropna().head(15).to_string(index=False))

