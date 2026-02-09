#!/usr/bin/env python3
"""
Test script to verify the application works for future dates (March and July)
"""

from datetime import datetime, date
from sprint_capacity_app import SprintManager, SprintCapacityCalculator
import json

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Create calculator
calculator = SprintCapacityCalculator('config.json')
sprint_manager = SprintManager(calculator)

# Test dates
test_dates = [
    ("2026-01-14", "January 2026 (Current)"),
    ("2026-03-15", "March 2026 (Future)"),
    ("2026-07-20", "July 2026 (Future)"),
]

print("=" * 80)
print("SPRINT CALCULATION TEST FOR FUTURE DATES")
print("=" * 80)
print(f"\nSprint Configuration:")
print(f"  Sprint Start Date: {config['sprint_start_date']}")
print(f"  Sprint Duration: {config['sprint_duration_days']} days")
print()

for test_date_str, label in test_dates:
    test_date = datetime.strptime(test_date_str, '%Y-%m-%d').date()

    print(f"\n{'=' * 80}")
    print(f"Testing: {label}")
    print(f"{'=' * 80}")

    # Manually calculate sprints as if today is test_date
    first_sprint_start = datetime.strptime(
        config['sprint_start_date'], '%Y-%m-%d').date()
    days_since_start = (test_date - first_sprint_start).days
    sprint_duration = config['sprint_duration_days']
    current_sprint_number = max(0, days_since_start // sprint_duration)

    print(f"Days since sprint start: {days_since_start}")
    print(f"Current sprint number: {current_sprint_number + 1}")

    # Generate sprints
    all_sprints = sprint_manager.calculate_sprints(
        first_sprint_start, current_sprint_number + 5)

    # Show previous, current, and next 2 sprints
    start_index = max(0, current_sprint_number - 1)
    end_index = min(len(all_sprints), current_sprint_number + 3)

    print(f"\nSprints to display (Previous, Current, Next 2):")
    for i in range(start_index, end_index):
        sprint = all_sprints[i]
        is_current = "✓ CURRENT" if i == current_sprint_number else ""
        print(
            f"  Sprint {sprint.number}: {sprint.start_date} to {sprint.end_date} {is_current}")

    # Show next 2 sprints for email template
    email_start = current_sprint_number + 2
    email_end = min(len(all_sprints), current_sprint_number + 4)

    print(f"\nSprints for Email Template (Next 2):")
    for i in range(email_start, email_end):
        if i < len(all_sprints):
            sprint = all_sprints[i]
            print(
                f"  Sprint {sprint.number}: {sprint.start_date} to {sprint.end_date}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
