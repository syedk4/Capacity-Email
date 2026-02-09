# 🎯 YOUR NEW WORKFLOW - AFTER SETUP

**Date:** January 14, 2026  
**Purpose:** How to use the system going forward

---

## 📋 WHAT CHANGED

### Before Setup
```
❌ Password in config.json (risky)
❌ Code might expose credentials
❌ Email sending uncertain
```

### After Setup (NOW)
```
✅ Password in .env (secure)
✅ Code reads from .env safely
✅ Email templates ready to send
```

---

## 🚀 YOUR NEW WORKFLOW

### Every Time You Need Sprint Reports

**Step 1: Run the Application**
```powershell
py sprint_capacity_app.py --analyze
```

**Step 2: Get Your Reports**
```
✅ Text report: sprint_capacity_report_YYYYMMDD_HHMMSS.txt
✅ HTML report: sprint_capacity_report_YYYYMMDD_HHMMSS.html
✅ Email template: email_template_filled_YYYYMMDD_HHMMSS.html
```

**Step 3: Send Email**

Option A - Automatic (if SMTP works):
- Email sends automatically during run
- Check output for "Email Sent: Yes"

Option B - Manual (recommended for now):
1. Go to `reports/` folder
2. Find latest `email_template_filled_*.html`
3. Open in browser
4. Copy all content (Ctrl+A, Ctrl+C)
5. Open Outlook
6. New Email
7. Paste content (Ctrl+V)
8. Add subject: "Sprint Capacity Report - [Date]"
9. Send

---

## 📊 SAMPLE RUN WALKTHROUGH

### Command
```powershell
cd "c:\Users\slatheef\Documents\Capacity Email"
py sprint_capacity_app.py --analyze
```

### Output You'll See
```
✅ Starting sprint capacity analysis...
✅ Loaded Excel file with 7 team members
✅ Parsed leave schedules
✅ Parsed on-call schedules
✅ Generated reports:
   - sprint_capacity_report_20260114_143805.txt
   - sprint_capacity_report_20260114_143805.html
   - email_template_filled_20260114_143805.html
✅ Analysis completed successfully!
```

### Reports You Get
```
reports/
├── sprint_capacity_report_20260114_143805.txt      ← Text version
├── sprint_capacity_report_20260114_143805.html     ← Web version
└── email_template_filled_20260114_143805.html      ← Email ready!
```

---

## 📧 SENDING THE EMAIL

### Method 1: Automatic (If SMTP Works)

**Setup:** Already done! Just run the app.

**What happens:**
1. App generates reports
2. App tries to send email
3. If successful: "Email Sent: Yes"
4. If fails: "Email Sent: No"

### Method 2: Manual Using Template (Recommended Now)

**Step 1: Find Latest Template**
```powershell
# PowerShell - find latest email template
cd reports
dir email_template_filled_*.html | Sort-Object LastWriteTime | Select-Object -Last 1
```

**Step 2: Open Template**
```
Double-click: email_template_filled_20260114_143805.html
Browser opens: Shows professional sprint report
```

**Step 3: Copy Content**
```
Ctrl+A  → Select all
Ctrl+C  → Copy
```

**Step 4: Paste in Outlook**
```
Outlook → New Email
Paste (Ctrl+V) → Content appears
Add To: recipient@company.com
Subject: Sprint Capacity Report - Jan 14, 2026
Send!
```

---

## 🔐 SECURITY REMINDERS

### What's Protected Now
✅ Your password is in `.env`
✅ `.env` is in `.gitignore`
✅ Credentials never exposed
✅ Code is safe for git

### What You Should Do
✅ Keep `.env` file private
✅ Never share `.env`
✅ Never commit `.env` to git (already prevented)
✅ If `.env` exposed, change password

### If Password Changes
If Ashley Furniture changes your email password:
1. Update `.env` with new password
2. Save file
3. Restart IDE
4. Run app again

---

## 📝 COMMAND REFERENCE

### Run Full Analysis
```powershell
py sprint_capacity_app.py --analyze
```

### Find Latest Email Template
```powershell
cd reports
Get-ChildItem email_template_filled_*.html | Sort-Object LastWriteTime -Desc | Select-Object -First 1
```

