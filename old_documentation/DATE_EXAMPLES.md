# 📋 Date Format Examples - Real Scenarios

## Scenario 1: User Enters "16 to 27" in January Planned Leave

### Input Data
```
Employee: John Doe
Month: January
Planned Leave: 16 to 27
Sprint: Sprint 3 (Jan 28 - Feb 10)
```

### Step-by-Step Processing

**Step 1: Parse the Date String**
```
Input: "16 to 27"
Regex extracts: 16, 27
Creates dates: Jan 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
Total: 12 dates
```

**Step 2: Filter Weekdays Only**
```
Jan 16 = Friday ✅ (weekday)
Jan 17 = Saturday ❌ (weekend - removed)
Jan 18 = Sunday ❌ (weekend - removed)
Jan 19 = Monday ✅ (weekday)
Jan 20 = Tuesday ✅ (weekday)
Jan 21 = Wednesday ✅ (weekday)
Jan 22 = Thursday ✅ (weekday)
Jan 23 = Friday ✅ (weekday)
Jan 24 = Saturday ❌ (weekend - removed)
Jan 25 = Sunday ❌ (weekend - removed)
Jan 26 = Monday ✅ (weekday)
Jan 27 = Tuesday ✅ (weekday)

Remaining: 10 working days
```

**Step 3: Check if Dates Fall in Sprint 3**
```
Sprint 3 Period: Jan 28 - Feb 10
John's leave dates: Jan 16-27
Overlap: NONE (all leave dates are BEFORE sprint)

Leave days counted for Sprint 3: 0 days
```

**Step 4: Impact on Capacity**
```
Sprint 3 has 10 working days
Team: 7 members
Total person-days: 7 × 10 = 70

John's leave in Sprint 3: 0 days
Capacity impact: NONE

Result: John is AVAILABLE for Sprint 3
```

---

## Scenario 2: User Enters "1st, 4th, 15th" in February

### Input Data
```
Employee: Jane Smith
Month: February
Planned Leave: 1st, 4th, 15th
Sprint: Sprint 3 (Jan 28 - Feb 10)
```

### Processing

**Step 1: Parse Dates**
```
Input: "1st, 4th, 15th"
Extracted: 1, 4, 15
Dates: Feb 1, Feb 4, Feb 15
```

**Step 2: Filter Weekdays**
```
Feb 1 = Saturday ❌ (weekend)
Feb 4 = Tuesday ✅ (weekday)
Feb 15 = Friday ✅ (weekday)

Remaining: 2 working days
```

**Step 3: Check Sprint Period**
```
Sprint 3: Jan 28 - Feb 10
Jane's dates: Feb 1, 4, 15

Dates in Sprint 3:
- Feb 1: Outside (before sprint) ❌
- Feb 4: Inside (Jan 28 - Feb 10) ✅
- Feb 15: Outside (after sprint) ❌

Dates counted: Feb 4 only = 1 day
```

**Step 4: Capacity Impact**
```
Sprint 3: 10 working days, 7 members
Total person-days: 70

Jane's leave in Sprint 3: 1 day
Capacity reduction: 1 / 70 = 1.4%

Result: Jane is ON LEAVE for 1 day in Sprint 3
```

---

## Scenario 3: User Enters "28 to 31" in January

### Input Data
```
Employee: Bob Wilson
Month: January
Planned Leave: 28 to 31
Sprint: Sprint 3 (Jan 28 - Feb 10)
```

### Processing

**Step 1: Parse Dates**
```
Input: "28 to 31"
Extracted: 28, 29, 30, 31
Dates: Jan 28, 29, 30, 31
```

**Step 2: Filter Weekdays**
```
Jan 28 = Tuesday ✅
Jan 29 = Wednesday ✅
Jan 30 = Thursday ✅
Jan 31 = Friday ✅

Remaining: 4 working days
```

**Step 3: Check Sprint Period**
```
Sprint 3: Jan 28 - Feb 10
Bob's dates: Jan 28, 29, 30, 31

All dates are in Sprint 3 ✅

Dates counted: 4 days
```

