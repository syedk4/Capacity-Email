# Sprint Capacity Automation System - QA Team Review Document

## 📋 Document Purpose
This document is created for the QA team to review, validate, and provide suggestions on the Sprint Capacity Automation System developed by the Syed Sufdar Hussain Lead QA.

**Review Date:** February 6, 2026  
**Version:** 2.0 (with Location-Based Holiday Support)  
**Team:** Finance Aspirants Team

---

## 🎯 System Overview

### What Does This System Do?
The Sprint Capacity Automation System automatically calculates team capacity for 2-week sprints by:
- Reading employee data and leave plans from Excel
- Calculating working days based on employee location (GCC/India vs US)
- Applying location-specific holidays (GCC holidays vs US holidays)
- Accounting for on-call rotations and their impact on capacity
- Generating detailed reports in text, HTML, and email formats
- Sending automated email reports to stakeholders

### Key Features
1. ✅ **Location-Based Holiday Support** - Different holiday calendars for India and US team members
2. ✅ **On-Call Rotation Tracking** - Primary and Secondary on-call assignments
3. ✅ **Capacity Reduction for On-Call** - Primary on-call person gets reduced development hours
4. ✅ **Multi-Format Reports** - Text, HTML, and Email template generation
5. ✅ **Automated Email Delivery** - Reports sent automatically to stakeholders
6. ✅ **Holiday Count Display** - Shows GCC and US holiday counts separately

---

## 📊 Capacity Calculation Logic - DETAILED EXPLANATION

### 1. Working Days Calculation

**Formula:**
```
Working Days = Total Weekdays in Sprint (Monday-Friday only)
```

**Example for Sprint 2 (Jan 14 - Jan 27, 2026):**
- Total calendar days: 14 days
- Weekdays (Mon-Fri): 10 days
- Weekends (Sat-Sun): 4 days
- **Working Days = 10**

**Important:** Working days count is the SAME for all employees initially. Location-based holidays are applied in the next step.

---

### 2. Location-Based Working Days

**Each employee gets different working days based on their location:**

**For GCC/India Employees:**
```
Employee Working Days = Total Weekdays - GCC Holidays in Sprint
```

**For US Employees:**
```
Employee Working Days = Total Weekdays - US Holidays in Sprint
```

**Example for Sprint 2:**
- Total Weekdays: 10 days
- GCC Holidays: Jan 15 (Republic Day Eve), Jan 26 (Republic Day) = 2 days
- US Holidays: Jan 19 (Martin Luther King Jr. Day) = 1 day

**GCC Employee Working Days:** 10 - 2 = **8 days**  
**US Employee Working Days:** 10 - 1 = **9 days**

---

### 3. Ideal Capacity Calculation

**Formula:**
```
Ideal Capacity = Σ (Each Employee's Working Days × Hours per Day) - On-Call Reduction
```

**Step-by-Step Calculation for Sprint 2:**

**Team Composition:**
- 7 GCC employees (India-based)
- 3 US employees

**Hours per Day:** 6 hours (configured in config.json)

**Step 1: Calculate capacity for GCC employees**
```
GCC Capacity = 7 employees × 8 working days × 6 hours/day
GCC Capacity = 7 × 8 × 6 = 336 hours
```

**Step 2: Calculate capacity for US employees**
```
US Capacity = 3 employees × 9 working days × 6 hours/day
US Capacity = 3 × 9 × 6 = 162 hours
```

**Step 3: Total capacity before on-call reduction**
```
Total = 336 + 162 = 498 hours
```

**Step 4: Apply on-call reduction**
- Primary on-call: Lakshmipathy (GCC employee)
- On-call reduction: 2 hours/day (configured in config.json)
- On-call working days: 10 days (ALL weekdays, including GCC holidays)
```
On-Call Reduction = 10 days × 2 hours/day = 20 hours
```

**Step 5: Final Ideal Capacity**
```
Ideal Capacity = 498 - 20 = 478 hours
```

**✅ This matches the report: Ideal Capacity: 478.0 hours**

---

### 4. Actual Capacity Calculation

**Formula:**
```
Actual Capacity = Ideal Capacity - Total Leave Hours
```

**Leave Hours Calculation:**
```
Leave Hours = Σ (Each employee's leave days × Hours per Day)
```

**Example for Sprint 2:**

| Employee | Leave Days | Hours per Day | Leave Hours |
|----------|-----------|---------------|-------------|
| Suganya Chandrasekaran | 1 (Jan 22) | 6 | 6 |
| Dhivya Dharmaraj | 2 (Jan 16, 19) | 6 | 12 |
| Sampanthamoorthy, Sivaguru | 2 (Jan 14, 16) | 6 | 12 |
| Murugan Pavithra | 2 (Jan 14, 16) | 6 | 12 |
| Satish KambleOne | 1 (Jan 21) | 6 | 6 |
| Satish KambleTwo | 1 (Jan 22) | 6 | 6 |
| Satish KambleThree | 1 (Jan 23) | 6 | 6 |
| **Total** | **10 days** | | **60 hours** |

