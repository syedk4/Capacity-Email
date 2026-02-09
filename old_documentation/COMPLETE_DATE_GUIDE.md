# 📚 Complete Date Format Guide - Everything You Need to Know

## Quick Answer to Your Questions

### Q1: Can user give any random date format?
**A:** ✅ **YES** - The program is very flexible with date formats. It accepts:
- `16 to 27` ✅
- `1st, 4th` ✅
- `16-27` ✅
- `1st & 4th` ✅
- `1, 4, 15` ✅

### Q2: Should it be a specific format?
**A:** ❌ **NO** - No specific format required, but follow basic rules:
- Use day numbers (1-31)
- Don't include month names in data
- Don't use full date formats (2026-01-15)

### Q3: What if user gives "16 to 27"?
**A:** Program will:
1. Extract numbers: 16, 27
2. Create dates: Jan 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
3. Filter weekdays: Remove weekends (17, 18, 24, 25)
4. Keep: 10 working days
5. Check sprint period: If dates fall in sprint → count them
6. Calculate: Reduce capacity by number of leave days

---

## How the Program Processes Dates

### Step 1: Parsing
```
Input: "16 to 27"
↓
Regex Pattern: (\d{1,2})(?:st|nd|rd|th)?
↓
Extracted Numbers: 16, 27
↓
Created Dates: Jan 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
```

### Step 2: Weekday Filtering
```
Jan 16 = Friday ✅
Jan 17 = Saturday ❌ (removed)
Jan 18 = Sunday ❌ (removed)
Jan 19 = Monday ✅
Jan 20 = Tuesday ✅
Jan 21 = Wednesday ✅
Jan 22 = Thursday ✅
Jan 23 = Friday ✅
Jan 24 = Saturday ❌ (removed)
Jan 25 = Sunday ❌ (removed)
Jan 26 = Monday ✅
Jan 27 = Tuesday ✅

Result: 10 working days
```

### Step 3: Sprint Period Check
```
Sprint 3: Jan 28 - Feb 10
Leave dates: Jan 16-27
Overlap: NONE (leave is before sprint)

Leave days in Sprint 3: 0
```

### Step 4: Capacity Calculation
```
Total person-days = 7 members × 10 working days = 70
Leave person-days = 0 (no overlap with sprint)
Available person-days = 70 - 0 = 70
Capacity % = (70 / 70) × 100 = 100%
```

---

## Accepted Date Formats

### Format 1: Single Date
```
Input: 15th
Parsed: Jan 15
Weekday check: If weekday → counts
Sprint check: If in sprint → reduces capacity
```

### Format 2: Multiple Dates (Comma)
```
Input: 1st, 4th, 15th
Parsed: Jan 1, Jan 4, Jan 15
Each date checked individually
```

### Format 3: Range (Dash)
```
Input: 16-27
Parsed: Jan 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
Weekends removed: 10 working days
```

### Format 4: Range (Word)
```
Input: 16 to 27
Parsed: Jan 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
Same as dash format
```

### Format 5: Ampersand
```
Input: 1st & 4th
Parsed: Jan 1, Jan 4
Works like comma separator
```

### Format 6: Mixed
```
Input: 1st, 5-7, 15th
Parsed: Jan 1, Jan 5, Jan 6, Jan 7, Jan 15
Combines all formats
```

---

## NOT Accepted Formats

| Format | Why Not | Example |
|--------|---------|---------|
| Month in data | Use column header | ❌ Jan 15th |
| Full date | Use day only | ❌ 2026-01-15 |
| Month name | Use column header | ❌ January 15 |
| Date format | Use day only | ❌ 15/01/2026 |

---

## Capacity Calculation Formula

