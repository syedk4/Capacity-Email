# Sprint Capacity Automation – Changes & System Overview (Augment Work)

**Prepared by:** Augment Agent  
**Date:** January 14, 2026  
**Audience:** New developers or support engineers joining the project

---

## 1. What This System Does Now

The **Sprint Capacity Automation System** is a Python application that:
- Reads team capacity and leave data from `CapacityUpdate.xlsx`
- Calculates 2‑week sprints starting from a configured reference date
- Computes team capacity percentages, working days, and members on leave
- Generates three types of reports for each run:
  - Plain‑text capacity report (`reports/sprint_capacity_report_*.txt`)
  - HTML capacity report for archive and attachment (`reports/sprint_capacity_report_*.html`)
  - Pre‑filled HTML email template (`reports/email_template_filled_*.html`)
- Optionally sends the report by email to the Scrum Master
- Has been fully verified to work correctly for **future dates** (e.g., Jan, Mar, Jul 2026)

All of this is wired together so that running a single command will read Excel, calculate capacity, generate reports, and (when SMTP connectivity is available) send the email.

---

## 2. Main Code Components (Python Files)

These are the key Python files and their roles as they stand **after** the Augment work:

- `sprint_capacity_app.py`
  - Main entry point for the automation.
  - Loads configuration from `config.json` and environment variables.
  - Reads `CapacityUpdate.xlsx` via `ExcelDataParser`.
  - Builds a calendar of 2‑week `Sprint` objects from a reference start date.
  - Uses `SprintCapacityCalculator` to compute capacity per sprint.
  - Generates text and HTML reports plus a filled email template file.
  - Can send the email using SMTP settings from environment variables.

- `run_capacity_analysis.py`
  - Helper script to run capacity analysis and generate reports without focusing on email.
  - Useful for quick re‑runs and debugging.

- `verify_sprint_dates.py`
  - Small utility used to verify that sprint boundaries and numbers are correct over time.
  - Supports the future‑dates testing work.

- `test_future_dates.py`, `test_full_app_future_dates.py`, `test_future_sprints_comprehensive.py`, `test_reports_emails_future_dates.py`
  - Automated tests that validate:
    - Sprint calculation logic across many future dates
    - Full application behavior (read Excel → calculate → reports → email template)
    - That the email body shows **the next 2 upcoming sprints** correctly
    - That the HTML reports always include **all 4 sprints** (previous, current, next, next+1)

- `setup_email_credentials.py`
  - Guides/implements setting email‑related environment variables securely on Windows.

- `check_sheets.py`, `detailed_excel_analysis.py`, `examine_excel.py`
  - Support scripts used to analyze the Excel structure and troubleshoot data issues.

- `web_app.py`
  - Web dashboard interface to visualize sprint capacity in a browser (optional but integrated).

---

## 3. Configuration & Security Improvements

Changes and improvements around configuration and credentials:

- **Centralized configuration** via `config.json`:
  - Stores base settings such as:
    - `sprint_start_date` (first sprint start)
    - `sprint_duration_days` (14)
    - `excel_file_path` (defaults to `CapacityUpdate.xlsx`)
  - Email settings (SMTP server, port, sender, recipient) are loaded from this file and then overridden by environment variables when present.

- **Environment‑based email settings** (no hard‑coded passwords):
  - `GMAIL_SENDER_EMAIL`
  - `GMAIL_SMTP_SERVER`
  - `GMAIL_SMTP_PORT`
  - `SCRUM_MASTER_EMAIL`
  - `GMAIL_SENDER_PASSWORD` is now **optional** and not required for the DONOTREPLY account.

- **Password removal and safer behavior** (documented in `FINAL_STATUS_REPORT.md`):
  - The previous requirement to store a password in a `.env` file has been removed.
  - The code was updated so that:
    - Password is not mandatory.
    - If no password is provided, the code skips `SMTP.login()` and relies on the internal relay.

- **Environment verification**:
  - `ENV_VERIFICATION_REPORT.md` and `ENV_VERIFICATION_SUMMARY.md` document step‑by‑step checks to ensure Python, packages, and environment variables are set correctly.

---

## 4. Email Template & Reporting Changes

The final behavior of reports and email after the Augment work:

- **Location of templates and outputs**
  - Base templates live in `Email_Templates/` (HTML and TXT versions).
  - Every run writes filled outputs under `reports/` with timestamps in the file name.

- **Email body vs attachment**
  - **Email body** (HTML):
    - Uses a template that shows **only the next 2 upcoming sprints** relative to the run date.
    - Contains sprint name, dates, working days, capacity %, on‑call primary/secondary, and a team table with leave information.
  - **Attachment (HTML report)**:
    - Shows **all 4 sprints**: previous, current, next, next+1.
    - Same styling as the email body but intended for archive / deeper review.

- **Future dates behavior** (documented in multiple files, including `EMAIL_BODY_*` and `FUTURE_DATES_*` reports):
  - The system correctly updates which sprint is treated as **current**, and therefore which two are shown in the email body, for any future date tested (Jan, Mar, Jul 2026 and beyond).