**Actual Capacity:**
```
Actual Capacity = 478 - 60 = 418 hours
```

**✅ This matches the report: Actual Capacity: 418.0 hours**

---

### 5. Team Capacity Percentage

**Formula:**
```
Team Capacity % = (Actual Capacity ÷ Ideal Capacity) × 100
```

**Example for Sprint 2:**
```
Team Capacity % = (418 ÷ 478) × 100 = 87.4%
```

**✅ This matches the report: GCC Team Capacity: 87.4%**

---

## 🔍 Validation Checklist for QA Team

### ✅ Data Validation

1. **Employee Count**
   - [ ] Verify total team members count (should be 10)
   - [ ] Verify GCC employees count (should be 7)
   - [ ] Verify US employees count (should be 3)

2. **Working Days**
   - [ ] Count weekdays in sprint manually (exclude Sat/Sun)
   - [ ] Verify working days = weekdays count
   - [ ] Example: Sprint 2 (Jan 14-27) should have 10 weekdays

3. **Holiday Counts**
   - [ ] Verify GCC holiday count matches Excel "Holiday" column
   - [ ] Verify US holiday count matches Excel "Holiday" column
   - [ ] Check holiday dates are within sprint period

4. **Leave Data**
   - [ ] Verify each employee's planned leave matches Excel
   - [ ] Check leave dates are parsed correctly
   - [ ] Verify leave dates fall within sprint period

5. **On-Call Assignments**
   - [ ] Verify Primary on-call name matches "On Call Schedules" sheet
   - [ ] Verify Secondary on-call name matches "On Call Schedules" sheet
   - [ ] Check on-call dates align with sprint dates

---

### ✅ Calculation Validation

**Use the formulas provided above to manually verify:**

1. **Ideal Capacity Calculation**
   - [ ] Calculate GCC employee capacity: (GCC count × GCC working days × 6)
   - [ ] Calculate US employee capacity: (US count × US working days × 6)
   - [ ] Add both capacities
   - [ ] Subtract on-call reduction (10 days × 2 hours = 20 hours)
   - [ ] Compare with report's "Ideal Capacity"

2. **Actual Capacity Calculation**
   - [ ] Count total leave days from the table
   - [ ] Multiply by 6 hours/day to get total leave hours
   - [ ] Subtract from Ideal Capacity
   - [ ] Compare with report's "Actual Capacity"

3. **Team Capacity Percentage**
   - [ ] Divide Actual by Ideal
   - [ ] Multiply by 100
   - [ ] Compare with report's "Team Capacity %"

---

### ✅ Report Format Validation

1. **Text Report**
   - [ ] Check all sprints are displayed (Sprint 2, 3, 4, 5)
   - [ ] Verify holiday counts format: "Holidays:" header with "GCC - X" and "US - Y" indented
   - [ ] Check on-call information is displayed
   - [ ] Verify employee table has all columns: Emp ID, Name, Planned Leave, GCC Holiday, US Holiday

2. **HTML Report**
   - [ ] Open HTML report in browser
   - [ ] Check metrics grid displays: Working Days, Holidays, Team Members, Team Capacity, Ideal/Actual Capacity
   - [ ] Verify holiday counts show "GCC - X" and "US - Y" separated by line break
   - [ ] Check capacity percentage color coding (Green ≥90%, Yellow 80-90%, Red <80%)
   - [ ] Verify employee table formatting and readability

3. **Email Template**
   - [ ] Check email shows next 2 upcoming sprints only
   - [ ] Verify same format as HTML report
   - [ ] Check all metrics are displayed correctly

---

## 🧪 Test Scenarios for QA Team

### Test Scenario 1: Sprint with Both GCC and US Holidays
**Sprint:** Sprint 2 (Jan 14 - Jan 27, 2026)

**Expected Results:**
- Working Days: 10
- Holidays: GCC - 2, US - 1
- GCC Holidays: Jan 15, Jan 26
- US Holidays: Jan 19
- Ideal Capacity: 478.0 hours
- Team Capacity: 87.4%

**Validation Steps:**
1. Open the text report
2. Find Sprint 2 section
3. Verify all values match expected results
4. Manually calculate using formulas above
5. Compare your calculation with report

---

### Test Scenario 2: Sprint with No Holidays
**Sprint:** Sprint 3 (Jan 28 - Feb 10, 2026)

**Expected Results:**
- Working Days: 10
- No "Holidays:" line should appear (no holidays in this sprint)
- Ideal Capacity: 580.0 hours
- Team Capacity: 93.8%

**Validation Steps:**
1. Verify no holiday line is displayed
2. Check GCC Holiday and US Holiday columns show "-" for all employees
3. Calculate ideal capacity: (7 × 10 × 6) + (3 × 10 × 6) - 20 = 580 hours

---

### Test Scenario 3: Sprint with Only US Holiday
**Sprint:** Sprint 4 (Feb 11 - Feb 24, 2026)

