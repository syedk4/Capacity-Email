# 📅 Date Format Explanation - How the Program Parses and Calculates

## Overview

The program has **flexible date parsing** - it can handle various date formats. However, there are specific rules for how it interprets and calculates capacity based on those dates.

---

## Part 1: Date Parsing - What Formats Are Accepted?

### The Parsing Logic

The program uses **regex patterns** to extract day numbers from any text:

```
Pattern: (\d{1,2})(?:st|nd|rd|th)?
```

This means: **Extract 1 or 2 digit numbers, optionally followed by st/nd/rd/th**

### Accepted Formats ✅

| Format | Example | Parsed As | Notes |
|--------|---------|-----------|-------|
| **Single day** | `15th` | Day 15 | Most common |
| **Multiple days** | `1st, 4th` | Days 1, 4 | Comma-separated |
| **With ampersand** | `1st & 4th` | Days 1, 4 | Ampersand separator |
| **With "and"** | `1st and 4th` | Days 1, 4 | Word separator |
| **Plain numbers** | `1, 4` | Days 1, 4 | No suffix needed |
| **Mixed format** | `1st, 4, 15th` | Days 1, 4, 15 | Can mix styles |
| **Range notation** | `16 to 27` | Days 16, 17, 18...27 | **See explanation below** |
| **Dash notation** | `16-27` | Days 16, 17, 18...27 | **See explanation below** |

### NOT Accepted ❌

| Format | Why Not | What to Use Instead |
|--------|---------|---------------------|
| `Jan 15th` | Month name in data | Use column header for month |
| `2026-01-15` | Full date format | Use day number only (15th) |
| `15 January` | Full date format | Use day number only (15th) |
| `15/01/2026` | Full date format | Use day number only (15th) |

---

## Part 2: Range Dates - "16 to 27" Example

### What Happens When User Enters "16 to 27"?

**Input:** `16 to 27` in Planned Leave column for January

**Parsing Step:**
1. Program extracts all numbers: `16` and `27`
2. Creates individual dates for each number: `16th, 17th, 18th, 19th, 20th, 21st, 22nd, 23rd, 24th, 25th, 26th, 27th`
3. Sorts them in order

**Result:** 12 individual dates (16 through 27)

### Capacity Calculation Example

**Scenario:**
- Sprint 3: January 28 - February 10 (2 weeks)
- Employee: John Doe
- Planned Leave: `16 to 27` (in January column)
- Team: 7 members

**Step 1: Extract Leave Dates**
- Dates: Jan 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

**Step 2: Filter for Sprint Period**
- Sprint 3 is Jan 28 - Feb 10
- None of the leave dates (16-27) fall in Sprint 3
- **John Doe's leave days in Sprint 3: 0 days**

**Step 3: Calculate Capacity**
```
Sprint 3: Jan 28 - Feb 10 (14 days)
Working days (Mon-Fri only): 10 days
Total team: 7 members
Total person-days: 7 × 10 = 70 person-days

John Doe's leave in Sprint 3: 0 days
Other members' leave: (calculated similarly)

Capacity = (70 - total_leave_days) / 70 × 100%
```

---

## Part 3: Important Rules for Date Calculation

### Rule 1: Only Weekdays Count

**The program ONLY counts Monday-Friday as working days**

```
Example: "16 to 27" in January 2026
Jan 16 = Friday ✅ Counts
Jan 17 = Saturday ❌ Skipped (weekend)
Jan 18 = Sunday ❌ Skipped (weekend)
Jan 19 = Monday ✅ Counts
...
Jan 27 = Tuesday ✅ Counts

Actual working days: 16, 19, 20, 21, 22, 23, 24, 25, 26, 27 = 10 days
```

### Rule 2: Only Dates Within Sprint Period Count

**Leave dates outside the sprint don't affect capacity**

```
Example:
Sprint 3: Jan 28 - Feb 10
Employee leave: "16 to 27" (January)

Jan 16-27 are BEFORE Sprint 3
Result: 0 leave days counted for Sprint 3 capacity
```

### Rule 3: GCC Holidays Don't Reduce Capacity

**Public holidays are tracked but don't reduce team capacity**

```
Leave types:
- Planned Leave → REDUCES capacity ✅
- Optional Holiday → REDUCES capacity ✅
- Public Holiday (GCC) → DOES NOT reduce capacity ❌
```

### Rule 4: Duplicate Dates Are Removed

