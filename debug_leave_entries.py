"""Debug script to check leave entries"""
import sys
sys.path.insert(0, '.')

from sprint_capacity_app import SprintCapacityCalculator, ExcelDataParser
from datetime import date

# Initialize calculator
calculator = SprintCapacityCalculator('config.json')

# Initialize parser
parser = ExcelDataParser(calculator)

# Parse Excel file
excel_path = r'C:\Users\slatheef\Ashley Furniture Industries, Inc\IT - Finance - India Finance Team Daily Updates\2026- India Finance team Daily work status.xlsx'
employees, leave_entries = parser.parse_excel_file(excel_path)

print("=" * 100)
print("LEAVE ENTRIES FOR LAKSHMIPATHY")
print("=" * 100)

for leave_entry in leave_entries:
    if leave_entry.employee.name == "Murugan, Lakshmipathy":
        print(f"\nEmployee: {leave_entry.employee.name}")
        print(f"Leave Type: {leave_entry.leave_type}")
        print(f"Description: {leave_entry.description}")
        print(f"Dates: {[d.strftime('%b %d') for d in leave_entry.leave_dates]}")
        print(f"Count: {len(leave_entry.leave_dates)} dates")

