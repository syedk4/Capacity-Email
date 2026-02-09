from datetime import date

def format_dates_as_ranges(dates):
    """Format a list of dates as ranges where possible"""
    if not dates:
        return ""

    sorted_dates = sorted(dates)
    ranges = []
    range_start = sorted_dates[0]
    range_end = sorted_dates[0]

    for i in range(1, len(sorted_dates)):
        current_date = sorted_dates[i]
        # Check if current date is consecutive (next day)
        if (current_date - range_end).days == 1:
            # Extend the range
            range_end = current_date
        else:
            # Range is broken, save the current range and start a new one
            if range_start == range_end:
                # Single date
                ranges.append(range_start.strftime("%b %d"))
            else:
                # Date range
                ranges.append(
                    f"{range_start.strftime('%b %d')}-{range_end.strftime('%d')}")
            range_start = current_date
            range_end = current_date

    # Don't forget the last range
    if range_start == range_end:
        ranges.append(range_start.strftime("%b %d"))
    else:
        ranges.append(
            f"{range_start.strftime('%b %d')}-{range_end.strftime('%d')}")

    return ", ".join(ranges)

# Test with Lakshmipathy's data
test_dates = [date(2026, 2, 19), date(2026, 2, 20), date(2026, 2, 23)]
result = format_dates_as_ranges(test_dates)

print("Test: Lakshmipathy - February Leave")
print(f"Input dates: {[d.strftime('%b %d') for d in test_dates]}")
print(f"Formatted: {result}")
print(f"Expected: Feb 19-20, Feb 23")
print(f"Match: {result == 'Feb 19-20, Feb 23'}")

