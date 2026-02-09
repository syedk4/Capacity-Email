#!/usr/bin/env python3
"""
Test script to verify the full application works for future dates
by mocking the current date
"""

from datetime import datetime, date
from unittest.mock import patch
from sprint_capacity_app import SprintCapacityApp
import sys

# Test dates
test_dates = [
    ("2026-01-14", "January 2026 (Current)"),
    ("2026-03-15", "March 2026 (Future)"),
    ("2026-07-20", "July 2026 (Future)"),
]

print("=" * 80)
print("FULL APPLICATION TEST FOR FUTURE DATES")
print("=" * 80)

for test_date_str, label in test_dates:
    test_date = datetime.strptime(test_date_str, '%Y-%m-%d').date()

    print(f"\n{'=' * 80}")
    print(f"Testing: {label}")
    print(f"{'=' * 80}")

    try:
        # Mock date.today() to return test_date
        with patch('sprint_capacity_app.date') as mock_date:
            mock_date.today.return_value = test_date
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

            # Create app and run analysis
            app = SprintCapacityApp('config.json')

            # Get sprints
            excel_file = app.calculator.config['excel_file_path']
            oncall_schedules = app.parser.parse_oncall_schedules(excel_file)
            sprints = app.sprint_manager.get_current_and_upcoming_sprints(
                oncall_schedules
            )

            print(f"\nGenerated {len(sprints)} sprints")
            print(f"\nSprints (Previous, Current, Next 2):")
            for i, sprint in enumerate(sprints[:4]):
                print(
                    f"  Sprint {sprint.number}: {sprint.start_date} to {sprint.end_date}")

            print(f"\nEmail Template will show (Next 2):")
            for i, sprint in enumerate(sprints[2:4]):
                print(
                    f"  Sprint {sprint.number}: {sprint.start_date} to {sprint.end_date}")

            print(
                f"\n✓ Application successfully processed date: {test_date_str}")

    except Exception as e:
        print(f"\n✗ Error processing date {test_date_str}: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
