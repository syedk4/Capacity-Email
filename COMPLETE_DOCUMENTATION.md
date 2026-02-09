# Sprint Capacity Automation System - Complete Documentation

**Version:** 2.0  
**Last Updated:** 2026-01-20  
**System Owner:** GCC Finance Team  
**Scrum Master:** slatheef@ashleyfurniture.com

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Quick Start Guide](#quick-start-guide)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [How to Use](#how-to-use)
6. [Capacity Calculation Logic](#capacity-calculation-logic)
7. [Email Setup](#email-setup)
8. [Task Scheduler Setup](#task-scheduler-setup)
9. [Test Cases](#test-cases)
10. [Troubleshooting](#troubleshooting)
11. [File Structure](#file-structure)
12. [FAQ](#faq)

---

## System Overview

### What is This System?

The **Sprint Capacity Automation System** is a Python-based tool that automates Agile sprint capacity planning for the GCC Finance Team. It:

- ✅ Reads leave data from OneDrive-synced Excel files
- ✅ Calculates ideal and actual capacity for upcoming sprints
- ✅ Accounts for on-call duties and reduces capacity accordingly
- ✅ Generates professional reports (text, HTML, email templates)
- ✅ Sends automated emails with capacity reports
- ✅ Can be scheduled to run automatically via Windows Task Scheduler

### Key Features

1. **Automated Capacity Calculation**
   - Ideal Capacity: Theoretical maximum (no constraints)
   - Actual Capacity: Realistic capacity after leave and on-call reductions
   - Team Capacity Percentage: (Actual ÷ Ideal) × 100

2. **On-Call Support Integration**
   - Primary on-call person gets configurable hours reduction per day
   - Only applies to working days (not leave days)
   - Secondary on-call gets no reduction

3. **Professional Email Reports**
   - Modern, clean design with white header
   - Color-coded capacity metrics (green/orange/red)
   - Leave badges (red for planned, blue for holidays)
   - Email-client compatible (Outlook, Gmail)

4. **Configurable Settings**
   - Hours per day (default: 6)
   - On-call reduction hours (default: 3)
   - Sprint duration (default: 14 days)
   - Email recipients and SMTP settings

### Technology Stack

- **Python 3.12**
- **Pandas** - Excel file reading and data manipulation
- **Flask** - Web dashboard (optional)
- **SMTP** - Email automation
- **Windows Task Scheduler** - Automated execution

---

## Quick Start Guide

### For First-Time Users

1. **Install Python 3.12** (if not already installed)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the system:**
   - Edit `config.json` with your settings
   - Set up email credentials (see Email Setup section)

4. **Run the analysis:**
   ```bash
   py sprint_capacity_app.py --analyze
   ```

5. **Check the results:**
   - Reports generated in `reports/` folder
   - Email sent to configured recipients

### For Regular Users

**Option 1: Manual Run**
- Double-click `run_sprint_analysis.bat`

**Option 2: Automated Run**
- Set up Windows Task Scheduler (see Task Scheduler Setup section)

---

## Installation & Setup

### Prerequisites

- Windows 10/11
- Python 3.12 or higher
- OneDrive access to Excel file
- SMTP email access (for sending emails)

### Step-by-Step Installation

**Step 1: Install Python**
1. Download Python 3.12 from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

**Step 2: Install Dependencies**
```bash
cd "c:\Users\slatheef\Documents\Capacity Email 19012026\Capacity Email"
pip install -r requirements.txt
```

**Step 3: Configure Excel File Path**
1. Open `config.json`
2. Update `excel_file_path` to point to your OneDrive Excel file
3. Update `sheet_name` if needed (default: "Leave plans")

**Step 4: Set Up Email Credentials**
See [Email Setup](#email-setup) section below.

**Step 5: Test the System**
```bash
py sprint_capacity_app.py --analyze
```

---

## How to Use

### Running the Analysis

**Method 1: Command Line**
```bash
py sprint_capacity_app.py --analyze
```

**Method 2: Batch File**
```bash
.\run_sprint_analysis.bat
```

**Method 3: Task Scheduler**
- Set up once, runs automatically (see Task Scheduler Setup)

### Understanding the Output

**1. Console Output**
```
============================================================
SPRINT CAPACITY ANALYSIS SUMMARY
============================================================
Analysis Date: 2026-01-20 19:01:10
Team Members Analyzed: 7
Sprints Analyzed: 4
Reports Generated: reports\sprint_capacity_report_*.txt, *.html
Email Sent: Yes

🟢 Sprint 1: 96.8% capacity (Members: 7)
🟢 Sprint 2: 87.5% capacity (Members: 7)
🟢 Sprint 3: 94.3% capacity (Members: 7)
🟢 Sprint 4: 81.4% capacity (Members: 7)
============================================================
```

**2. Generated Files**
- `reports/sprint_capacity_report_*.txt` - Text report (all 4 sprints)
- `reports/sprint_capacity_report_*.html` - HTML report (all 4 sprints)
- `reports/email_template_filled_*.html` - Email template (next 2 sprints)

**3. Email**
- Sent to configured recipients
- Body: Email template with next 2 sprints
- Attachment: HTML report with all 4 sprints

---

## Capacity Calculation Logic

### Overview

The system calculates two types of capacity:

1. **Ideal Capacity** - Theoretical maximum (no constraints)
2. **Actual Capacity** - Realistic capacity (after all reductions)

### Formulas

#### Ideal Capacity
```
Ideal Capacity = Total Members × Working Days × Hours Per Day
```

**Example:**
```
7 members × 10 working days × 6 hours/day = 420 hours
```

**Important:** Ideal Capacity is NEVER reduced by:
- ❌ Leave
- ❌ On-call duties
- ❌ Any other constraints

#### Actual Capacity
```
Step 1: Base Capacity = Total Members × Working Days × Hours Per Day
Step 2: Subtract Leave = Base - (Leave Days × Hours Per Day)
Step 3: Subtract On-Call = Result from Step 2 - (On-Call Days × Reduction Hours)
Final: Actual Capacity
```

**Example (Sprint 3):**
```
Step 1: Base = 7 × 10 × 6 = 420 hours
Step 2: Leave = 4 person-days × 6 = 24 hours
        After leave = 420 - 24 = 396 hours
Step 3: On-Call (Siva Guru) = 10 days × 3 hours = 30 hours
        Actual = 396 - 30 = 366 hours
```

#### Team Capacity Percentage
```
Team Capacity % = (Actual Capacity ÷ Ideal Capacity) × 100
```

**Example:**
```
(366 ÷ 420) × 100 = 87.1%
```

### On-Call Reduction Logic

**Rules:**
1. ✅ Only PRIMARY on-call person gets reduction
2. ✅ Secondary on-call gets NO reduction
3. ✅ Reduction only applies to WORKING days (not leave days)
4. ✅ Reduction is configurable (default: 3 hours/day)
5. ✅ Can be disabled by setting `oncall_primary_hours_reduction: 0`

**Rationale:**
- On-call person works 6 hours/day total
- 3 hours/day for support activities (NOT counted in JIRA sprint)
- 3 hours/day for development work (counted in JIRA sprint capacity)

**Example:**
```
Siva Guru (Primary On-Call) in Sprint 3:
- Working days: 10
- On-call reduction: 10 × 3 = 30 hours
- Sprint capacity: 60 - 30 = 30 hours (only development work)
```

### Working Days Calculation

**Excluded from working days:**
- ✅ Saturdays and Sundays (weekends)
- ✅ GCC public holidays (from config.json)

**Example:**
```
Sprint: Jan 28 - Feb 10 (14 calendar days)
Weekends: 4 days (2 Saturdays + 2 Sundays)
GCC Holidays: 0 days
Working Days: 14 - 4 - 0 = 10 days
```

### Leave Handling

**Types of Leave:**
1. **Planned Leave** - Shown in red badges
2. **Optional Holiday (GCC)** - Shown in blue badges

**Leave Calculation:**
- Only weekday leave counts (Monday-Friday)
- Weekend leave is ignored
- GCC holidays are already excluded from working days

---

## Email Setup

### SMTP Configuration

**For Office 365 / Outlook:**

1. **Update config.json:**
```json
{
  "email_settings": {
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587,
    "sender_email": "DONOTREPLY@ashleyfurniture.com",
    "scrum_master_email": "slatheef@ashleyfurniture.com"
  }
}
```

2. **Set up email credentials:**
```bash
py setup_email_credentials.py
```

3. **Enter credentials when prompted:**
   - Email: DONOTREPLY@ashleyfurniture.com
   - Password: [Your password]

**Security Note:** Credentials are stored in Windows Credential Manager (secure).

### Email Template Design

**Features:**
- ✅ White header with black text (no gradients)
- ✅ Table-based layouts (email client compatible)
- ✅ Color-coded capacity metrics:
  - Green: ≥ 90%
  - Orange: 80-89%
  - Red: < 80%
- ✅ Leave badges:
  - Red: Planned leave
  - Blue: GCC holidays
- ✅ Yellow highlighting for team members on leave

**Email Body vs Attachment:**
- **Email Body:** Next 2 sprints only (Sprint 3 & 4)
- **HTML Attachment:** All 4 sprints (Sprint 1-4)

### Troubleshooting Email Issues

**Problem: Email not sending**

**Solution 1: Check SMTP settings**
```bash
# Test SMTP connection
py -c "import smtplib; smtplib.SMTP('smtp.office365.com', 587).starttls()"
```

**Solution 2: Verify credentials**
```bash
py setup_email_credentials.py
```

**Solution 3: Check firewall**
- Ensure port 587 is not blocked
- Check corporate firewall settings

**Problem: Email displays incorrectly**

**Solution:** Email uses table-based layouts for compatibility. If issues persist:
1. Check in Outlook desktop client
2. Check in Gmail web interface
3. Verify HTML attachment renders correctly

---

## Task Scheduler Setup

### Automated Weekly Execution

Set up Windows Task Scheduler to run the analysis automatically every week.

**Step 1: Open Task Scheduler**
1. Press `Win + R`
2. Type `taskschd.msc`
3. Press Enter

**Step 2: Create New Task**
1. Click "Create Task" (not "Create Basic Task")
2. Name: "Sprint Capacity Analysis"
3. Description: "Automated sprint capacity report generation"
4. Check "Run whether user is logged on or not"
5. Check "Run with highest privileges"

**Step 3: Configure Trigger**
1. Go to "Triggers" tab
2. Click "New"
3. Begin the task: "On a schedule"
4. Settings: "Weekly"
5. Select day: Monday (or your preferred day)
6. Time: 8:00 AM (or your preferred time)
7. Click "OK"

**Step 4: Configure Action**
1. Go to "Actions" tab
2. Click "New"
3. Action: "Start a program"
4. Program/script: `C:\Windows\System32\cmd.exe`
5. Add arguments: `/c "c:\Users\slatheef\Documents\Capacity Email 19012026\Capacity Email\run_sprint_analysis.bat"`
6. Start in: `c:\Users\slatheef\Documents\Capacity Email 19012026\Capacity Email`
7. Click "OK"

**Step 5: Configure Conditions**
1. Go to "Conditions" tab
2. Uncheck "Start the task only if the computer is on AC power"
3. Check "Wake the computer to run this task" (optional)

**Step 6: Configure Settings**
1. Go to "Settings" tab
2. Check "Allow task to be run on demand"
3. Check "Run task as soon as possible after a scheduled start is missed"
4. If task fails, restart every: 10 minutes
5. Attempt to restart up to: 3 times

**Step 7: Save and Test**
1. Click "OK"
2. Enter your Windows password if prompted
3. Right-click the task → "Run" to test

### Verify Automated Run

**Check the log file:**
```bash
Get-Content "c:\Users\slatheef\Documents\Capacity Email 19012026\Capacity Email\sprint_capacity.log" -Tail 20
```

**Expected log entry:**
```
============================================================================
Task started at 20-01-2026 08:00:00
============================================================================
[... analysis logs ...]
Task completed successfully at 20-01-2026 08:00:15
Exit code: 0
============================================================================
```

---

## Test Cases

### Critical Test Cases

**TC-001: Ideal Capacity Calculation**
```
Objective: Verify Ideal Capacity is calculated correctly WITHOUT any reductions

Test Steps:
1. Run: py sprint_capacity_app.py --analyze
2. Check Sprint 3 report
3. Verify: Ideal Capacity = 7 × 10 × 6 = 420 hours

Expected: Ideal Capacity is NOT reduced by leave or on-call
Status: ✅ Pass / ❌ Fail
```

**TC-002: Actual Capacity with On-Call**
```
Objective: Verify Actual Capacity calculation when on-call reduction is applied

Preconditions: oncall_primary_hours_reduction: 3 in config.json

Test Steps:
1. Check Sprint 3 (On-Call Primary: Siva Guru)
2. Verify calculation

Expected Results:
Base = 420 hours
Leave = 24 hours (4 person-days × 6)
After leave = 396 hours
On-call reduction = 30 hours (10 days × 3)
Actual = 366 hours

Status: ✅ Pass / ❌ Fail
```

**TC-003: Team Capacity Percentage**
```
Objective: Verify Team Capacity % is calculated based on final Actual Capacity

Test Steps:
1. Check Sprint 3
2. Verify: Team Capacity % = (366 ÷ 420) × 100 = 87.1%

Important: Percentage must be calculated AFTER on-call reduction

Status: ✅ Pass / ❌ Fail
```

**TC-004: On-Call Name Matching**
```
Objective: Verify system correctly matches on-call names with employee names

Test Data:
- "Siva Guru" matches "Sampanthamoorthy, Sivaguru" ✅
- "Lakshmipathy" matches "Murugan, Lakshmipathy" ✅
- "Pavithra" matches "Murugan Pavithra" ✅

Status: ✅ Pass / ❌ Fail
```

**TC-005: On-Call Reduction Only for Primary**
```
Objective: Verify on-call reduction is applied ONLY to Primary, not Secondary

Test Steps:
1. Check Sprint 3 (Primary: Siva Guru, Secondary: Dhivya Dharmaraj)
2. Verify only Siva Guru gets reduction

Expected:
- Siva Guru: 30 hours reduction ✅
- Dhivya Dharmaraj: No reduction ✅

Status: ✅ Pass / ❌ Fail
```

**TC-006: Regression - Ideal Capacity Never Reduced**
```
Objective: Ensure Ideal Capacity is NEVER reduced by any factor

Test Steps:
1. Run analysis for all sprints
2. Check Ideal Capacity for each sprint

Expected: Ideal Capacity = Total Members × Working Days × Hours Per Day

Never reduced by:
- ❌ Leave
- ❌ On-call reduction
- ❌ Any other factor

Status: ✅ Pass / ❌ Fail
```

### Full Test Suite

For complete test documentation with 32 detailed test cases, see `TEST_CASES.md`.

---

## Troubleshooting

### Common Issues and Solutions

**Issue 1: Excel file not found**

**Error:**
```
FileNotFoundError: Excel file not found
```

**Solution:**
1. Check `excel_file_path` in config.json
2. Ensure OneDrive is synced
3. Verify file path is correct (use double backslashes `\\`)

---

**Issue 2: Sheet not found**

**Error:**
```
Sheet 'Leave plans' not found
```

**Solution:**
1. Open Excel file and check sheet names
2. Update `sheet_name` in config.json (case-sensitive)
3. Common sheet names: "Leave plans", "2026", "Team Info"

---

**Issue 3: On-call reduction not applied**

**Symptoms:**
- Actual Capacity higher than expected
- Team Capacity % higher than expected

**Solution:**
1. Check `oncall_primary_hours_reduction` in config.json
2. Verify it's set to 3 (not 0)
3. Check on-call name matches employee name
4. Verify "On Call Schedules" sheet exists

---

**Issue 4: Email not sending**

**Error:**
```
SMTPAuthenticationError: Authentication failed
```

**Solution:**
1. Run: `py setup_email_credentials.py`
2. Re-enter email credentials
3. Check SMTP settings in config.json
4. Verify email account has SMTP access enabled

---

**Issue 5: Incorrect capacity percentage**

**Symptoms:**
- Sprint 3 shows 94.3% instead of 87.1%

**Root Cause:**
- `oncall_primary_hours_reduction` is set to 0

**Solution:**
1. Open config.json
2. Change `"oncall_primary_hours_reduction": 0` to `"oncall_primary_hours_reduction": 3`
3. Run analysis again

---

**Issue 6: Unicode encoding error in logs**

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solution:**
- This is a cosmetic issue with emoji characters in logs
- Does not affect functionality
- Reports and emails are generated correctly
- Can be ignored

---

## File Structure

### Main Files

```
Capacity Email/
├── sprint_capacity_app.py          # Main application
├── config.json                     # Configuration file
├── requirements.txt                # Python dependencies
├── run_sprint_analysis.bat         # Windows batch file
├── setup_email_credentials.py      # Email setup utility
├── COMPLETE_DOCUMENTATION.md       # This file
├── TEST_CASES.md                   # Detailed test cases
├── README.md                       # Quick reference
└── reports/                        # Generated reports
    ├── sprint_capacity_report_*.txt
    ├── sprint_capacity_report_*.html
    └── email_template_filled_*.html
```

### Configuration Files

| File | Purpose |
|------|---------|
| `config.json` | Main configuration (paths, settings, holidays) |
| `requirements.txt` | Python package dependencies |

### Script Files

| File | Purpose |
|------|---------|
| `sprint_capacity_app.py` | Main application (2200+ lines) |
| `run_sprint_analysis.bat` | Windows batch wrapper for automation |
| `setup_email_credentials.py` | Email credential setup utility |

### Documentation Files

| File | Purpose |
|------|---------|
| `COMPLETE_DOCUMENTATION.md` | Consolidated documentation (this file) |
| `TEST_CASES.md` | 32 detailed test cases |
| `README.md` | Quick start guide |

### Generated Files

| File | Purpose |
|------|---------|
| `reports/*.txt` | Text reports (all 4 sprints) |
| `reports/*.html` | HTML reports (all 4 sprints) |
| `reports/email_template_*.html` | Email templates (next 2 sprints) |
| `sprint_capacity.log` | Application log file |

---

## FAQ

### General Questions

**Q: How often should I run the analysis?**

A: Recommended weekly (e.g., every Monday morning). Set up Task Scheduler for automation.

---

**Q: Can I change the sprint duration?**

A: Yes, edit `sprint_duration_days` in config.json. Default is 14 days (2 weeks).

---

**Q: Can I change the hours per day?**

A: Yes, edit `hours_per_day` in config.json. Default is 6 hours.

---

**Q: What if I don't want on-call reduction?**

A: Set `oncall_primary_hours_reduction: 0` in config.json.

---

### Capacity Calculation Questions

**Q: Why is Ideal Capacity not reduced by on-call?**

A: Ideal Capacity represents the theoretical maximum with no constraints. It's used as a baseline to calculate the Team Capacity percentage. Only Actual Capacity is reduced.

---

**Q: Why does the on-call person only get 3 hours/day for development?**

A: The on-call person works 6 hours/day total:
- 3 hours for support activities (not counted in JIRA sprint)
- 3 hours for development work (counted in JIRA sprint capacity)

This reflects the reality that on-call duties take time away from development work.

---

**Q: Why doesn't the secondary on-call person get a reduction?**

A: Based on team practice, only the primary on-call person has significant support responsibilities. The secondary is backup only.

---

**Q: How are GCC holidays handled?**

A: GCC holidays are excluded from working days entirely. They don't count as leave and don't reduce capacity beyond the working days calculation.

---

### Technical Questions

**Q: Can I run this on Mac or Linux?**

A: The Python script is cross-platform, but the batch file is Windows-only. On Mac/Linux, run the Python script directly:
```bash
python3 sprint_capacity_app.py --analyze
```

---

**Q: Where are email credentials stored?**

A: In Windows Credential Manager (secure). Use `setup_email_credentials.py` to update them.

---

**Q: Can I customize the email template?**

A: Yes, but it requires editing the `generate_email_template()` function in `sprint_capacity_app.py`. The current design is optimized for email client compatibility.

---

**Q: How do I add more GCC holidays?**

A: Edit the `gcc_holidays` array in config.json:
```json
{
  "gcc_holidays": [
    "2026-01-01",
    "2026-01-15",
    "2026-01-26",
    "2026-04-14"
  ]
}
```

---

### Data Questions

**Q: What Excel format is required?**

A: The system expects:
- **Leave plans sheet:** Columns for Emp Id, Emp Name, and date columns (Jan, Feb, etc.)
- **On Call Schedules sheet:** Columns for Start Date, End Date, Primary, Secondary

---

**Q: Can I use a different Excel file?**

A: Yes, update `excel_file_path` in config.json. The file must follow the same format.

---

**Q: What if an employee name doesn't match?**

A: The system uses fuzzy matching:
- "Siva Guru" matches "Sampanthamoorthy, Sivaguru"
- "Lakshmipathy" matches "Murugan, Lakshmipathy"

If matching fails, check the on-call name spelling in the Excel file.

---

## Support and Contact

### Getting Help

**For technical issues:**
1. Check this documentation
2. Check `TEST_CASES.md` for test scenarios
3. Check `sprint_capacity.log` for error messages
4. Contact: slatheef@ashleyfurniture.com

### Reporting Bugs

When reporting bugs, include:
1. Error message (from console or log file)
2. Steps to reproduce
3. Expected vs actual behavior
4. Screenshots (if applicable)

### Feature Requests

Submit feature requests to: slatheef@ashleyfurniture.com

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-01-20 | Fixed on-call reduction bug, updated documentation |
| 1.5 | 2026-01-14 | Added email template, modern design |
| 1.0 | 2026-01-13 | Initial release with basic capacity calculation |

---

## License and Credits

**Developed for:** GCC Finance Team, Ashley Furniture Industries, Inc.
**System Owner:** slatheef@ashleyfurniture.com
**Last Updated:** 2026-01-20

---

**END OF DOCUMENTATION**

## Configuration

### config.json Structure

```json
{
  "sprint_start_date": "2025-12-31",
  "sprint_duration_days": 14,
  "hours_per_day": 6,
  "oncall_primary_hours_reduction": 3,
  "excel_file_path": "C:\\Users\\slatheef\\Ashley Furniture Industries, Inc\\IT - Finance - India Finance Team Daily Updates\\2026- India Finance team Daily work status.xlsx",
  "sheet_name": "Leave plans",
  "oncall_sheet_name": "On Call Schedules",
  "gcc_holidays": [
    "2026-01-01",
    "2026-01-15",
    "2026-01-26"
  ],
  "email_settings": {
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587,
    "sender_email": "DONOTREPLY@ashleyfurniture.com",
    "scrum_master_email": "slatheef@ashleyfurniture.com"
  }
}
```

### Configuration Parameters

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `sprint_start_date` | First sprint start date | "2025-12-31" | Format: YYYY-MM-DD |
| `sprint_duration_days` | Sprint length in days | 14 | 2-week sprints |
| `hours_per_day` | Working hours per day | 6 | Used for capacity calculation |
| `oncall_primary_hours_reduction` | On-call reduction per day | 3 | Set to 0 to disable |
| `excel_file_path` | Path to Excel file | OneDrive path | Must be accessible |
| `sheet_name` | Leave data sheet name | "Leave plans" | Case-sensitive |
| `oncall_sheet_name` | On-call schedule sheet | "On Call Schedules" | Case-sensitive |
| `gcc_holidays` | List of GCC holidays | Array of dates | Format: YYYY-MM-DD |

---


