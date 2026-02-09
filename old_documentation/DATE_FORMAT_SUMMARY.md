# 📅 Date Format Summary - Quick Answer

## Your Question: "What if user gives 16 to 27?"

### Answer: The program creates individual dates for each day

When user enters `16 to 27` in the Planned Leave column:

```
Input: "16 to 27"
↓
Program extracts: 16, 27
↓
Creates dates: Jan 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
↓
Filters weekdays: Jan 16(Fri), 19(Mon), 20(Tue), 21(Wed), 22(Thu), 23(Fri), 26(Mon), 27(Tue)
↓
Checks sprint period: If dates fall in sprint → counts them
↓
Reduces capacity: Each working day = -1 person-day
```

---

## Can User Give ANY Random Date?

### ✅ YES - Program is Flexible

The program accepts **any format** as long as it contains **day numbers (1-31)**:

| Format | Works? | Example |
|--------|--------|---------|
| `15th` | ✅ Yes | Single date |
| `1st, 4th` | ✅ Yes | Multiple dates |
| `16 to 27` | ✅ Yes | Range |
| `16-27` | ✅ Yes | Dash range |
| `1st & 4th` | ✅ Yes | Ampersand |
| `1st and 4th` | ✅ Yes | Word separator |
| `1, 4, 15` | ✅ Yes | Plain numbers |
| `Jan 15th` | ❌ No | Month name in data |
| `2026-01-15` | ❌ No | Full date format |

---

## Should It Be Specific Format?

### Answer: NO - But Follow These Rules

**The program is FLEXIBLE but has RULES:**

1. **Use day numbers only** (1-31)
   - ✅ `15th`, `1st`, `28`
   - ❌ `Jan 15`, `January 15`

2. **Use any separator**
   - ✅ Comma: `1st, 4th`
   - ✅ Ampersand: `1st & 4th`
   - ✅ Word: `1st and 4th`
   - ✅ Dash: `1-4`

3. **Month comes from column header**
   - ✅ Column named "January" + data "15th" = Jan 15
   - ❌ Don't put month name in data cell

4. **Weekends are auto-excluded**
   - ✅ Enter `16 to 27` - program removes weekends
   - ❌ Don't manually skip weekends

---

## How Program Calculates with "16 to 27"

### Example Calculation

**Setup:**
- Employee: John Doe
- Leave: `16 to 27` in January
- Sprint 3: Jan 28 - Feb 10

**Calculation:**

```
Step 1: Parse "16 to 27"
→ Creates 12 dates: Jan 16-27

Step 2: Filter weekdays
→ Removes weekends (17, 18, 24, 25)
→ Keeps 10 working days

Step 3: Check sprint period
→ Sprint 3 is Jan 28 - Feb 10
→ Leave dates are Jan 16-27
→ NO OVERLAP
→ Leave days in Sprint 3: 0

Step 4: Capacity impact
→ John has 0 leave days in Sprint 3
→ John is AVAILABLE for Sprint 3
→ No capacity reduction
```

---

## Real Example: "28 to 31" in January

**Setup:**
- Employee: Jane Smith
- Leave: `28 to 31` in January
- Sprint 3: Jan 28 - Feb 10

**Calculation:**

```
Step 1: Parse "28 to 31"
→ Creates 4 dates: Jan 28, 29, 30, 31

Step 2: Filter weekdays
→ Jan 28 = Tue ✅
→ Jan 29 = Wed ✅
→ Jan 30 = Thu ✅
→ Jan 31 = Fri ✅
→ All 4 are working days

Step 3: Check sprint period
→ Sprint 3 is Jan 28 - Feb 10
→ All 4 dates are IN Sprint 3
→ Leave days in Sprint 3: 4

Step 4: Capacity impact
→ Jane has 4 leave days in Sprint 3
→ Reduces team capacity by 4 person-days
→ If team is 7 members × 10 working days = 70 person-days
→ Capacity = (70 - 4) / 70 = 91.4%
```

---

## Key Points

### Date Parsing
- **Flexible:** Accepts various formats
- **Smart:** Extracts day numbers from any text
- **Automatic:** Removes weekends, filters by sprint

### Capacity Calculation
- **Person-days:** Team members × Working days
- **Leave reduction:** Each leave day = -1 person-day
- **Sprint filter:** Only dates in sprint period count
- **Weekday only:** Weekends don't count

### User Input
- **Can be random:** Any format with day numbers works
- **Should be clear:** Use consistent format for readability
- **Must be valid:** Day 1-31 (Feb 30 is invalid)
- **No month names:** Use column headers for months

---

## Examples of Valid Inputs

```
15th                    ✅ Single date
1st, 4th, 15th         ✅ Multiple dates
16 to 27               ✅ Range
16-27                  ✅ Dash range
1st & 4th              ✅ Ampersand
1st and 4th            ✅ Word separator
1, 4, 15               ✅ Plain numbers
1st, 5-7, 15th         ✅ Mixed format
28 to 31               ✅ End of month range
```

---

## Examples of Invalid Inputs

```
Jan 15th               ❌ Month name in data
January 15             ❌ Full month name
2026-01-15             ❌ Full date format
15/01/2026             ❌ Date format
Feb 30th               ❌ Invalid date (Feb has 28/29 days)
32nd                   ❌ Invalid day (max 31)
```

---

## Bottom Line

✅ **User can enter dates in flexible format**
- `16 to 27` works perfectly
- Program extracts day numbers
- Creates individual dates
- Filters weekdays automatically
- Checks sprint period
- Calculates capacity impact

❌ **But must follow basic rules**
- Use day numbers (1-31)
- Don't include month names in data
- Don't use full date formats
- Keep dates valid (1-31)

**Result:** Flexible but smart date parsing that handles real-world data entry variations!

