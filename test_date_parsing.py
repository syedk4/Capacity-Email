"""Test date parsing with actual Excel formats"""
import re
from datetime import date

def parse_date_string(date_str, month, year):
    """Parse date string and return list of dates"""
    if not date_str or str(date_str).strip() == '':
        return []

    dates = []
    date_str = str(date_str).strip()

    # Common patterns for date parsing
    patterns = [
        r'(\d{1,2})(?:st|nd|rd|th)?',
        r'(\d{1,2})',  # Simple numbers
    ]

    for pattern in patterns:
        matches = re.findall(pattern, date_str)
        for match in matches:
            try:
                day = int(match)
                if 1 <= day <= 31:
                    try:
                        parsed_date = date(year, month, day)
                        if parsed_date not in dates:
                            dates.append(parsed_date)
                    except ValueError:
                        continue
            except ValueError:
                continue

    return sorted(dates)

# Test cases from Excel
test_cases = [
    ("22, 30", 1, 2026, "Suganya - January"),
    ("16 to 27", 2, 2026, "Suganya - February"),
    ("2, 3, 16, 17", 2, 2026, "BindhuMadhuri - February"),
    ("19,20,23", 2, 2026, "Lakshmipathy - February"),
    ("16 and 17", 2, 2026, "Syed Sufdar - February"),
    ("23", 2, 2026, "Dhivya - February"),
    ("2", 1, 2026, "Lakshmipathy - January"),
    ("28", 1, 2026, "Syed Sufdar - January"),
]

print("=" * 100)
print("DATE PARSING TEST - ACTUAL EXCEL FORMATS")
print("=" * 100)

for date_str, month, year, label in test_cases:
    result = parse_date_string(date_str, month, year)
    month_name = ["", "Jan", "Feb", "Mar"][month]
    
    print(f"\n{label}")
    print(f"  Input: '{date_str}'")
    print(f"  Parsed: {[d.strftime(f'{month_name} %d') for d in result]}")
    print(f"  Count: {len(result)} dates")
    
    # Check if parsing is correct
    if len(result) == 0:
        print(f"  ❌ ERROR: No dates parsed!")
    elif date_str == "16 and 17" and len(result) != 2:
        print(f"  ❌ ERROR: Expected 2 dates, got {len(result)}")
    elif date_str == "19,20,23" and len(result) != 3:
        print(f"  ❌ ERROR: Expected 3 dates, got {len(result)}")
    else:
        print(f"  ✅ OK")

print("\n" + "=" * 100)