**Expected Results:**
- Working Days: 10
- Holidays: US - 1
- US Holiday: Feb 12 (Lincoln's Birthday)
- No GCC holidays
- Ideal Capacity: 582.0 hours
- Team Capacity: 85.6%

**Validation Steps:**
1. Verify only "US - 1" is shown in holidays
2. Check only US employees show Feb 12 in US Holiday column
3. GCC employees should show "-" in US Holiday column

---

### Test Scenario 4: On-Call Reduction Validation
**Sprint:** Sprint 2 (Primary: Lakshmipathy)

**Expected On-Call Reduction:**
- Primary on-call works ALL weekdays (10 days) including GCC holidays
- Reduction: 2 hours/day × 10 days = 20 hours

**Validation Steps:**
1. Verify Lakshmipathy is shown as Primary on-call
2. Calculate capacity without on-call: (7 × 8 × 6) + (3 × 9 × 6) = 498 hours
3. Subtract on-call reduction: 498 - 20 = 478 hours
4. Compare with Ideal Capacity in report

---

## 📝 Feedback Template for QA Team

Please use this template to provide your feedback:

### 1. Data Accuracy
- [ ] All employee data is correct
- [ ] Leave dates are parsed correctly
- [ ] Holiday dates are accurate
- [ ] On-call assignments are correct
- **Issues Found:** _[Describe any issues]_

### 2. Calculation Accuracy
- [ ] Ideal Capacity calculations are correct
- [ ] Actual Capacity calculations are correct
- [ ] Team Capacity % is accurate
- [ ] On-call reduction is applied correctly
- **Issues Found:** _[Describe any issues]_

### 3. Report Format & Readability
- [ ] Text report is clear and easy to read
- [ ] HTML report displays correctly in browser
- [ ] Email template is professional and complete
- [ ] Holiday counts are displayed clearly
- **Suggestions:** _[Provide suggestions for improvement]_

### 4. Functionality Testing
- [ ] System handles GCC holidays correctly
- [ ] System handles US holidays correctly
- [ ] Location-based capacity works as expected
- [ ] On-call rotation tracking works correctly
- **Issues Found:** _[Describe any issues]_

### 5. Edge Cases & Scenarios
- [ ] Tested sprint with no holidays
- [ ] Tested sprint with only GCC holidays
- [ ] Tested sprint with only US holidays
- [ ] Tested sprint with both GCC and US holidays
- **Issues Found:** _[Describe any issues]_

### 6. Overall Assessment
**Rating:** _[1-5 stars]_
**Strengths:** _[What works well]_
**Areas for Improvement:** _[What needs improvement]_
**Additional Suggestions:** _[Any other feedback]_

---

## 📧 Review Materials Provided

You will receive the following files for review:

1. **Text Report:** `sprint_capacity_report_20260206_140719.txt`
   - Contains detailed capacity analysis for 4 sprints
   - Shows all calculations and employee status

2. **HTML Report:** `sprint_capacity_report_20260206_140719.html`
   - Visual representation of the same data
   - Open in browser for best viewing experience

3. **Email Template:** `email_template_filled_20260206_140719.html`
   - Shows next 2 upcoming sprints
   - This is what stakeholders will receive via email

4. **Excel Data File:** `CapacityUpdate.xlsx`
   - Source data for validation
   - Contains employee data, leave plans, holidays, and on-call schedules

---

## 🎯 Key Questions for QA Team

1. **Is the calculation logic clear and easy to understand?**
2. **Are the reports easy to read and interpret?**
3. **Is the holiday count display format helpful?**
4. **Should we add any additional metrics or information?**
5. **Are there any edge cases we should test?**
6. **Is the email template professional and complete?**
7. **Should we add any visual indicators or charts?**
8. **Are there any performance concerns with the current implementation?**

---

## 📞 Contact Information

**Lead QA:** [Your Name]
**Review Deadline:** [Specify deadline]
**Feedback Method:** [Email/Meeting/Document]

---

## 🔧 Technical Details (For Reference)

### System Configuration
- **Sprint Duration:** 14 calendar days (2 weeks)
- **Working Hours per Day:** 6 hours
- **On-Call Primary Reduction:** 2 hours/day
- **On-Call Secondary Reduction:** 0 hours/day (no reduction)

### Data Sources
- **Employee Data:** Excel file "CapacityUpdate.xlsx", Sheet "2026"
- **On-Call Schedules:** Excel file "CapacityUpdate.xlsx", Sheet "On Call Schedules"
- **GCC Holidays:** Excel "Holiday" column (leave_type = 'public_holiday', Location = 'GCC')
- **US Holidays:** Excel "Holiday" column (leave_type = 'public_holiday', Location = 'US')

### Report Generation
- **Text Report:** Plain text format for easy sharing
- **HTML Report:** Rich formatting with color-coded capacity indicators
- **Email Template:** Pre-filled HTML email body with next 2 sprints

---

## ✅ Thank You!

Thank you for taking the time to review this Sprint Capacity Automation System. Your feedback is valuable and will help improve the system for the entire team.

Please provide your feedback by [deadline date].

---

**Document Version:** 1.0
**Created:** February 6, 2026
**Last Updated:** February 6, 2026


