# 📊 Data Format Guide - How the Program Reads Your OneDrive File

## Overview

The program reads data from an **Excel file stored on OneDrive** and automatically parses it to calculate team capacity for sprint planning.

**Your File Location:**
```
C:\Users\slatheef\Ashley Furniture Industries, Inc\IT - Finance - India Finance Team Daily Updates\2026- India Finance team Daily work status.xlsx
```

---

## How the Program Reads Data

### Step 1: File Access
- The program reads the Excel file directly from your OneDrive folder
- OneDrive syncs the file to your local computer, so the program accesses it locally
- **No internet connection needed** once the file is synced

### Step 2: Sheet Detection
The program looks for specific sheets in your Excel file:

| Sheet Name | Purpose | Required? |
|-----------|---------|-----------|
| **Leave plans** | Employee leave data | ✅ Yes |
| **On Call Schedules** | On-call rotation data | ✅ Yes |
| Other sheets | Ignored | ❌ No |

### Step 3: Data Parsing
The program automatically:
1. **Detects employee information** from the "Leave plans" sheet
2. **Extracts leave dates** from various columns
3. **Parses on-call schedules** from the "On Call Schedules" sheet
4. **Calculates sprint capacity** based on leave data

---

## Required Format: "Leave plans" Sheet

### Column Structure

Your "Leave plans" sheet must have these columns:

```
| Emp Id | Emp Name | [Month Columns] | Opting? |
```

**Example:**
```
| Emp Id | Emp Name | January | February | March | Opting? |
|--------|----------|---------|----------|-------|---------|
| 200071 | John Doe | 1st, 4th | 15th | - | Yes |
| 200325 | Jane Smith | 28th, 29th | - | 10th | No |
```

### Column Details

#### 1. **Emp Id** (Employee ID)
- **Format:** Any unique identifier (number or text)
- **Example:** `200071`, `EMP001`, `John_Doe`
- **Required:** ✅ Yes

#### 2. **Emp Name** (Employee Name)
- **Format:** Full name as text
- **Example:** `John Doe`, `Jane Smith`
- **Required:** ✅ Yes

#### 3. **Month Columns** (January, February, etc.)
- **Format:** Day numbers with optional suffixes
- **Examples:**
  - `1st, 4th` (multiple dates)
  - `15th` (single date)
  - `28th & 29th` (with ampersand)
  - `10, 11, 12` (without suffixes)
  - Leave blank or `-` for no leave
- **Required:** ✅ Yes (at least one month)

#### 4. **Opting?** (Optional Holiday Opt-in)
- **Format:** `Yes` or `No`
- **Purpose:** Indicates if employee is taking optional holidays
- **Example:** `Yes` means include optional holiday dates in capacity calculation
- **Required:** ❌ Optional

### Date Format Rules

The program is **flexible with date formats**:

✅ **Accepted Formats:**
- `1st, 4th` (with ordinal suffixes)
- `1, 4` (plain numbers)
- `1st & 4th` (with ampersand)
- `1st and 4th` (with "and")
- `1-4` (range - will parse as individual dates)
- `15th` (single date)
- Spaces don't matter: `1st , 4th` works fine

❌ **NOT Accepted:**
- `Jan 1st` (month names in data cells - use column headers instead)
- `2026-01-01` (full dates - use day numbers only)
- Empty cells are fine (treated as no leave)

---

## Required Format: "On Call Schedules" Sheet

### Column Structure

```
| Month | From Date | To date | Primary | Secondary |
```

**Example:**
```
| Month | From Date | To date | Primary | Secondary |
|-------|-----------|---------|---------|-----------|
| January | 14th | 27th | Lakshmipathy | BindhuMadhuri |
| February | 11th | 24th | Suresh Mahalingam | Pavithra |
```

### Column Details

#### 1. **Month**
- **Format:** Month name (January, February, etc.)
- **Example:** `January`, `Feb`, `March`
- **Required:** ✅ Yes

#### 2. **From Date**
- **Format:** Day number with optional suffix
- **Example:** `14th`, `1st`, `28`
- **Required:** ✅ Yes

#### 3. **To date**
- **Format:** Day number with optional suffix
- **Example:** `27th`, `31st`, `10`
- **Note:** If day < from_day, program assumes next month
- **Required:** ✅ Yes

#### 4. **Primary**
- **Format:** Employee name (must match name in "Leave plans" sheet)
- **Example:** `Lakshmipathy`, `Siva Guru`
- **Required:** ✅ Yes

#### 5. **Secondary**
- **Format:** Employee name (backup on-call person)
- **Example:** `BindhuMadhuri Maddela`, `Dhivya Dharmaraj`
- **Required:** ✅ Yes

---

## How to Update Your Data

### Method 1: Direct Edit in Excel
1. Open the Excel file from OneDrive
2. Edit the "Leave plans" sheet:
   - Add/remove leave dates in month columns
   - Update "Opting?" column for optional holidays
3. Edit the "On Call Schedules" sheet:
   - Update on-call assignments
4. **Save the file** (Ctrl+S)
5. Run the program - it will automatically read the updated data

### Method 2: Update via OneDrive Web
1. Go to OneDrive.com
2. Navigate to the file
3. Click "Edit in Excel Online"
4. Make changes
5. Changes auto-save

### Method 3: Sync and Edit Locally
1. OneDrive automatically syncs changes
2. Edit locally in Excel
3. Save - OneDrive syncs to cloud

---

## Important Notes

⚠️ **Keep These in Mind:**

1. **Employee Names Must Match**
   - Names in "Leave plans" sheet must exactly match names in "On Call Schedules" sheet
   - Example: If you write "John Doe" in one sheet, don't write "John D." in another

2. **Column Headers Matter**
   - First row should contain headers: `Emp Id`, `Emp Name`, month names, etc.
   - Program auto-detects these headers

3. **Month Detection**
   - Program automatically detects which month each column represents
   - Column headers should be month names (January, February, etc.)

4. **Year Handling**
   - Program uses current year automatically
   - For dates in past months, it still processes them (for historical reports)

5. **Weekends & Holidays**
   - Program automatically excludes weekends (Saturday, Sunday)
   - GCC holidays are marked as "public_holiday" and don't reduce capacity

---

## Example: Complete Data Setup

### Leave plans Sheet
```
Emp Id | Emp Name | January | February | March | Opting?
200071 | John Doe | 1st, 4th | 15th | - | Yes
200325 | Jane Smith | 28th, 29th | - | 10th | No
200456 | Bob Wilson | - | 11th, 12th | 5th, 6th | Yes
```

### On Call Schedules Sheet
```
Month | From Date | To date | Primary | Secondary
January | 14th | 27th | John Doe | Jane Smith
February | 11th | 24th | Bob Wilson | John Doe
March | 11th | 24th | Jane Smith | Bob Wilson
```

---

## Troubleshooting

### Problem: "No employees found"
- **Cause:** Column headers not found
- **Fix:** Ensure first row has `Emp Id` and `Emp Name` columns

### Problem: Dates not parsing
- **Cause:** Wrong date format
- **Fix:** Use day numbers only (e.g., `1st`, `15th`, not `Jan 1st`)

### Problem: On-call not showing
- **Cause:** Employee names don't match between sheets
- **Fix:** Check spelling and spacing in both sheets

### Problem: File not found
- **Cause:** OneDrive not synced or path changed
- **Fix:** Check `config.json` for correct file path

---

## Questions?

The program logs all data it reads. Check `sprint_capacity.log` for details about:
- Which sheets were found
- How many employees were parsed
- Which dates were extracted
- Any parsing errors