**Step 4: Capacity Impact**
```
Sprint 3: 10 working days, 7 members
Total person-days: 70

Bob's leave in Sprint 3: 4 days
Capacity reduction: 4 / 70 = 5.7%

Result: Bob is ON LEAVE for 4 days in Sprint 3
```

---

## Scenario 4: Mixed Format "1st, 5-7, 15th"

### Input Data
```
Employee: Alice Johnson
Month: March
Planned Leave: 1st, 5-7, 15th
Sprint: Sprint 4 (Feb 11 - Feb 24)
```

### Processing

**Step 1: Parse Dates**
```
Input: "1st, 5-7, 15th"
Extracted: 1, 5, 7, 15
Dates: Mar 1, 5, 6, 7, 15
```

**Step 2: Filter Weekdays**
```
Mar 1 = Saturday ❌
Mar 5 = Wednesday ✅
Mar 6 = Thursday ✅
Mar 7 = Friday ✅
Mar 15 = Saturday ❌

Remaining: 3 working days
```

**Step 3: Check Sprint Period**
```
Sprint 4: Feb 11 - Feb 24
Alice's dates: Mar 1, 5, 6, 7, 15

All dates are in MARCH (after Sprint 4) ❌

Dates counted: 0 days
```

**Step 4: Capacity Impact**
```
Alice's leave in Sprint 4: 0 days
Capacity impact: NONE

Result: Alice is AVAILABLE for Sprint 4
```

---

## Scenario 5: Invalid Date Handling

### Input Data
```
Employee: Charlie Brown
Month: February
Planned Leave: 29th, 30th
Sprint: Sprint 3 (Jan 28 - Feb 10)
```

### Processing

**Step 1: Parse Dates**
```
Input: "29th, 30th"
Extracted: 29, 30
Attempts to create: Feb 29, Feb 30
```

**Step 2: Validation**
```
Feb 29 = Valid (2026 is not leap year, but program tries)
Feb 30 = INVALID ❌ (February has max 28/29 days)

Program skips invalid dates
Remaining: Feb 29 (if valid) or 0 dates
```

**Step 3: Result**
```
If Feb 29 is invalid: 0 dates parsed
If Feb 29 is valid: 1 date parsed

Capacity impact: Minimal or none
```

---

## Scenario 6: Duplicate Dates

### Input Data
```
Employee: Diana Prince
Month: January
Planned Leave: 15th, 15th, 16th
Sprint: Sprint 3 (Jan 28 - Feb 10)
```

### Processing

**Step 1: Parse Dates**
```
Input: "15th, 15th, 16th"
Extracted: 15, 15, 16
Initial dates: Jan 15, 15, 16
```

**Step 2: Remove Duplicates**
```
Program removes duplicate Jan 15
Final dates: Jan 15, 16
```

**Step 3: Filter Weekdays**
```
Jan 15 = Thursday ✅
Jan 16 = Friday ✅

Remaining: 2 working days
```

**Step 4: Check Sprint Period**
```
Sprint 3: Jan 28 - Feb 10
Diana's dates: Jan 15, 16

Both dates are BEFORE Sprint 3 ❌

Dates counted: 0 days
```

---

## Key Takeaways

| Scenario | Input | Parsed As | In Sprint? | Impact |
|----------|-------|-----------|-----------|--------|
| Range | 16 to 27 | 12 dates | Check each | Varies |
| Multiple | 1st, 4th, 15th | 3 dates | Check each | Varies |
| Weekend | 1st (Sat) | 1 date | No | 0 days |
| Invalid | 30th (Feb) | Skipped | N/A | 0 days |
| Duplicate | 15th, 15th | 1 date | Check | Varies |
| Mixed | 1st, 5-7 | 4 dates | Check each | Varies |

---

## Important Rules Summary

1. **Weekends are automatically excluded** - No need to skip them
2. **Only sprint dates count** - Past/future leave doesn't affect capacity
3. **Duplicates are removed** - Same date entered twice = counted once
4. **Invalid dates are skipped** - Feb 30 is ignored
5. **All formats work** - Comma, dash, "and", ampersand all work
6. **Flexible parsing** - Program handles various formats gracefully

