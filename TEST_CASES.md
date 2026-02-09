# Sprint Capacity Automation - Test Cases Document

## Document Information
- **Created:** 2026-01-20
- **Purpose:** Test case documentation for Sprint Capacity Automation System
- **Version:** 1.0

---

## Table of Contents
1. [Configuration Tests](#configuration-tests)
2. [Capacity Calculation Tests](#capacity-calculation-tests)
3. [On-Call Reduction Tests](#on-call-reduction-tests)
4. [Email Template Tests](#email-template-tests)
5. [Report Generation Tests](#report-generation-tests)

---

## Configuration Tests

### TC-001: Hours Per Day Configuration
**Objective:** Verify that the system uses configurable hours per day from config.json

**Preconditions:**
- config.json exists
- `hours_per_day` parameter is set

**Test Steps:**
1. Open `config.json`
2. Set `"hours_per_day": 6`
3. Run: `py sprint_capacity_app.py --analyze`
4. Check the generated report

**Expected Results:**
- Ideal Capacity = Total Members × Working Days × 6
- Example: 7 members × 10 days × 6 = 420 hours

**Test Data:**
```json
{
  "hours_per_day": 6
}
```

**Status:** ✅ Pass / ❌ Fail

---

### TC-002: On-Call Reduction Configuration
**Objective:** Verify that on-call reduction hours are configurable

**Preconditions:**
- config.json exists
- `oncall_primary_hours_reduction` parameter is set

**Test Steps:**
1. Open `config.json`
2. Set `"oncall_primary_hours_reduction": 3`
3. Run: `py sprint_capacity_app.py --analyze`
4. Check Sprint 3 (On-Call Primary: Siva Guru)

**Expected Results:**
- On-call reduction = Working Days × 3 hours
- Example: 10 days × 3 = 30 hours reduction
- Actual Capacity should be reduced by 30 hours

**Test Data:**
```json
{
  "oncall_primary_hours_reduction": 3
}
```

**Status:** ✅ Pass / ❌ Fail

---

### TC-003: Disable On-Call Reduction
**Objective:** Verify that setting on-call reduction to 0 disables the feature

**Test Steps:**
1. Open `config.json`
2. Set `"oncall_primary_hours_reduction": 0`
3. Run: `py sprint_capacity_app.py --analyze`
4. Check Sprint 3 (On-Call Primary: Siva Guru)

**Expected Results:**
- No on-call reduction applied
- Actual Capacity = Base Capacity - Leave Hours only

**Test Data:**
```json
{
  "oncall_primary_hours_reduction": 0
}
```

**Status:** ✅ Pass / ❌ Fail

---

## Capacity Calculation Tests

### TC-004: Ideal Capacity Calculation
**Objective:** Verify Ideal Capacity is calculated correctly WITHOUT any reductions

**Test Steps:**
1. Run: `py sprint_capacity_app.py --analyze`
2. Check Sprint 3 report
3. Verify Ideal Capacity calculation

**Expected Results:**
```
Ideal Capacity = Total Members × Working Days × Hours Per Day
Example: 7 × 10 × 6 = 420 hours
```

**Important:** Ideal Capacity should NOT be reduced by:
- Leave
- On-call reduction
- Any other constraints

**Status:** ✅ Pass / ❌ Fail

---

### TC-005: Actual Capacity Calculation (No On-Call)
**Objective:** Verify Actual Capacity calculation when there's no on-call person

**Test Steps:**
1. Check Sprint 1 (no on-call assigned)
2. Verify calculation

**Expected Results:**
```
Base Capacity = 7 × 9 × 6 = 378 hours
Leave: BindhuMadhuri (1 day) + Lakshmipathy (1 day) = 2 × 6 = 12 hours
Actual Capacity = 378 - 12 = 366 hours
Team Capacity % = (366 ÷ 378) × 100 = 96.8%
```

**Status:** ✅ Pass / ❌ Fail

---

### TC-006: Actual Capacity Calculation (With On-Call)
**Objective:** Verify Actual Capacity calculation when on-call reduction is applied

**Preconditions:**
- `oncall_primary_hours_reduction: 3` in config.json

**Test Steps:**
1. Check Sprint 3 (On-Call Primary: Siva Guru)
2. Verify calculation

**Expected Results:**
```
Base Capacity = 7 × 10 × 6 = 420 hours
Leave: BindhuMadhuri (2 days) + Suganya (1 day) + Syed Sufdar (1 day) = 4 × 6 = 24 hours
Capacity after leave = 420 - 24 = 396 hours
On-Call Reduction (Siva Guru) = 10 days × 3 hours = 30 hours
Actual Capacity = 396 - 30 = 366 hours
Team Capacity % = (366 ÷ 420) × 100 = 87.1%
```

**Status:** ✅ Pass / ❌ Fail

---

### TC-007: Team Capacity Percentage Calculation
**Objective:** Verify Team Capacity % is calculated based on final Actual Capacity (after all reductions)

**Test Steps:**
1. Run: `py sprint_capacity_app.py --analyze`
2. Check all sprints
3. Verify percentage calculation

**Expected Results:**
```
Team Capacity % = (Actual Capacity ÷ Ideal Capacity) × 100

Sprint 1: (366 ÷ 378) × 100 = 96.8%
Sprint 2: (270 ÷ 336) × 100 = 80.4%
Sprint 3: (366 ÷ 420) × 100 = 87.1%
Sprint 4: (342 ÷ 420) × 100 = 81.4%
```

**Important:** Percentage must be calculated AFTER on-call reduction is applied

**Status:** ✅ Pass / ❌ Fail

---

## On-Call Reduction Tests

### TC-008: On-Call Name Matching
**Objective:** Verify system correctly matches on-call names with employee names

**Test Data:**
| On-Call Name (Excel) | Employee Name (System) | Should Match? |
|---------------------|------------------------|---------------|
| Siva Guru | Sampanthamoorthy, Sivaguru | ✅ Yes |
| Lakshmipathy | Murugan, Lakshmipathy | ✅ Yes |
| Pavithra | Murugan Pavithra | ✅ Yes |
| Dhivya Dharmaraj | Dhivya Dharmaraj | ✅ Yes |

**Test Steps:**
1. Check Sprint 2 - On-Call Primary: Lakshmipathy
2. Check Sprint 3 - On-Call Primary: Siva Guru
3. Verify on-call reduction is applied to correct person

**Expected Results:**
- System should match names even with different formats
- On-call reduction should be applied to the matched employee

**Status:** ✅ Pass / ❌ Fail

---

### TC-009: On-Call Reduction Only for Primary
**Objective:** Verify on-call reduction is applied ONLY to Primary On-Call, not Secondary

**Test Steps:**
1. Check Sprint 3
   - Primary: Siva Guru
   - Secondary: Dhivya Dharmaraj
2. Verify only Siva Guru gets 3 hours/day reduction

**Expected Results:**
- Siva Guru: 10 days × 3 hours = 30 hours reduction ✅
- Dhivya Dharmaraj: No reduction ✅

**Status:** ✅ Pass / ❌ Fail

---

### TC-010: On-Call Reduction When On-Call Person Has Leave
**Objective:** Verify on-call reduction is NOT applied for days when on-call person is on leave

**Test Steps:**
1. Create scenario: On-call person has 2 days leave in a 10-day sprint
2. Run analysis

**Expected Results:**
```
Working days for on-call person = 10 - 2 = 8 days
On-call reduction = 8 days × 3 hours = 24 hours (not 30 hours)
```

**Status:** ✅ Pass / ❌ Fail

---

### TC-011: On-Call Reduction Does NOT Affect Ideal Capacity
**Objective:** Verify Ideal Capacity remains unchanged regardless of on-call assignment

**Test Steps:**
1. Compare Sprint 1 (no on-call) and Sprint 3 (with on-call)
2. Both have same working days (10) and team size (7)

**Expected Results:**
```
Sprint 1 Ideal Capacity = 7 × 10 × 6 = 420 hours (if 10 working days)
Sprint 3 Ideal Capacity = 7 × 10 × 6 = 420 hours
```

**Important:** Ideal Capacity should be IDENTICAL for sprints with same working days and team size

**Status:** ✅ Pass / ❌ Fail

---

## Email Template Tests

### TC-012: Email Template Header Design
**Objective:** Verify email template has clean white header with black text

**Test Steps:**
1. Run: `py sprint_capacity_app.py --analyze`
2. Open generated email template in browser
3. Check header design

**Expected Results:**
- Background color: White (#ffffff)
- Title text color: Black (#000000)
- Subtitle text color: Gray (#64748b)
- Bottom border: Blue (#2563eb)
- No gradient backgrounds

**Status:** ✅ Pass / ❌ Fail

---

### TC-013: Email Template Sprint Labels
**Objective:** Verify email body shows "Next Sprint" labels but attached HTML doesn't

**Test Steps:**
1. Check email body (email_template_filled_*.html)
2. Check attached HTML report (sprint_capacity_report_*.html)

**Expected Results:**

**Email Body (Next 2 sprints):**
- Sprint 3 - Next Sprint (Jan 28 - Feb 10, 2026)
- Sprint 4 - Next Sprint +1 (Feb 11 - Feb 24, 2026)

**Attached HTML Report (All 4 sprints):**
- Sprint 1 (Dec 31 - Jan 13, 2026)
- Sprint 2 (Jan 14 - Jan 27, 2026)
- Sprint 3 (Jan 28 - Feb 10, 2026)
- Sprint 4 (Feb 11 - Feb 24, 2026)

**Status:** ✅ Pass / ❌ Fail

---

### TC-014: Email Template Color-Coded Capacity
**Objective:** Verify capacity percentages are color-coded correctly

**Test Steps:**
1. Open email template in browser
2. Check capacity percentage colors

**Expected Results:**
- **Green:** Capacity ≥ 90% (e.g., 94.3%)
- **Orange:** 80% ≤ Capacity < 90% (e.g., 87.1%, 81.4%)
- **Red:** Capacity < 80% (e.g., 75.0%)

**Status:** ✅ Pass / ❌ Fail

---

### TC-015: Email Template Leave Badges
**Objective:** Verify leave dates are displayed as colored badges

**Test Steps:**
1. Open email template
2. Check team member table

**Expected Results:**
- **Planned Leave:** Red badges (#fee2e2 background, #991b1b text)
- **GCC Holiday:** Blue badges (#dbeafe background, #1e40af text)
- Rows with leave: Yellow background (#fef3c7)

**Status:** ✅ Pass / ❌ Fail

---

### TC-016: Email Client Compatibility
**Objective:** Verify email displays correctly in email clients (Outlook, Gmail)

**Test Steps:**
1. Run: `py sprint_capacity_app.py --analyze`
2. Check email in Outlook
3. Check email in Gmail (web)

**Expected Results:**
- Table-based layouts render correctly
- Info cards display in horizontal row
- Metrics display properly
- Colors and styling are preserved
- No broken layouts

**Status:** ✅ Pass / ❌ Fail

---

## Report Generation Tests

### TC-017: Text Report Generation
**Objective:** Verify text report is generated with correct format

**Test Steps:**
1. Run: `py sprint_capacity_app.py --analyze`
2. Open `reports/sprint_capacity_report_*.txt`

**Expected Results:**
- File exists in reports folder
- Contains all 4 sprints
- Shows Ideal Capacity, Actual Capacity, Team Capacity %
- Shows On-Call Primary and Secondary
- Shows team member status with leave dates

**Status:** ✅ Pass / ❌ Fail

---

### TC-018: HTML Report Generation
**Objective:** Verify HTML report is generated with modern design

**Test Steps:**
1. Run: `py sprint_capacity_app.py --analyze`
2. Open `reports/sprint_capacity_report_*.html` in browser

**Expected Results:**
- Modern card-based design
- White header with black text
- Blue sprint section headers
- Metrics in horizontal card layout
- Color-coded capacity percentages
- Leave badges (red for planned, blue for holidays)
- Yellow highlighting for team members on leave

**Status:** ✅ Pass / ❌ Fail

---

### TC-019: Email Template Generation
**Objective:** Verify email template is generated with next 2 sprints only

**Test Steps:**
1. Run: `py sprint_capacity_app.py --analyze`
2. Open `reports/email_template_filled_*.html`

**Expected Results:**
- Shows only next 2 upcoming sprints (Sprint 3 and Sprint 4)
- Sprint labels show "Next Sprint" and "Next Sprint +1"
- Same modern design as HTML report
- Info cards show: Generated date, Team Members, "Next 2" for sprints shown

**Status:** ✅ Pass / ❌ Fail

---

### TC-020: Email Sending
**Objective:** Verify email is sent successfully with correct attachments

**Test Steps:**
1. Run: `py sprint_capacity_app.py --analyze`
2. Check email inbox

**Expected Results:**
- Email received at configured address
- Subject: "Sprint Capacity Report - [Date]"
- Body: Email template with next 2 sprints
- Attachment: HTML report with all 4 sprints
- Sender: DONOTREPLY@ashleyfurniture.com

**Status:** ✅ Pass / ❌ Fail

---

## Edge Cases and Regression Tests

### TC-021: Sprint with No Leave
**Objective:** Verify calculation when no team members have leave

**Test Steps:**
1. Create a sprint where all team members are available
2. Run analysis

**Expected Results:**
```
Ideal Capacity = 7 × 10 × 6 = 420 hours
Actual Capacity = 420 hours (no leave deduction)
Team Capacity % = 100%
```

**Status:** ✅ Pass / ❌ Fail

---

### TC-022: Sprint with All Members on Leave
**Objective:** Verify calculation when all members have some leave

**Test Steps:**
1. Create a sprint where all 7 members have at least 1 day leave
2. Run analysis

**Expected Results:**
- Ideal Capacity = 420 hours (unchanged)
- Actual Capacity = 420 - (total leave days × 6)
- Team Capacity % < 100%

**Status:** ✅ Pass / ❌ Fail

---

### TC-023: On-Call Person Not in Team
**Objective:** Verify system handles case when on-call name doesn't match any employee

**Test Steps:**
1. Manually set on-call primary to a name not in employee list
2. Run analysis

**Expected Results:**
- System should log warning or skip on-call reduction
- No crash or error
- Calculation continues normally

**Status:** ✅ Pass / ❌ Fail

---

### TC-024: Multiple Sprints with Same On-Call Person
**Objective:** Verify on-call reduction is applied correctly across multiple sprints

**Test Steps:**
1. Check if same person is on-call for consecutive sprints
2. Verify reduction is applied to each sprint independently

**Expected Results:**
- Each sprint calculates on-call reduction independently
- No carry-over or accumulation of reductions

**Status:** ✅ Pass / ❌ Fail

---

### TC-025: GCC Holidays Handling
**Objective:** Verify GCC holidays reduce working days but not counted as leave

**Test Steps:**
1. Check Sprint 1 (has Jan 01 GCC holiday)
2. Verify working days calculation

**Expected Results:**
- Working days excludes GCC holidays
- GCC holidays shown in "GCC Holiday" column
- GCC holidays NOT counted in leave person-days
- All team members show same GCC holiday

**Status:** ✅ Pass / ❌ Fail

---

### TC-026: Weekend Handling
**Objective:** Verify weekends are excluded from working days

**Test Steps:**
1. Check any sprint
2. Verify working days count

**Expected Results:**
- Saturdays and Sundays excluded from working days
- Only Monday-Friday counted
- Example: 14-day sprint = max 10 working days (excluding weekends)

**Status:** ✅ Pass / ❌ Fail

---

### TC-027: Leave on Weekend
**Objective:** Verify leave on weekends doesn't reduce capacity

**Test Steps:**
1. Add leave entry for Saturday or Sunday
2. Run analysis

**Expected Results:**
- Weekend leave NOT counted in leave person-days
- No capacity reduction for weekend leave

**Status:** ✅ Pass / ❌ Fail

---

### TC-028: Regression - Ideal Capacity Never Reduced
**Objective:** Ensure Ideal Capacity is NEVER reduced by any factor

**Test Steps:**
1. Run analysis for all sprints
2. Check Ideal Capacity for each sprint

**Expected Results:**
```
Ideal Capacity = Total Members × Working Days × Hours Per Day
```

**Never reduced by:**
- ❌ Leave
- ❌ On-call reduction
- ❌ GCC holidays (already excluded from working days)
- ❌ Any other factor

**Status:** ✅ Pass / ❌ Fail

---

### TC-029: Regression - Actual Capacity Calculation Order
**Objective:** Verify Actual Capacity reductions are applied in correct order

**Test Steps:**
1. Check Sprint 3 with leave and on-call
2. Verify calculation order

**Expected Results:**
```
Step 1: Base = Total Members × Working Days × Hours Per Day
Step 2: Subtract Leave = Base - (Leave Days × Hours Per Day)
Step 3: Subtract On-Call = Result from Step 2 - (On-Call Days × Reduction Hours)
Final: Actual Capacity
```

**Status:** ✅ Pass / ❌ Fail

---

### TC-030: Regression - Capacity Percentage Based on Final Values
**Objective:** Verify Team Capacity % uses final Actual Capacity (after all reductions)

**Test Steps:**
1. Check Sprint 3
2. Verify percentage calculation

**Expected Results:**
```
Team Capacity % = (Final Actual Capacity ÷ Ideal Capacity) × 100
NOT: (Capacity before on-call reduction ÷ Ideal Capacity) × 100
```

**Example:**
- ✅ Correct: (366 ÷ 420) × 100 = 87.1%
- ❌ Wrong: (396 ÷ 420) × 100 = 94.3%

**Status:** ✅ Pass / ❌ Fail

---

## Integration Tests

### TC-031: End-to-End Test - Full Analysis
**Objective:** Verify complete workflow from Excel to Email

**Test Steps:**
1. Ensure Excel file is accessible
2. Run: `py sprint_capacity_app.py --analyze`
3. Check all outputs

**Expected Results:**
1. ✅ Excel file read successfully
2. ✅ Leave data parsed correctly
3. ✅ On-call schedules parsed correctly
4. ✅ 4 sprints calculated
5. ✅ Text report generated
6. ✅ HTML report generated
7. ✅ Email template generated
8. ✅ Email sent successfully
9. ✅ All calculations correct

**Status:** ✅ Pass / ❌ Fail

---

### TC-032: Configuration Change Test
**Objective:** Verify system responds correctly to config changes

**Test Steps:**
1. Change `hours_per_day` from 6 to 8
2. Run analysis
3. Verify all capacities recalculated
4. Change back to 6
5. Run analysis again

**Expected Results:**
- All capacity values update based on new hours_per_day
- No cached or stale values
- System uses latest config values

**Status:** ✅ Pass / ❌ Fail

---

## Test Data Reference

### Sample Sprint 3 Data (For Manual Verification)

**Configuration:**
```json
{
  "hours_per_day": 6,
  "oncall_primary_hours_reduction": 3
}
```

**Sprint Details:**
- Period: 2026-01-28 to 2026-02-10
- Working Days: 10
- Team Members: 7
- On-Call Primary: Siva Guru
- On-Call Secondary: Dhivya Dharmaraj

**Leave Data:**
- BindhuMadhuri Maddela: Feb 02-03 (2 days)
- Suganya Chandrasekaran: Jan 30 (1 day)
- Syed Sufdar Hussain: Jan 28 (1 day)
- Total Leave: 4 person-days

**Expected Calculations:**
```
Ideal Capacity = 7 × 10 × 6 = 420 hours
Base Capacity = 7 × 10 × 6 = 420 hours
Leave Reduction = 4 × 6 = 24 hours
Capacity after leave = 420 - 24 = 396 hours
On-Call Reduction (Siva Guru) = 10 × 3 = 30 hours
Actual Capacity = 396 - 30 = 366 hours
Team Capacity % = (366 ÷ 420) × 100 = 87.1%
```

---

## Test Execution Checklist

### Before Testing:
- [ ] Backup current config.json
- [ ] Ensure Excel file is accessible
- [ ] Clear old reports from reports folder (optional)
- [ ] Note current date for sprint calculations

### During Testing:
- [ ] Run each test case
- [ ] Mark status (✅ Pass / ❌ Fail)
- [ ] Document any failures with screenshots
- [ ] Note actual vs expected results for failures

### After Testing:
- [ ] Restore original config.json
- [ ] Document all test results
- [ ] Create bug reports for failures
- [ ] Archive test reports

---

## Known Issues and Limitations

### Current Limitations:
1. On-call name matching requires at least partial name match
2. System assumes 2-week (14-day) sprint cycles
3. GCC holidays must be entered in Excel leave data
4. Email requires SMTP configuration

### Future Enhancements:
1. Support for variable sprint lengths
2. Configurable capacity thresholds for color coding
3. Multiple on-call reduction levels
4. Dashboard for historical capacity trends

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-20 | System | Initial test case documentation |

---

## Contact and Support

For questions about these test cases or to report issues:
- **Scrum Master:** slatheef@ashleyfurniture.com
- **System Location:** `Capacity Email 19012026/Capacity Email/`
- **Main Script:** `sprint_capacity_app.py`
- **Test Document:** `TEST_CASES.md`

---

**END OF TEST CASES DOCUMENT**
