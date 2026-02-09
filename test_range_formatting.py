from datetime import date, timedelta

def format_dates_as_ranges(dates):
    if not dates:
        return ''
    
    sorted_dates = sorted(dates)
    ranges = []
    range_start = sorted_dates[0]
    range_end = sorted_dates[0]
    
    for i in range(1, len(sorted_dates)):
        current_date = sorted_dates[i]
        if (current_date - range_end).days == 1:
            range_end = current_date
        else:
            if range_start == range_end:
                ranges.append(range_start.strftime('%b %d'))
            else:
                start_str = range_start.strftime('%b %d')
                end_str = range_end.strftime('%d')
                ranges.append(f'{start_str}-{end_str}')
            range_start = current_date
            range_end = current_date
    
    if range_start == range_end:
        ranges.append(range_start.strftime('%b %d'))
    else:
        start_str = range_start.strftime('%b %d')
        end_str = range_end.strftime('%d')
        ranges.append(f'{start_str}-{end_str}')
    
    return ', '.join(ranges)

# Test cases
test_cases = [
    # Continuous range
    ([date(2026, 2, 16) + timedelta(days=i) for i in range(9)], 'Feb 16-24'),
    # Single date
    ([date(2026, 2, 16)], 'Feb 16'),
    # Multiple ranges
    ([date(2026, 2, 16), date(2026, 2, 17), date(2026, 2, 18), date(2026, 2, 20), date(2026, 2, 21)], 'Feb 16-18, Feb 20-21'),
    # All 12 dates
    ([date(2026, 2, 16) + timedelta(days=i) for i in range(12)], 'Feb 16-27'),
]

print("Testing date range formatting:")
print("=" * 60)

for dates, expected in test_cases:
    result = format_dates_as_ranges(dates)
    status = 'PASS' if result == expected else 'FAIL'
    print(f'{status}: Expected: {expected}')
    print(f'      Got:      {result}')
    print()

