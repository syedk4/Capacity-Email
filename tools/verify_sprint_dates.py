from datetime import datetime, timedelta

sprint_start = datetime.strptime("2025-12-17", "%Y-%m-%d").date()
sprint_duration = 14

print('='*70)
print('SPRINT DATE VERIFICATION')
print('='*70)
print(f'\nConfiguration:')
print(f'  Sprint Start Date: {sprint_start}')
print(f'  Sprint Duration: {sprint_duration} days')
print()

for i in range(1, 5):
    start_date = sprint_start + timedelta(days=(i-1) * sprint_duration)
    end_date = start_date + timedelta(days=sprint_duration - 1)
    
    # Count working days (exclude weekends)
    working_days = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Monday=0, Sunday=6
            working_days += 1
        current += timedelta(days=1)
    
    print(f'Sprint {i}:')
    print(f'  Period: {start_date.strftime("%b %d, %Y")} to {end_date.strftime("%b %d, %Y")}')
    print(f'  Total Days: {sprint_duration}')
    print(f'  Working Days: {working_days}')
    print()

