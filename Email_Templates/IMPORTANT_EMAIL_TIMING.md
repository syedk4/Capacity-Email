# ⚠️ IMPORTANT: Email Timing and Sprint Selection

## 📅 When to Send the Email

**Send on the LAST DAY of the current sprint**

### Example:
- **Today's Date**: January 13, 2026
- **Current Sprint**: Sprint 1 (2025-12-31 to 2026-01-13)
- **Email Send Date**: January 13, 2026 (last day of Sprint 1)
- **Sprints to Include in Email**: Sprint 2 and Sprint 3

## 📊 Which Sprints to Include

**Always include the NEXT 2 UPCOMING SPRINTS (not the current sprint)**

### Example Scenario:

```
Current Situation:
├── Sprint 1: 2025-12-31 to 2026-01-13 ← Current sprint (ending today)
├── Sprint 2: 2026-01-14 to 2026-01-27 ← Include in email ✓
├── Sprint 3: 2026-01-28 to 2026-02-10 ← Include in email ✓
└── Sprint 4: 2026-02-11 to 2026-02-24 ← Do NOT include
```

## 🎯 Why This Approach?

1. **Forward-Looking**: The team needs to know about upcoming sprints, not the current one
2. **Planning**: Helps with resource planning for the next 2 sprints
3. **Timely**: Sent at the end of the current sprint, just before the next sprint starts
4. **Concise**: Only 2 sprints keeps the email focused and actionable

## 📝 Template Placeholders to Use

When filling in the email template, use data from:

| Placeholder | Use Data From | Example |
|-------------|---------------|---------|
| `[SPRINT2_PERIOD]` | Sprint 2 dates | 2026-01-14 to 2026-01-27 |
| `[SPRINT2_WORKING_DAYS]` | Sprint 2 working days | 8 |
| `[SPRINT2_CAPACITY]` | Sprint 2 capacity % | 83.9 |
| `[SPRINT3_PERIOD]` | Sprint 3 dates | 2026-01-28 to 2026-02-10 |
| `[SPRINT3_WORKING_DAYS]` | Sprint 3 working days | 10 |
| `[SPRINT3_CAPACITY]` | Sprint 3 capacity % | 100 |

## ✅ Checklist Before Sending

- [ ] Today is the last day of the current sprint
- [ ] Email shows Sprint 2 and Sprint 3 (not Sprint 1)
- [ ] All placeholders are replaced with correct data
- [ ] Team member rows are updated for both sprints
- [ ] Rows with planned leave are highlighted (class="highlight")
- [ ] Subject line mentions "Next 2 Sprints (Sprint 2 & 3)"
- [ ] Test email sent to yourself first

## 📧 Recommended Subject Lines

- "Sprint Capacity Report - Next 2 Sprints (Sprint 2 & 3)"
- "Team Capacity Update - Upcoming Sprints 2 & 3"
- "Sprint Planning: Capacity for Sprint 2 & 3"

## 🔄 Workflow

```
Last Day of Sprint 1 (Jan 13)
    ↓
Generate Report (py sprint_capacity_app.py --analyze)
    ↓
Open email_template_simple.html
    ↓
Fill in Sprint 2 and Sprint 3 data
    ↓
Preview in browser
    ↓
Copy and paste to email
    ↓
Send to team
    ↓
Next email on last day of Sprint 2 (Jan 27)
    ↓
(Will show Sprint 3 and Sprint 4)
```

## ❌ Common Mistakes to Avoid

1. **DON'T** include Sprint 1 (current sprint) in the email
2. **DON'T** send at the beginning of the sprint
3. **DON'T** include all 4 sprints (too much information)
4. **DON'T** forget to update both Sprint 2 AND Sprint 3 sections

## ✓ Correct Approach

1. **DO** send on the last day of the current sprint
2. **DO** include only the next 2 upcoming sprints
3. **DO** use Sprint 2 and Sprint 3 data from your report
4. **DO** highlight rows with planned leave

## 📞 Questions?

If you're unsure which sprints to include:
1. Check today's date
2. Find which sprint is currently active
3. Include the next 2 sprints after the current one
4. Ignore the current sprint and Sprint 4

---

**Remember**: The email is about **future planning**, not current status!

