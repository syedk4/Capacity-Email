# Quick Start Guide - Email Template

## 🚀 Quick Steps to Send Email Report

### 1. Generate Report
```bash
py sprint_capacity_app.py --analyze
```

### 2. Open Template
Open `email_template_simple.html` in a text editor (Notepad, VS Code, etc.)

### 3. Replace Placeholders

**IMPORTANT:** The email shows the **next 2 upcoming sprints** (not the current sprint).
If today is the last day of Sprint 1, the email should show Sprint 2 and Sprint 3.

Find and replace these values from your generated report:

| Find This | Replace With | Example |
|-----------|--------------|---------|
| `[DATE]` | Generated date | 2026-01-13 14:41:12 |
| `[TOTAL_MEMBERS]` | Total team members | 7 |
| `[SPRINT2_PERIOD]` | Sprint 2 dates (next sprint) | 2026-01-14 to 2026-01-27 |
| `[SPRINT2_WORKING_DAYS]` | Sprint 2 working days | 8 |
| `[SPRINT2_CAPACITY]` | Sprint 2 capacity % | 83.9 |
| `[SPRINT3_PERIOD]` | Sprint 3 dates | 2026-01-28 to 2026-02-10 |
| `[SPRINT3_WORKING_DAYS]` | Sprint 3 working days | 10 |
| `[SPRINT3_CAPACITY]` | Sprint 3 capacity % | 100 |

### 4. Update Team Member Rows

**For Sprint 2 (Next Sprint):**
Delete the example rows and replace with actual data from Sprint 2 in your report.

Example row format:
```html
<tr>
    <td>200071</td>
    <td>BindhuMadhuri Maddela</td>
    <td>-</td>
    <td>Jan 15, Jan 26</td>
</tr>
```

If the employee has planned leave, add `class="highlight"`:
```html
<tr class="highlight">
    <td>200325</td>
    <td>Suganya Chandrasekaran</td>
    <td>Jan 22</td>
    <td>Jan 15, Jan 26</td>
</tr>
```

**For Sprint 3:**
Repeat the same process for Sprint 3 team member rows.

### 5. Preview
Open the HTML file in a web browser to preview how it will look.

### 6. Copy to Email
1. Open the HTML file in a web browser
2. Press `Ctrl+A` to select all
3. Press `Ctrl+C` to copy
4. Open your email client (Outlook, Gmail, etc.)
5. Create a new email
6. Press `Ctrl+V` to paste
7. Add subject: "Sprint Capacity Report - [Month Year]"
8. Add recipients
9. Send!

## 📋 Example Email Subject Lines

- Sprint Capacity Report - January 2026
- Team Capacity Update - Next 2 Sprints
- Sprint Planning: Capacity Report for Jan-Feb 2026

## 👥 Suggested Recipients

- Scrum Master
- Product Owner
- Development Team Members
- Engineering Manager
- Stakeholders (optional)

## ⏰ When to Send

- **Best Time**: Last day of the current sprint (e.g., if Sprint 1 ends on Jan 13, send on Jan 13)
- **Frequency**: Every 2 weeks (at the end of each sprint)
- **Day**: Last working day of the sprint
- **Purpose**: To inform the team about capacity for the next 2 upcoming sprints

## 💡 Pro Tips

1. **Save Time**: Create a draft email template in your email client with standard recipients and subject line
2. **Consistency**: Send at the same time each sprint for predictability
3. **Backup**: Keep a copy of sent emails in a dedicated folder
4. **Feedback**: Ask recipients if the format works for them and adjust as needed
5. **Automation Coming**: This is temporary - programmatic email sending will be added soon!

## ❓ Common Questions

**Q: Which sprints should I include in the email?**
A: Always include the **next 2 upcoming sprints** (not the current sprint). If today is the last day of Sprint 1, include Sprint 2 and Sprint 3.

**Q: When should I send the email?**
A: Send on the **last day of the current sprint** to inform the team about the next 2 sprints.

**Q: Do I need to include all 4 sprints?**
A: No, the simple template shows only the next 2 upcoming sprints to keep emails concise.

**Q: Can I customize the colors?**
A: Yes! Edit the CSS in the `<style>` section of the HTML file.

**Q: What if I want plain text instead?**
A: Use `email_template_simple.txt` instead and paste directly into your email.

**Q: How do I highlight rows with leave?**
A: Add `class="highlight"` to the `<tr>` tag for that row.

## 🆘 Need Help?

Check the detailed instructions in `EMAIL_TEMPLATE_INSTRUCTIONS.md`

