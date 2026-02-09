# Windows Task Scheduler Setup Guide

## Overview
This guide walks you through setting up an **automated email trigger** in Windows Task Scheduler to run your sprint capacity analysis on a schedule (e.g., every Monday morning).

---

## Prerequisites

Before starting, ensure:
- ✅ `sprint_capacity_app.py` is working (test with `py sprint_capacity_app.py --analyze`)
- ✅ Email credentials are set in environment variables (`SMTP_SENDER_EMAIL`, `SMTP_SENDER_PASSWORD`, `SMTP_RECIPIENT_EMAIL`)
- ✅ Python 3.12+ is installed
- ✅ You have admin access to your computer

---

## Step 1: Create a Batch File (Wrapper Script)

Windows Task Scheduler works best with batch files. We'll create a wrapper that runs your Python script.

**File:** `run_sprint_analysis.bat`  
**Location:** `c:\Users\slatheef\Documents\Capacity Email\`

Create this file with the following content:

```batch
@echo off
REM Sprint Capacity Analysis - Automated Task Scheduler Wrapper
REM This script runs the Python application and logs output

cd /d "c:\Users\slatheef\Documents\Capacity Email"

REM Run the Python script with analysis flag
python sprint_capacity_app.py --analyze

REM Log completion
echo Task completed at %date% %time% >> sprint_capacity.log
```

**Save as:** `run_sprint_analysis.bat` (in your project root)

---

## Step 2: Open Windows Task Scheduler

1. Press **Windows Key + R**
2. Type: `taskschd.msc`
3. Press **Enter**
4. Windows Task Scheduler opens

---

## Step 3: Create a New Task

1. In Task Scheduler, click **Action** → **Create Basic Task**
2. Fill in the details:

**Name:** `Sprint Capacity Email - Weekly`  
**Description:** `Automated sprint capacity analysis and email report`  
**Location:** `\` (root)

Click **Next**

---

## Step 4: Set the Trigger (Schedule)

Choose when to run. Select one of these options:

### Option A: Every Monday at 8:00 AM (Recommended)
1. Select **Weekly**
2. Click **Next**
3. Set:
   - **Start:** Today's date
   - **Recur every:** 1 week
   - **Days:** Check only **Monday**
   - **Time:** 08:00:00 (8:00 AM)
4. Click **Next**

### Option B: Every Day at 9:00 AM
1. Select **Daily**
2. Click **Next**
3. Set:
   - **Start:** Today's date
   - **Recur every:** 1 day
   - **Time:** 09:00:00 (9:00 AM)
4. Click **Next**

### Option C: Once at a Specific Time
1. Select **One time**
2. Click **Next**
3. Set:
   - **Start:** Today's date
   - **Time:** Your preferred time
4. Click **Next**

### Option D: When Computer Starts
1. Select **When the computer starts**
2. Click **Next**
3. (No additional settings needed)
4. Click **Next**

### Option E: When You Log In
1. Select **When I log on**
2. Click **Next**
3. (No additional settings needed)
4. Click **Next**

---

## Step 5: Set the Action (Run the Batch File)

1. Select **Start a program**
2. Click **Next**
3. Fill in:
   - **Program/script:** `C:\Users\slatheef\Documents\Capacity Email\run_sprint_analysis.bat`
   - **Add arguments:** (leave empty)
   - **Start in:** `C:\Users\slatheef\Documents\Capacity Email`
4. Click **Next**

---

## Step 6: Set Conditions (Optional)

These settings help the task run reliably:

1. **Power:**
   - ☐ Uncheck "Start the task only if the computer is on AC power"
   - ☑ Check "Wake the computer to run this task"

2. **Network:**
   - ☑ Check "Start only if the following network connection is available"
   - Select your network (or "Any connection")

3. Click **Next**

---

## Step 7: Set Additional Settings

1. **General:**
   - ☑ Check "Run with highest privileges"
   - ☑ Check "Run whether user is logged in or not"

2. **Conditions:**
   - ☑ Check "Stop the task if it runs longer than: 1 hour"

3. Click **Next**

---

## Step 8: Review and Create

1. Review all settings
2. Click **Finish**
3. You may be prompted for your Windows password (required for "Run whether user is logged in or not")
4. Enter your password and click **OK**

---

## Step 9: Verify the Task

1. In Task Scheduler, find your task in the list
2. Right-click → **Properties**
3. Verify:
   - ✅ **General:** "Run with highest privileges" is checked
   - ✅ **Triggers:** Shows your schedule (e.g., "Weekly on Monday at 8:00 AM")
   - ✅ **Actions:** Shows your batch file path
4. Click **OK**

---

## Step 10: Test the Task

### Manual Test (Recommended First)

1. In Task Scheduler, find your task
2. Right-click → **Run**
3. Watch for:
   - Task status changes to "Running"
   - After 30-60 seconds, status changes to "Ready"
   - Check `reports/` folder for new files
   - Check `sprint_capacity.log` for completion message

### Verify Output

```powershell
# Check if reports were generated
dir reports\sprint_capacity_report_*.html | Sort-Object LastWriteTime -Desc | Select-Object -First 1

