import pandas as pd
import os

excel_path = r'C:\Users\slatheef\Ashley Furniture Industries, Inc\IT - Finance - India Finance Team Daily Updates\2026- India Finance team Daily work status.xlsx'

if os.path.exists(excel_path):
    df = pd.read_excel(excel_path, sheet_name='Leave plans')
    
    print('=' * 100)
    print('JANUARY SECTION FROM EXCEL')
    print('=' * 100)
    
    # Print rows 3-9 (January section)
    for idx in range(3, 10):
        if idx < len(df):
            row = df.iloc[idx]
            emp_id = row.iloc[0]
            emp_name = row.iloc[1]
            planned_leave = row.iloc[2]
            print(f'Row {idx}: {emp_id} | {emp_name} | Planned Leave: {repr(planned_leave)}')
    
    print('\n' + '=' * 100)
    print('FEBRUARY SECTION FROM EXCEL')
    print('=' * 100)
    
    # Print rows 11-19 (February section)
    for idx in range(11, 20):
        if idx < len(df):
            row = df.iloc[idx]
            emp_id = row.iloc[0]
            emp_name = row.iloc[1]
            planned_leave = row.iloc[2]
            print(f'Row {idx}: {emp_id} | {emp_name} | Planned Leave: {repr(planned_leave)}')
else:
    print('File not found')

