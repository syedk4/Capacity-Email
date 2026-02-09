# 🚀 Quick Reference - Data Format Cheat Sheet

## File Location
```
C:\Users\slatheef\Ashley Furniture Industries, Inc\IT - Finance - India Finance Team Daily Updates\2026- India Finance team Daily work status.xlsx
```

---

## Sheet 1: "Leave plans" - Required Columns

| Column | Format | Example | Notes |
|--------|--------|---------|-------|
| **Emp Id** | Any unique ID | `200071` | Required |
| **Emp Name** | Full name | `John Doe` | Must match On Call sheet |
| **January** | Day numbers | `1st, 4th` | Month columns (auto-detected) |
| **February** | Day numbers | `15th` | Can be blank |
| **March** | Day numbers | `10th, 11th` | Can be blank |
| **Opting?** | Yes/No | `Yes` | Optional holiday opt-in |

### Date Format Examples ✅
```
1st, 4th          ✅ Multiple dates with suffix
1, 4              ✅ Plain numbers
1st & 4th         ✅ With ampersand
1st and 4th       ✅ With "and"
15th              ✅ Single date
-                 ✅ No leave
(blank)           ✅ No leave
```

### Date Format Examples ❌
```
Jan 1st           ❌ Don't include month name
2026-01-01        ❌ Don't use full dates
Jan 1 - Jan 4     ❌ Don't use ranges with month
```

---

## Sheet 2: "On Call Schedules" - Required Columns

| Column | Format | Example | Notes |
|--------|--------|---------|-------|
| **Month** | Month name | `January` | Auto-detected |
| **From Date** | Day number | `14th` | Required |
| **To date** | Day number | `27th` | If < from_day, assumes next month |
| **Primary** | Employee name | `Lakshmipathy` | Must match Leave plans sheet |
| **Secondary** | Employee name | `BindhuMadhuri` | Backup on-call person |

---

## How to Update Data

### Step 1: Open File
- Open from OneDrive or local folder
- File auto-syncs between cloud and computer

### Step 2: Edit Data
- **Leave plans sheet:** Update leave dates in month columns
- **On Call Schedules sheet:** Update on-call assignments

### Step 3: Save
- Press Ctrl+S
- OneDrive auto-syncs

### Step 4: Run Program
- Program automatically reads updated data
- No manual refresh needed

---

## Important Rules

✅ **DO:**
- Use day numbers only (1st, 15th, 28th)
- Match employee names exactly between sheets
- Keep column headers in first row
- Use month names for column headers

❌ **DON'T:**
- Include month names in data cells
- Use full dates (2026-01-01)
- Leave employee names blank
- Change column header names

---

## Example Data

### Leave plans Sheet
```
Emp Id | Emp Name | January | February | March | Opting?
200071 | John Doe | 1st, 4th | 15th | - | Yes
200325 | Jane Smith | 28th, 29th | - | 10th | No
```

### On Call Schedules Sheet
```
Month | From Date | To date | Primary | Secondary
January | 14th | 27th | John Doe | Jane Smith
February | 11th | 24th | Jane Smith | John Doe
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No employees found | Missing headers | Add `Emp Id` and `Emp Name` in first row |
| Dates not parsing | Wrong format | Use day numbers only (1st, 15th) |
| On-call not showing | Name mismatch | Check spelling in both sheets |
| File not found | Wrong path | Update `excel_file_path` in config.json |

---

## Program Behavior

- **Reads:** Excel file from local computer (OneDrive synced)
- **Parses:** Employee names, leave dates, on-call schedules
- **Calculates:** Sprint capacity percentages
- **Generates:** Email reports with next 2 sprints
- **Sends:** Email to scrum master + additional recipients
- **Logs:** All details in `sprint_capacity.log`

---

## Key Points

1. **OneDrive Sync:** File is automatically synced to your computer
2. **Flexible Dates:** Program handles various date formats
3. **Auto-Detection:** Sheets and columns are auto-detected
4. **Name Matching:** Employee names must match between sheets
5. **No Manual Refresh:** Just save and run the program

---

## Need Help?

Check these files:
- `DATA_FORMAT_GUIDE.md` - Detailed format guide
- `sprint_capacity.log` - Program logs with parsing details
- `config.json` - Configuration settings