# Check if email template was created
dir reports\email_template_filled_*.html | Sort-Object LastWriteTime -Desc | Select-Object -First 1

# Check log file
Get-Content sprint_capacity.log | Select-Object -Last 5
```

---

## Troubleshooting

### Task Runs But No Reports Generated

**Problem:** Task shows "Completed" but no files in `reports/`

**Solutions:**
1. Check `sprint_capacity.log` for errors
2. Verify batch file path is correct
3. Run batch file manually: Double-click `run_sprint_analysis.bat`
4. Check if Python is in PATH: `python --version` in PowerShell

### Task Won't Run at Scheduled Time

**Problem:** Task doesn't execute at the scheduled time

**Solutions:**
1. Verify computer is on at scheduled time
2. Check Task Scheduler History:
   - Right-click task → **View History**
   - Look for error codes
3. Ensure "Run with highest privileges" is checked
4. Verify network connection is available

### "Access Denied" Error

**Problem:** Task fails with access denied

**Solutions:**
1. Right-click task → **Properties**
2. Go to **General** tab
3. Check "Run with highest privileges"
4. Click **OK** and enter your Windows password

### Email Not Sending

**Problem:** Reports generate but email doesn't send

**Solutions:**
1. Verify environment variables are set:
   ```powershell
   $env:SMTP_SENDER_EMAIL
   $env:SMTP_SENDER_PASSWORD
   $env:SMTP_RECIPIENT_EMAIL
   ```
2. Check if VPN is required (may not be connected when task runs)
3. See `SMTP_TROUBLESHOOTING.md` for email-specific fixes

---

## Monitoring Your Task

### View Task History

1. In Task Scheduler, select your task
2. Click **View History** (bottom right)
3. See all runs with timestamps and status

### Disable/Enable Task

- Right-click task → **Disable** (to pause)
- Right-click task → **Enable** (to resume)

### Delete Task

- Right-click task → **Delete**
- Confirm deletion

---

## Advanced: Multiple Schedules

To run at different times (e.g., Monday 8 AM AND Friday 2 PM):

1. Right-click task → **Properties**
2. Go to **Triggers** tab
3. Click **New**
4. Add another trigger with different schedule
5. Click **OK**

---

## Security Notes

✅ **Best Practices:**
- Task runs with your user credentials
- Environment variables are secure (not in batch file)
- Batch file doesn't contain passwords
- Logs are stored locally

⚠️ **Important:**
- Keep `.env` file private
- Don't share batch file if it contains sensitive info
- Regularly check Task Scheduler History for errors

---

## Quick Reference

| Action | Steps |
|--------|-------|
| Create task | Win+R → `taskschd.msc` → Action → Create Basic Task |
| Run task now | Right-click task → Run |
| View history | Right-click task → View History |
| Edit schedule | Right-click task → Properties → Triggers |
| Disable task | Right-click task → Disable |
| Delete task | Right-click task → Delete |

---

## Next Steps

1. ✅ Create `run_sprint_analysis.bat`
2. ✅ Open Task Scheduler
3. ✅ Create the task with your preferred schedule
4. ✅ Test by running manually
5. ✅ Verify reports are generated
6. ✅ Monitor Task Scheduler History

**Your automated email trigger is now ready!** 🎉

---

**Last Updated:** 2026-01-14  
**Status:** Ready to Deploy

