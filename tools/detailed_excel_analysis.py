import pandas as pd
from datetime import datetime

print('='*80)
print('DETAILED EXCEL FILE ANALYSIS - CapacityUpdate.xlsx')
print('='*80)

df = pd.read_excel('CapacityUpdate.xlsx', sheet_name='Monthly')

print(f'\n📊 Total Rows: {df.shape[0]}')
print(f'📊 Total Columns: {df.shape[1]}')
print(f'📊 Columns: {df.columns.tolist()}')

print('\n' + '='*80)
print('MONTH SECTIONS DETECTED:')
print('='*80)

current_month = None
month_sections = []

for idx, row in df.iterrows():
    emp_id_val = str(row['Emp Id']).strip() if not pd.isna(row['Emp Id']) else ''
    
    if emp_id_val == 'Emp Id':
        # This is a header row
        month_col = df.columns[2]
        month_header = str(row[month_col]).strip() if not pd.isna(row[month_col]) else ''
        
        month_mapping = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        
        for month_name, month_num in month_mapping.items():
            if month_name in month_header.lower():
                current_month = month_name.title()
                month_sections.append({
                    'row': idx,
                    'month': current_month,
                    'header': month_header
                })
                break

print(f'\nFound {len(month_sections)} month sections:\n')
for section in month_sections:
    print(f"  Row {section['row']:3d}: {section['month']:10s} - {section['header']}")

print('\n' + '='*80)
print('DATA ROWS BY MONTH:')
print('='*80)

current_month = None
today = datetime.now().date()

for idx, row in df.iterrows():
    emp_id_val = str(row['Emp Id']).strip() if not pd.isna(row['Emp Id']) else ''
    
    if emp_id_val == 'Emp Id':
        month_col = df.columns[2]
        month_header = str(row[month_col]).strip() if not pd.isna(row[month_col]) else ''
        
        month_mapping = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        
        for month_name, month_num in month_mapping.items():
            if month_name in month_header.lower():
                current_month = month_name.title()
                print(f'\n--- {current_month.upper()} 2025 ---')
                break
        continue
    
    if emp_id_val and emp_id_val.isdigit():
        emp_name = str(row['Emp Name']).strip() if not pd.isna(row['Emp Name']) else ''
        leave_col = df.columns[2]
        leave_data = str(row[leave_col]).strip() if not pd.isna(row[leave_col]) else ''
        
        if leave_data and leave_data not in ['nan', '']:
            print(f"  {emp_name:30s}: {leave_data}")

print('\n' + '='*80)
print('CURRENT DATE ANALYSIS:')
print('='*80)
print(f'\nToday: {today}')
print(f'Current Month: {today.month} ({today.strftime("%B")})')
print(f'Current Year: {today.year}')
print('\nMonths in Excel:')
for section in month_sections:
    month_name = section['month']
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    month_num = month_mapping.get(month_name, 0)
    
    if month_num < today.month:
        status = '❌ PAST (will be filtered out)'
    elif month_num == today.month:
        status = '✅ CURRENT (will be used)'
    else:
        status = '✅ FUTURE (will be used)'
    
    print(f'  {month_name:10s} (Month {month_num:2d}): {status}')