```
Total Person-Days = Number of Team Members × Working Days in Sprint

Example:
- Team: 7 members
- Sprint: Jan 28 - Feb 10 (14 calendar days)
- Working days (Mon-Fri): 10 days
- Total Person-Days: 7 × 10 = 70

Leave Person-Days = Sum of all leave days in sprint
(Only planned + optional holidays, only weekdays, only in sprint)

Example:
- John: 2 days leave in sprint
- Jane: 1 day leave in sprint
- Others: 0 days
- Total Leave: 3 person-days

Available Person-Days = Total - Leave
= 70 - 3 = 67

Capacity % = (Available / Total) × 100
= (67 / 70) × 100 = 95.7%
```

---

## Important Rules

### Rule 1: Weekends Auto-Excluded
- Saturday and Sunday are automatically removed
- No need to manually skip them
- Only Mon-Fri count as working days

### Rule 2: Sprint Period Filter
- Only dates within sprint period count
- Past leave: doesn't affect capacity
- Future leave: doesn't affect capacity
- Example: Jan 16-27 leave doesn't affect Sprint 3 (Jan 28-Feb 10)

### Rule 3: Leave Type Matters
- **Planned Leave** → Reduces capacity ✅
- **Optional Holiday** → Reduces capacity ✅
- **Public Holiday (GCC)** → Does NOT reduce capacity ❌

### Rule 4: Duplicates Removed
- Same date entered twice = counted once
- Example: "15th, 15th, 16th" = "15th, 16th"

### Rule 5: Invalid Dates Skipped
- Feb 30 is invalid → skipped
- Day 32 is invalid → skipped
- Program handles gracefully

---

## Real-World Examples

### Example 1: "16 to 27" in January
```
Sprint 3: Jan 28 - Feb 10
Leave: Jan 16-27
Result: 0 days (before sprint)
Impact: NONE
```

### Example 2: "28 to 31" in January
```
Sprint 3: Jan 28 - Feb 10
Leave: Jan 28-31
Result: 4 working days (all in sprint)
Impact: -4 person-days
```

### Example 3: "1st, 4th, 15th" in February
```
Sprint 3: Jan 28 - Feb 10
Leave: Feb 1, 4, 15
In sprint: Feb 4 only (1 day)
Impact: -1 person-day
```

### Example 4: "5-7" in February
```
Sprint 3: Jan 28 - Feb 10
Leave: Feb 5, 6, 7
All in sprint: 3 working days
Impact: -3 person-days
```

---

## User Guidelines

### ✅ DO:
1. Use day numbers (1-31)
2. Use any separator (comma, dash, "and", "&")
3. Enter dates in correct month column
4. Use ranges for consecutive days
5. Mix formats if needed

### ❌ DON'T:
1. Include month names in data
2. Use full date formats
3. Expect automatic range expansion across months
4. Enter invalid dates (Feb 30)
5. Leave employee names blank

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Dates not parsing | Wrong format | Use day numbers only |
| Weekends counted | Misunderstanding | Program auto-excludes weekends |
| No capacity impact | Dates outside sprint | Check sprint period |
| Invalid date error | Feb 30, etc. | Use valid days (1-31) |
| Duplicate dates | Entered twice | Program removes duplicates |

---

## Summary Table

| Aspect | Details |
|--------|---------|
| **Flexibility** | Very flexible - accepts various formats |
| **Required** | Day numbers (1-31) only |
| **Separators** | Comma, dash, "and", "&" all work |
| **Weekends** | Auto-excluded from calculation |
| **Sprint Filter** | Only dates in sprint period count |
| **Leave Types** | Planned/Optional reduce capacity; Public holidays don't |
| **Duplicates** | Automatically removed |
| **Invalid Dates** | Skipped gracefully |

---

## Key Takeaway

**The program is smart and flexible:**
- ✅ Accepts various date formats
- ✅ Automatically handles weekends
- ✅ Filters by sprint period
- ✅ Calculates capacity accurately
- ✅ Handles edge cases gracefully

**Users can enter dates naturally:**
- `16 to 27` works
- `1st, 4th` works
- `16-27` works
- Any format with day numbers works!

