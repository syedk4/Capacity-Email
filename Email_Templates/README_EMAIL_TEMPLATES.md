# Email Templates for Sprint Capacity Reports

## 📧 Overview

This folder contains email templates for manually sending Sprint Capacity Reports. These are temporary solutions until programmatic email sending is implemented.

## 📁 Files

### Email Templates
- **`email_template_simple.html`** ⭐ RECOMMENDED - Simple HTML template showing next 2 sprints
- **`email_template_simple.txt`** - Plain text version showing next 2 sprints
- **`email_template.html`** - Advanced HTML template showing all 4 sprints
- **`email_template.txt`** - Plain text version showing all 4 sprints

### Documentation
- **`QUICK_START_EMAIL.md`** - Quick reference guide for sending emails
- **`EMAIL_TEMPLATE_INSTRUCTIONS.md`** - Detailed instructions and troubleshooting
- **`README_EMAIL_TEMPLATES.md`** - This file

## 🎯 Which Template Should I Use?

### Use `email_template_simple.html` if:
- ✅ You want a clean, professional look matching the screenshot
- ✅ You only need to show the next 2 upcoming sprints (not the current sprint)
- ✅ You're sending on the last day of the current sprint
- ✅ You're sending to stakeholders who prefer concise updates
- ✅ You want to match the standard report format

### Use `email_template_simple.txt` if:
- ✅ Your email client doesn't support HTML
- ✅ You prefer plain text emails
- ✅ You want maximum compatibility

### Use `email_template.html` if:
- ✅ You need to show all 4 sprints
- ✅ You want a more colorful, gradient design
- ✅ You're sending detailed planning reports

## 🚀 Quick Start

1. **Generate Report**
   ```bash
   py sprint_capacity_app.py --analyze
   ```

2. **Open Template**
   - Open `email_template_simple.html` in a text editor

3. **Replace Placeholders**
   - Replace `[DATE]`, `[TOTAL_MEMBERS]`, etc. with actual values
   - Update team member rows with data from your report

4. **Preview**
   - Open the HTML file in a web browser

5. **Send**
   - Copy the content and paste into your email client
   - Add recipients and send

📖 **For detailed instructions, see `QUICK_START_EMAIL.md`**

## 🎨 Template Features

### Simple HTML Template
- Light gray header with report title
- Light blue sprint section headers
- Clean table layout
- Yellow highlighting for rows with planned leave
- Shows only next 2 sprints
- Matches the standard report screenshot

### Advanced HTML Template
- Purple gradient header
- Color-coded capacity indicators (green/yellow/red)
- Card-based layout
- Shows all 4 sprints
- More visual styling

## 📊 What Data to Include

The templates show:
- **Generated Date**: When the report was created
- **Total Team Members**: Number of team members
- **Sprint Period**: Date range for each sprint
- **Working Days**: Working days excluding weekends and GCC holidays
- **GCC Members Count**: Total team members
- **GCC Team Capacity**: Capacity percentage based on person-days
- **Team Member Status**: Individual leave details for each member

## 🔄 Workflow

```
Generate Report → Edit Template → Preview → Copy → Paste to Email → Send
```

## 💡 Best Practices

1. **Timing**: Send on the **last day of the current sprint** (e.g., if Sprint 1 ends on Jan 13, send on Jan 13)
2. **Sprint Selection**: Always show the **next 2 upcoming sprints** (not the current sprint)
3. **Consistency**: Use the same template format each time
4. **Recipients**: Include Scrum Master, Product Owner, and team
5. **Subject**: Use clear subject lines like "Sprint Capacity Report - Next 2 Sprints (Sprint 2 & 3)"
6. **Test**: Always send a test email to yourself first

## 🎯 Future Enhancements

This is a temporary solution. Future versions will include:
- ✨ Automatic email generation from reports
- ✨ Programmatic email sending
- ✨ Configurable recipients
- ✨ Scheduled automatic sending
- ✨ Email templates stored in configuration

## 📞 Support

For questions or issues:
1. Check `QUICK_START_EMAIL.md` for quick answers
2. Review `EMAIL_TEMPLATE_INSTRUCTIONS.md` for detailed help
3. Contact your Scrum Master or tool administrator

## 📝 Notes

- **Working Days**: Calculated excluding weekends and GCC holidays
- **GCC Team Capacity**: Based on available person-days, not just member count
- **Highlighting**: Yellow background indicates team members with planned leave
- **Next 2 Sprints**: Simple templates show only the next 2 upcoming sprints (not the current sprint)
- **Send Timing**: Email should be sent on the last day of the current sprint
- **Example**: If today is Jan 13 (last day of Sprint 1), show Sprint 2 and Sprint 3

---

**Last Updated**: 2026-01-13
**Version**: 1.0
**Status**: Temporary solution until programmatic email sending is implemented