- **Deep‑dive documentation specifically about the email body**:
  - `EMAIL_BODY_FUTURE_DATES_EXAMPLES.md` – concrete examples for specific dates.
  - `EMAIL_TEMPLATE_STRUCTURE_DETAILED.md` – exact HTML structure and sections of the email body.
  - `EMAIL_VISUAL_PREVIEW_FUTURE_DATES.md` – visual/ASCII mock‑up of how the email looks.
  - `EMAIL_BODY_COMPREHENSIVE_GUIDE.md` – end‑to‑end explanation of email generation.
  - `EMAIL_BODY_FUTURE_DATES_SUMMARY.md` – short summary of email behavior.
  - `FINAL_EMAIL_BODY_ANALYSIS.md` – final analysis and confirmation of correctness.
  - `EMAIL_BODY_DOCUMENTATION_INDEX.md` – index that ties all email‑body docs together.

---

## 5. Testing & Verification Work

A significant part of the Augment work was to **prove** that the system behaves correctly.

Key artifacts:

- `TESTING_INDEX.md`, `TESTING_GUIDE.md`, `TESTING_SUMMARY.md`, `TESTING_COMPLETE_SUMMARY.md`
  - Explain how tests are organized, how to run them, and summarize results.

- `VERIFICATION_COMPLETE_INDEX.md`, `VERIFICATION_COMPLETE.md`, `FINAL_VERIFICATION_REPORT.md`
  - High‑level indexes and final reports confirming that:
    - Sprint calculation is correct for a wide range of dates.
    - Reports (text, HTML, email) contain the right sprints and data.
    - Future date behavior is as required.

- `README_FUTURE_DATES_VERIFICATION.md`, `FUTURE_DATES_VERIFICATION_REPORT.md`, `FUTURE_DATES_VERIFICATION_FINAL.md`, `FUTURE_DATES_TEST_MATRIX.md`
  - Focus specifically on **future date** scenarios (Jan, Mar, Jul 2026, and more).
  - Include test matrices, expected vs actual results, and conclusions.

- `APPLICATION_RUN_REPORT.md`, `SUCCESS_REPORT.md`, `FINAL_STATUS_REPORT.md`
  - Capture real application runs, including environment status and any remaining external issues (for example, SMTP connectivity depending on VPN).

Overall conclusion from these documents: **all logic inside the application is correct and production‑ready; any remaining issues are environmental (e.g., VPN or SMTP server availability).**

---

## 6. Documentation and Workflow Changes

To make the system easy for anyone to pick up, a large set of Markdown guides were created or organized:

- **Top‑level navigation and status**
  - `DOCUMENTATION_INDEX.md` – master index with "if you want X, read Y" guidance.
  - `PROJECT_STATUS_DASHBOARD.md`, `ACTION_ITEMS_COMPLETION_DASHBOARD.md` – high‑level status views.
  - `EXECUTIVE_SUMMARY.md` – non‑technical overview and business value.

- **How to run and use the system**
  - `YOUR_NEW_WORKFLOW.md` – step‑by‑step daily usage guide.
  - `QUICK_START_AFTER_SETUP.md` – condensed quick reference.
  - `START_EMAIL_SETUP.md`, `EMAIL_SETUP_GUIDE.md`, `EMAIL_SETUP_QUICK_REFERENCE.md` – how to configure email.

- **Email credentials and security**
  - `EMAIL_CREDENTIALS_GUIDE.md`, `EMAIL_CREDENTIALS_IMPLEMENTATION_REPORT.md`, `EMAIL_CREDENTIALS_SECURITY_IMPLEMENTATION.md`.
  - `EMAIL_SECURITY_ACTION_COMPLETED.md`, `SECURE_CREDENTIALS_SETUP.md` – what changed and why.

- **Outlook and environment integration**
  - `OUTLOOK_COMPLETE_GUIDE.md`, `OUTLOOK_STEP_BY_STEP.md`, `OUTLOOK_SETUP_SUMMARY.md` – how Outlook fits into the workflow.
  - `ENV_VERIFICATION_REPORT.md`, `ENV_VERIFICATION_SUMMARY.md` – environment checks.

These files together answer: *What changed? How do I run it? How do I fix it if something breaks?*

---

## 7. How a New Person Should Get Started

If you are new to this project, here is the recommended reading and action order:

1. **Read high‑level overview**
   - `EXECUTIVE_SUMMARY.md` – understand what the system does and why it exists.
   - `DOCUMENTATION_INDEX.md` – see the available docs and quick navigation.

2. **Understand day‑to‑day usage**
   - `YOUR_NEW_WORKFLOW.md` – how to run the script and use the outputs.
   - Optionally review `QUICK_START_AFTER_SETUP.md` for a one‑page reminder.

3. **Review email and future‑dates behavior**
   - `EMAIL_BODY_FUTURE_DATES_SUMMARY.md` – how the email body behaves.
   - `README_FUTURE_DATES_VERIFICATION.md` – proof that future dates work correctly.

4. **Dive deeper only if needed**
   - For debugging or extending the code, start with `sprint_capacity_app.py` and the tests in `test_*.py`.
   - For security or environment questions, see the email/security and environment docs listed above.

This single file is meant to give you a clear, end‑to‑end picture of **what was built and verified during the Augment work**, and where to look for more detail in the repository.