### View Latest Text Report
```powershell
cd reports
Get-Content (Get-ChildItem sprint_capacity_report_*.txt | Sort-Object LastWriteTime -Desc | Select-Object -First 1).FullName
```

### Quick Browser View
```powershell
cd reports
Invoke-Item (Get-ChildItem sprint_capacity_report_*.html | Sort-Object LastWriteTime -Desc | Select-Object -First 1).FullName
```

---

## 🔍 WHAT YOU CAN FIND

### Email Template Content
- Sprint numbers and dates
- Team capacity percentages
- On-call assignments
- Professional HTML formatting
- Ready to forward to stakeholders

### Text Report Content
- Detailed sprint analysis
- Capacity breakdown
- On-call schedules
- Leave information

### HTML Report Content
- Formatted version of text report
- Charts and visualizations
- Professional presentation
- Easy to read on screen

---

## ❓ COMMON SCENARIOS

### Scenario 1: Email Didn't Send Automatically
**What to do:**
1. Use manual email template method
2. Check SMTP_TROUBLESHOOTING.md for fixes
3. Connect to VPN if required

### Scenario 2: Report Shows Wrong Sprint
**What to do:**
1. Check `config.json` for `sprint_start_date`
2. Ensure it's set to: `"2025-12-31"`
3. Application auto-calculates from there

### Scenario 3: Team Members Missing
**What to do:**
1. Check Excel file: `2026- India Finance team Daily work status.xlsx`
2. Verify `Leave plans` sheet has data
3. Run app again

### Scenario 4: Password Changed at Company
**What to do:**
1. Update `.env` file: `GMAIL_SENDER_PASSWORD=new-password`
2. Save file
3. Restart IDE
4. Run app again

---

## 🎯 SUCCESS METRICS

### You'll Know It's Working When:
✅ Application starts without errors
✅ Excel file loads with 7 team members
✅ Reports generate in `reports/` folder
✅ Email template is created
✅ Summary shows sprint info and on-calls

### You'll Know Email Works When:
✅ Output says: "Email Sent: Yes"
   OR
✅ You manually send and recipient gets it

---

## 📈 RECURRING USE

### Weekly Report Generation
```
Monday: py sprint_capacity_app.py --analyze
Send report to team
```

### Biweekly Update
```
Every 2 weeks before sprint review
Generate fresh reports
Share with stakeholders
```

### On-Demand Analysis
```
Anytime: py sprint_capacity_app.py --analyze
Get current sprint status
```

---

## 🔧 IF SOMETHING BREAKS

### Application Won't Start
```
1. Check Python installed: py --version
2. Check working directory correct
3. Check Excel file exists and has data
```

### Can't Find Reports
```
1. Check: reports/ folder exists
2. Run: py sprint_capacity_app.py --analyze
3. Look in: c:\Users\slatheef\Documents\Capacity Email\reports\
```

### Email Won't Send
```
1. Check SMTP_TROUBLESHOOTING.md
2. Verify VPN connected
3. Use manual template sending as workaround
```

### Wrong Sprints Showing
```
1. Verify sprint_start_date in config.json
2. Should be: "2025-12-31"
3. Application calculates from that date
```

---

## ✅ PRE-RUN CHECKLIST

Before running the application each time:
- [ ] On VPN if required
- [ ] Excel file exists and has data
- [ ] `.env` file has credentials
- [ ] At least 1 GB free disk space
- [ ] Python 3.12 or higher installed

---

## 📚 QUICK REFERENCE

| Task | Command |
|------|---------|
| Run analysis | `py sprint_capacity_app.py --analyze` |
| View latest report | Open `reports/sprint_capacity_report_*.html` in browser |
| Check latest email | Open `reports/email_template_filled_*.html` in browser |
| Find password location | Check `.env` file (keep it private!) |
| Update credentials | Edit `.env` and save |
| Verify config | Check `config.json` |

---

## 🎉 YOU'RE ALL SET!

Your system is now:
- 🔒 Secure
- ✅ Working
- 📧 Ready to email
- 🎯 Production-ready

**Just run the command and you're done!** 🚀

```powershell
py sprint_capacity_app.py --analyze
```

---

**Last Updated:** 2026-01-14  
**Status:** Ready for Production Use  
**Next:** Run the command above anytime you need sprint reports!
