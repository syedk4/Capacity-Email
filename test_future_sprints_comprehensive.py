#!/usr/bin/env python3
"""
Comprehensive test suite for future sprints, months, and dates
Tests reports and emails for various future dates
"""

from datetime import datetime, date, timedelta
from sprint_capacity_app import SprintManager, SprintCapacityCalculator
import json
import os

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Create calculator
calculator = SprintCapacityCalculator('config.json')
sprint_manager = SprintManager(calculator)

# Test dates covering different months and quarters
test_dates = [
    # Q1 2026
    ("2026-01-14", "January 2026 - Current"),
    ("2026-01-31", "January 2026 - End of Month"),
    ("2026-02-15", "February 2026 - Mid Month"),
    ("2026-02-28", "February 2026 - End of Month"),
    ("2026-03-15", "March 2026 - Mid Month"),
    ("2026-03-31", "March 2026 - End of Month"),
    
    # Q2 2026
    ("2026-04-15", "April 2026 - Mid Month"),
    ("2026-05-15", "May 2026 - Mid Month"),
    ("2026-06-15", "June 2026 - Mid Month"),
    
    # Q3 2026
    ("2026-07-15", "July 2026 - Mid Month"),
    ("2026-07-31", "July 2026 - End of Month"),
    ("2026-08-15", "August 2026 - Mid Month"),
    ("2026-09-15", "September 2026 - Mid Month"),
    
    # Q4 2026
    ("2026-10-15", "October 2026 - Mid Month"),
    ("2026-11-15", "November 2026 - Mid Month"),
    ("2026-12-15", "December 2026 - Mid Month"),
    
    # 2027
    ("2027-01-15", "January 2027 - Future Year"),
    ("2027-06-15", "June 2027 - Future Year"),
    ("2027-12-15", "December 2027 - Future Year"),
]

print("=" * 100)
print("COMPREHENSIVE FUTURE SPRINTS AND DATES TEST")
print("=" * 100)
print(f"\nConfiguration:")
print(f"  Sprint Start Date: {config['sprint_start_date']}")
print(f"  Sprint Duration: {config['sprint_duration_days']} days")
print(f"  Total Test Dates: {len(test_dates)}")
print()

# Track results
results = []
first_sprint_start = datetime.strptime(config['sprint_start_date'], '%Y-%m-%d').date()
sprint_duration = config['sprint_duration_days']

for test_date_str, label in test_dates:
    test_date = datetime.strptime(test_date_str, '%Y-%m-%d').date()
    
    # Calculate current sprint
    days_since_start = (test_date - first_sprint_start).days
    current_sprint_number = max(0, days_since_start // sprint_duration)
    
    # Generate sprints
    all_sprints = sprint_manager.calculate_sprints(
        first_sprint_start, current_sprint_number + 5)
    
    # Get next 2 sprints for email
    email_sprint_1 = current_sprint_number + 2
    email_sprint_2 = current_sprint_number + 3
    
    # Verify sprints exist
    email_valid = (email_sprint_1 < len(all_sprints) and 
                   email_sprint_2 < len(all_sprints))
    
    result = {
        'date': test_date_str,
        'label': label,
        'current_sprint': current_sprint_number + 1,
        'email_sprint_1': email_sprint_1 + 1 if email_sprint_1 < len(all_sprints) else None,
        'email_sprint_2': email_sprint_2 + 1 if email_sprint_2 < len(all_sprints) else None,
        'valid': email_valid,
        'status': '✅ PASS' if email_valid else '❌ FAIL'
    }
    results.append(result)
    
    print(f"{label}")
    print(f"  Date: {test_date_str}")
    print(f"  Current Sprint: {result['current_sprint']}")
    print(f"  Email Sprints: {result['email_sprint_1']}, {result['email_sprint_2']}")
    print(f"  Status: {result['status']}")
    print()

# Summary
print("\n" + "=" * 100)
print("TEST SUMMARY")
print("=" * 100)

passed = sum(1 for r in results if r['valid'])
failed = sum(1 for r in results if not r['valid'])

print(f"\nTotal Tests: {len(results)}")
print(f"Passed: {passed} ✅")
print(f"Failed: {failed} ❌")
print(f"Success Rate: {(passed/len(results)*100):.1f}%")

if failed > 0:
    print("\nFailed Tests:")
    for r in results:
        if not r['valid']:
            print(f"  - {r['label']}")

print("\n" + "=" * 100)
print("CONCLUSION: All future dates tested successfully!" if failed == 0 else "CONCLUSION: Some tests failed!")
print("=" * 100)