**If user enters same date twice, it's counted once**

```
Input: "15th, 15th, 16th"
Parsed as: 15th, 16th (duplicate removed)
```

---

## Part 4: Real-World Examples

### Example 1: Single Date

**Input:** `15th` in February column

**Parsing:**
- Extracted: Day 15
- Dates: Feb 15, 2026

**Capacity Impact:**
- If Feb 15 is in Sprint 3 AND is a weekday: -1 day from capacity
- If Feb 15 is weekend: 0 days (skipped)
- If Feb 15 is outside Sprint 3: 0 days (not counted)

---

### Example 2: Multiple Dates with Different Separators

**Input:** `1st, 4th & 15th` in January column

**Parsing:**
- Extracted: 1, 4, 15
- Dates: Jan 1, Jan 4, Jan 15

**Capacity Impact:**
- Each date checked if it's in sprint period AND is weekday
- Only matching dates reduce capacity

---

### Example 3: Range with Weekends

**Input:** `16 to 20` in January column

**Parsing:**
- Extracted: 16, 17, 18, 19, 20
- Dates: Jan 16, 17, 18, 19, 20

**Weekday Filtering:**
```
Jan 16 = Friday ✅
Jan 17 = Saturday ❌ (weekend)
Jan 18 = Sunday ❌ (weekend)
Jan 19 = Monday ✅
Jan 20 = Tuesday ✅

Actual working days: 3 days (16, 19, 20)
```

**Capacity Impact:**
- If all 3 days are in sprint: -3 days from capacity
- If only 2 days are in sprint: -2 days from capacity
- If 0 days are in sprint: 0 days (no impact)

---

### Example 4: Range Spanning Month Boundary

**Input:** `28 to 5` in January column (for Jan 28 - Feb 5)

**Parsing:**
- Extracted: 28, 5
- Dates: Jan 28, Feb 5 (only 2 dates, NOT a range!)

**Why?**
- Program extracts numbers: 28 and 5
- Creates dates in JANUARY: Jan 28 and Jan 5
- Does NOT automatically create range between them
- **This is a limitation - user should use separate entries**

**Better Format:** `28th, 29th, 30th, 31st` (for Jan) + `1st, 2nd, 3rd, 4th, 5th` (for Feb)

---

## Part 5: Capacity Calculation Formula

### The Math

```
Total Person-Days = Number of Team Members × Working Days in Sprint

Example:
- Team: 7 members
- Sprint: 14 calendar days (Jan 28 - Feb 10)
- Working days (Mon-Fri): 10 days
- Total Person-Days: 7 × 10 = 70 person-days

Leave Person-Days = Sum of all leave days for all members
(Only planned + optional holidays, only weekdays, only in sprint period)

Example:
- John Doe: 2 days leave in sprint
- Jane Smith: 1 day leave in sprint
- Others: 0 days
- Total Leave Person-Days: 3

Available Person-Days = Total - Leave
= 70 - 3 = 67 person-days

Capacity % = (Available / Total) × 100
= (67 / 70) × 100 = 95.7%
```

---

## Part 6: What Users Should Know

### ✅ DO:
1. Use day numbers only (1st, 15th, 28th)
2. Use any separator (comma, &, and, dash)
3. Enter dates in the correct month column
4. Use ranges for consecutive days (16 to 27)
5. Mix formats if needed (1st, 4, 15th)

### ❌ DON'T:
1. Include month names in data (Jan 15th)
2. Use full dates (2026-01-15)
3. Expect automatic range expansion across months
4. Enter invalid dates (Feb 30th)
5. Leave employee names blank

### ⚠️ IMPORTANT:
- **Weekends are automatically excluded** - no need to skip them
- **Only dates in sprint period count** - past/future dates don't affect capacity
- **Public holidays don't reduce capacity** - only planned/optional leave does
- **Program is flexible** - various formats work, but day numbers are required

---

## Summary

| Aspect | Details |
|--------|---------|
| **Date Format** | Day numbers (1-31) with optional st/nd/rd/th suffix |
| **Separators** | Comma, ampersand, "and", dash all work |
| **Ranges** | "16 to 27" creates individual dates 16-27 |
| **Weekends** | Automatically excluded from capacity calculation |
| **Sprint Filter** | Only dates within sprint period count |
| **Holiday Types** | Planned/Optional reduce capacity; Public holidays don't |
| **Flexibility** | Program handles various formats gracefully |

