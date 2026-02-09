# 📊 DETAILED DATA COMPARISON - Excel vs Report

## Summary
Comparing the Excel "Planned Leave" data with the generated Sprint Capacity Report.

---

## JANUARY DATA (Sprint 2: Jan 14-27)

| Employee | Excel Data | Report Shows | Status |
|----------|-----------|-------------|--------|
| BindhuMadhuri | 12 | Jan 12 | ✅ Correct |
| Suganya | 22, 30 | Jan 22 | ✅ Correct (30 is in Sprint 3) |
| Dhivya | 16, 19 | Jan 16, Jan 19 | ✅ Correct |
| Lakshmipathy | 2 | Jan 02 | ✅ Correct |
| Sivaguru | 14, 16 | Jan 14, Jan 16 | ✅ Correct |
| Pavithra | 14, 16 | Jan 14, Jan 16 | ✅ Correct |
| Syed Sufdar | 28 | - | ✅ Correct (28 is in Sprint 3) |

---

## FEBRUARY DATA - SPRINT 3 (Jan 28 - Feb 10)

| Employee | Excel Data | Report Shows | Status |
|----------|-----------|-------------|--------|
| BindhuMadhuri | 2, 3, 16, 17 | Feb 02-03 | ✅ Correct (16-17 in Sprint 4) |
| Suganya | 16 to 27 | Jan 30 | ⚠️ Shows Jan 30, not Feb dates |
| Dhivya | 23 | - | ✅ Correct (23 is in Sprint 4) |
| Lakshmipathy | 19, 20, 23 | - | ✅ Correct (all in Sprint 4) |
| Sivaguru | - | - | ✅ Correct |
| Pavithra | - | - | ✅ Correct |
| Syed Sufdar | 16 and 17 | Jan 28 | ✅ Correct (16-17 in Sprint 4) |

---

## FEBRUARY DATA - SPRINT 4 (Feb 11-24)

| Employee | Excel Data | Report Shows | Status |
|----------|-----------|-------------|--------|
| BindhuMadhuri | 2, 3, 16, 17 | Feb 16-17 | ✅ Correct (2-3 in Sprint 3) |
| Suganya | 16 to 27 | Feb 16-24 | ✅ Correct |
| Dhivya | 23 | Feb 23 | ✅ Correct |
| Lakshmipathy | 19, 20, 23 | Feb 23 | ❌ **MISSING Feb 19-20** |
| Sivaguru | - | - | ✅ Correct |
| Pavithra | - | - | ✅ Correct |
| Syed Sufdar | 16 and 17 | Feb 16-17 | ✅ Correct |

---

## CRITICAL ISSUE FOUND

### Lakshmipathy - February Leave

**Excel Data:** `19,20,23`
**Report Shows (Sprint 4):** `Feb 23` only
**Missing:** `Feb 19, Feb 20`

**Analysis:**
- Feb 19 = Thursday (working day) ✅
- Feb 20 = Friday (working day) ✅
- Feb 23 = Monday (working day) ✅
- All three dates are working days
- All three dates are in Sprint 4 (Feb 11-24)
- **Why are Feb 19-20 missing?**

---

## Root Cause Investigation

The issue appears to be in the **date display logic**, not the parsing logic.

**Possible causes:**
1. Date range formatting is collapsing non-consecutive dates
2. Some dates are being filtered out during display
3. The range formatting function is not handling gaps correctly

---

## Recommendation

Check the `format_dates_as_ranges()` function to ensure it:
1. Correctly identifies consecutive dates
2. Preserves non-consecutive dates
3. Displays all dates in the leave entry

**Example:**
- Input: `[Feb 19, Feb 20, Feb 23]`
- Expected: `Feb 19-20, Feb 23`
- Actual: `Feb 23` (missing Feb 19-20)

---

## Next Steps

1. Debug the `format_dates_as_ranges()` function
2. Check if dates are being filtered before formatting
3. Verify the leave entry contains all three dates
4. Test with the actual data from the Excel file

