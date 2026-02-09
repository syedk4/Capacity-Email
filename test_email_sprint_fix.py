"""Test to verify email template shows next 2 upcoming sprints correctly"""
from datetime import date, datetime, timedelta

# Configuration
sprint_start_date = "2025-12-16"
sprint_duration_days = 14
reference_date = datetime.strptime('2025-12-31', '%Y-%m-%d').date()

# Parse dates
first_sprint_start = datetime.strptime(sprint_start_date, '%Y-%m-%d').date()
today = date.today()

print("=" * 80)
print("EMAIL TEMPLATE SPRINT SELECTION - VERIFICATION TEST")
print("=" * 80)
print(f"\nToday's Date: {today}")
print(f"First Sprint Start: {first_sprint_start}")
print(f"Reference Date (for numbering): {reference_date}")
print(f"Sprint Duration: {sprint_duration_days} days")

# Calculate current sprint
days_since_start = (today - first_sprint_start).days
current_sprint_number = max(0, days_since_start // sprint_duration_days)

print(f"\nDays since first sprint start: {days_since_start}")
print(f"Current Sprint Index (0-indexed): {current_sprint_number}")
print(f"Current Sprint Number (1-indexed): {current_sprint_number + 1}")

# Generate sprints
def calculate_sprints(start_date, num_sprints):
    sprints = []
    current_start = start_date
    for i in range(num_sprints):
        sprint_end = current_start + timedelta(days=sprint_duration_days - 1)
        sprints.append({
            'index': i,
            'number': i + 1,
            'start_date': current_start,
            'end_date': sprint_end
        })
        current_start = sprint_end + timedelta(days=1)
    return sprints

all_sprints = calculate_sprints(first_sprint_start, current_sprint_number + 5)

print("\n" + "=" * 80)
print("ALL SPRINTS:")
print("=" * 80)
for sprint in all_sprints:
    marker = ""
    if sprint['index'] == current_sprint_number:
        marker = " ← CURRENT SPRINT"
    print(f"Index {sprint['index']}: Sprint {sprint['number']}: {sprint['start_date']} to {sprint['end_date']}{marker}")

# Current logic: get previous, current, and next 3
start_index = max(0, current_sprint_number - 1)
returned_sprints = all_sprints[start_index:start_index + 4]

print("\n" + "=" * 80)
print("SPRINTS RETURNED BY get_current_and_upcoming_sprints():")
print("=" * 80)
for i, sprint in enumerate(returned_sprints):
    print(f"Index {i}: Sprint {sprint['number']}: {sprint['start_date']} to {sprint['end_date']}")

# Email template logic: indices 2 and 3
print("\n" + "=" * 80)
print("EMAIL TEMPLATE LOGIC (indices 2 and 3 from returned sprints):")
print("=" * 80)
if len(returned_sprints) >= 4:
    email_sprints = returned_sprints[2:4]
    for i, sprint in enumerate(email_sprints):
        # Calculate absolute sprint number using reference date
        days_from_ref = (sprint['start_date'] - reference_date).days
        absolute_sprint_num = (days_from_ref // 14) + 1
        print(f"Email Sprint {i+1}: Sprint {absolute_sprint_num} ({sprint['start_date']} to {sprint['end_date']})")
else:
    print("Not enough sprints!")

# What SHOULD be shown: next 2 upcoming sprints from today
print("\n" + "=" * 80)
print("EXPECTED: Next 2 upcoming sprints from today:")
print("=" * 80)
next_2_sprints = all_sprints[current_sprint_number + 1:current_sprint_number + 3]
for i, sprint in enumerate(next_2_sprints):
    # Calculate absolute sprint number using reference date
    days_from_ref = (sprint['start_date'] - reference_date).days
    absolute_sprint_num = (days_from_ref // 14) + 1
    print(f"Expected Sprint {i+1}: Sprint {absolute_sprint_num} ({sprint['start_date']} to {sprint['end_date']})")

print("\n" + "=" * 80)
print("VERIFICATION:")
print("=" * 80)
print(f"Current Sprint: Sprint {current_sprint_number + 1} ({all_sprints[current_sprint_number]['start_date']} to {all_sprints[current_sprint_number]['end_date']})")
print(f"\nNext 2 Upcoming Sprints:")
print(f"  1. Sprint {next_2_sprints[0]['number']} ({next_2_sprints[0]['start_date']} to {next_2_sprints[0]['end_date']})")
print(f"  2. Sprint {next_2_sprints[1]['number']} ({next_2_sprints[1]['start_date']} to {next_2_sprints[1]['end_date']})")

# Calculate absolute sprint numbers for email
email_sprint_1_abs = ((next_2_sprints[0]['start_date'] - reference_date).days // 14) + 1
email_sprint_2_abs = ((next_2_sprints[1]['start_date'] - reference_date).days // 14) + 1

print(f"\nEmail Template Shows:")
print(f"  1. Sprint {email_sprint_1_abs} ({next_2_sprints[0]['start_date']} to {next_2_sprints[0]['end_date']})")
print(f"  2. Sprint {email_sprint_2_abs} ({next_2_sprints[1]['start_date']} to {next_2_sprints[1]['end_date']})")

if email_sprints[0]['number'] == next_2_sprints[0]['number'] and email_sprints[1]['number'] == next_2_sprints[1]['number']:
    print("\n✅ EMAIL TEMPLATE IS CORRECT - Shows next 2 upcoming sprints!")
else:
    print("\n❌ EMAIL TEMPLATE IS INCORRECT")
    print(f"   Currently showing Sprint {email_sprints[0]['number']} and Sprint {email_sprints[1]['number']}")
    print(f"   Should show Sprint {next_2_sprints[0]['number']} and Sprint {next_2_sprints[1]['number']}")

