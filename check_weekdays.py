from datetime import date

# Check if Feb 19-20 are weekdays
feb_19 = date(2026, 2, 19)
feb_20 = date(2026, 2, 20)
feb_23 = date(2026, 2, 23)

print(f'Feb 19, 2026: {feb_19.strftime("%A")} (weekday={feb_19.weekday()})')
print(f'Feb 20, 2026: {feb_20.strftime("%A")} (weekday={feb_20.weekday()})')
print(f'Feb 23, 2026: {feb_23.strftime("%A")} (weekday={feb_23.weekday()})')

print()
print('Weekday values: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun')
print('Working days: 0-4 (Mon-Fri)')

