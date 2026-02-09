# ✅ Your Questions Answered

## Your Questions

1. **How does the program read data from the OneDrive file?**
2. **How can users update the data?**
3. **Should the date format be specific?**
4. **What if user gives "16 to 27"?**

---

## Answer 1: How Program Reads Data from OneDrive

### The Process

```
OneDrive File
    ↓
Auto-synced to Local Computer
    ↓
Program reads Excel file locally
    ↓
Parses "Leave plans" sheet
    ↓
Extracts employee names and leave dates
    ↓
Parses "On Call Schedules" sheet
    ↓
Extracts on-call assignments
    ↓
Calculates sprint capacity
    ↓
Generates email report
```

### File Location
```
C:\Users\slatheef\Ashley Furniture Industries, Inc\IT - Finance - India Finance Team Daily Updates\2026- India Finance team Daily work status.xlsx
```

### How It Works
1. **OneDrive syncs** the file to your local computer automatically
2. **Program reads** the Excel file from local storage (no internet needed)
3. **Parses sheets:** "Leave plans" and "On Call Schedules"
4. **Extracts data:** Employee info, leave dates, on-call assignments
5. **Calculates:** Sprint capacity based on leave data
6. **Generates:** Email reports with capacity percentages

---

## Answer 2: How Users Can Update Data

### Method 1: Edit Locally in Excel
1. Open the Excel file from your computer
2. Edit "Leave plans" sheet:
   - Add/remove leave dates in month columns
   - Update "Opting?" column for optional holidays
3. Edit "On Call Schedules" sheet:
   - Update on-call assignments
4. **Save the file** (Ctrl+S)
5. Run the program - it automatically reads updated data

### Method 2: Edit via OneDrive Web
1. Go to OneDrive.com
2. Navigate to the file
3. Click "Edit in Excel Online"
4. Make changes
5. Changes auto-save

### Method 3: Sync and Edit
1. OneDrive automatically syncs changes
2. Edit locally in Excel
3. Save - OneDrive syncs to cloud

### Required Data Format

**"Leave plans" Sheet:**
```
| Emp Id | Emp Name | January | February | March | Opting? |
|--------|----------|---------|----------|-------|---------|
| 200071 | John Doe | 1st, 4th | 15th | - | Yes |
| 200325 | Jane Smith | 28th, 29th | - | 10th | No |
```

**"On Call Schedules" Sheet:**
```
| Month | From Date | To date | Primary | Secondary |
|-------|-----------|---------|---------|-----------|
| January | 14th | 27th | John Doe | Jane Smith |
| February | 11th | 24th | Jane Smith | John Doe |
```

---

## Answer 3: Should Date Format Be Specific?

### Answer: NO - Program is Flexible

The program accepts **ANY format** as long as it contains **day numbers (1-31)**:

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

### Rules to Follow

✅ **DO:**
- Use day numbers (1-31)
- Use any separator (comma, dash, "and", "&")
- Enter dates in correct month column
- Use ranges for consecutive days

❌ **DON'T:**
- Include month names in data
- Use full date formats
- Enter invalid dates (Feb 30)
- Leave employee names blank

---

## Answer 4: What if User Gives "16 to 27"?

### Step-by-Step Processing

**Input:** `16 to 27` in January Planned Leave column

**Step 1: Parse the Date String**
```
Input: "16 to 27"
↓
Regex extracts: 16, 27
↓
Creates dates: Jan 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
↓
Total: 12 dates
```

**Step 2: Filter Weekdays Only**
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

**Step 3: Check Sprint Period**
```
Sprint 3: Jan 28 - Feb 10
Leave dates: Jan 16-27
Overlap: NONE (leave is BEFORE sprint)

Leave days in Sprint 3: 0
```

**Step 4: Calculate Capacity**
```
Team: 7 members
Working days in Sprint 3: 10 days
Total person-days: 7 × 10 = 70

Leave person-days: 0 (no overlap)
Available person-days: 70 - 0 = 70

Capacity %: (70 / 70) × 100 = 100%

Result: Employee is AVAILABLE for Sprint 3
```

### Another Example: "28 to 31" in January

**Input:** `28 to 31` in January Planned Leave

**Processing:**
```
Dates: Jan 28, 29, 30, 31
Weekdays: All 4 are weekdays ✅
Sprint 3: Jan 28 - Feb 10
Overlap: ALL 4 dates are in Sprint 3 ✅

Leave days in Sprint 3: 4 days
Capacity reduction: 4 / 70 = 5.7%
```

---

## Key Takeaways

### About Date Parsing
- ✅ Program is **very flexible** with date formats
- ✅ Accepts various separators (comma, dash, "and", "&")
- ✅ Automatically removes weekends
- ✅ Handles ranges like "16 to 27"
- ✅ Removes duplicates automatically
- ✅ Skips invalid dates gracefully

### About Capacity Calculation
- ✅ Only **weekdays** count (Mon-Fri)
- ✅ Only dates **in sprint period** count
- ✅ **Planned/Optional leave** reduces capacity
- ✅ **Public holidays** don't reduce capacity
- ✅ Formula: (Available / Total) × 100

### About Data Updates
- ✅ Users can edit **locally or online**
- ✅ OneDrive **auto-syncs** changes
- ✅ Program **automatically reads** updated data
- ✅ No manual refresh needed
- ✅ Just save and run the program

---

## Documentation Available

I've created detailed documentation:

1. **DATE_FORMAT_SUMMARY.md** - Quick answers
2. **DATE_FORMAT_EXPLANATION.md** - Detailed explanation
3. **DATE_EXAMPLES.md** - Real scenarios
4. **COMPLETE_DATE_GUIDE.md** - Complete reference
5. **DATA_FORMAT_GUIDE.md** - Excel structure
6. **QUICK_REFERENCE.md** - Cheat sheet
7. **DATE_FORMAT_DOCUMENTATION_INDEX.md** - Index of all docs

---

## Bottom Line

✅ **Program is smart and flexible**
- Accepts various date formats
- Automatically handles weekends
- Filters by sprint period
- Calculates capacity accurately

✅ **Users can enter dates naturally**
- `16 to 27` works
- `1st, 4th` works
- `16-27` works
- Any format with day numbers works!

✅ **Data updates are easy**
- Edit locally or online
- OneDrive auto-syncs
- Program auto-reads changes
- No manual refresh needed

