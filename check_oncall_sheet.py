"""Check if On Call Schedules sheet exists and show its data"""
import pandas as pd

xl = pd.ExcelFile('CapacityUpdate.xlsx')
print('Available sheets:')
for sheet in xl.sheet_names:
    print(f'  - {sheet}')

print()

if 'On Call Schedules' in xl.sheet_names:
    df = pd.read_excel('CapacityUpdate.xlsx', sheet_name='On Call Schedules')
    print('✅ On Call Schedules sheet found!')
    print(f'Shape: {df.shape}')
    print()
    print('Columns:')
    print(df.columns.tolist())
    print()
    print('Data:')
    print(df.to_string(index=False))
else:
    print('❌ On Call Schedules sheet NOT found!')

