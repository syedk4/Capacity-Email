"""Check if employee locations are being read correctly"""
from sprint_capacity_app import SprintCapacityCalculator, ExcelDataParser

# Initialize calculator
calculator = SprintCapacityCalculator('config.json')

# Initialize parser
parser = ExcelDataParser(calculator)

# Parse Excel file
excel_path = 'CapacityUpdate.xlsx'
employees, leave_entries = parser.parse_excel_file(excel_path)

print("=" * 80)
print("EMPLOYEE LOCATIONS")
print("=" * 80)
print(f"\nTotal Employees: {len(employees)}\n")

gcc_count = 0
us_count = 0

for emp in employees:
    print(f"Emp ID: {emp.emp_id:<10} | Name: {emp.name:<30} | Location: {emp.location}")
    if emp.location == 'GCC':
        gcc_count += 1
    elif emp.location == 'US':
        us_count += 1

print("\n" + "=" * 80)
print(f"GCC Employees: {gcc_count}")
print(f"US Employees: {us_count}")
print("=" * 80)

