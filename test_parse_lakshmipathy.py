"""Test parsing of Lakshmipathy's leave data"""
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

# Test with Lakshmipathy's exact data
test_data = '19,20,23'
result = parse_date_string(test_data, 2, 2026)

print("Test: Lakshmipathy - February Leave")
print(f"Input: '{test_data}'")
print(f"Parsed: {[d.strftime('Feb %d') for d in result]}")
print(f"Count: {len(result)} dates")
print(f"Expected: 3 dates (Feb 19, 20, 23)")
print(f"Status: {'✅ PASS' if len(result) == 3 else '❌ FAIL'}")

