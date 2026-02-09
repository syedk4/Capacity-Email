# 📧 Email Templates Folder

This folder contains all email templates and documentation for manually sending Sprint Capacity Reports.

## 📁 Folder Contents

### 🎯 Email Templates (Ready to Use)

1. **`email_template_simple.html`** ⭐ **RECOMMENDED**
   - Clean HTML template showing Sprint 2 and Sprint 3
   - Matches the standard report format
   - Light blue headers, yellow highlighting for leave
   - Use this for most emails

2. **`email_template_simple_SAMPLE.html`** ⭐ **EXAMPLE**
   - Fully filled-in example
   - Shows exactly how the final email should look
   - Open in browser to preview

3. **`email_template_simple.txt`**
   - Plain text version
   - Shows Sprint 2 and Sprint 3
   - For email clients that don't support HTML

4. **`email_template.html`** & **`email_template.txt`**
   - Advanced templates showing all 4 sprints
   - For detailed reports

### 📚 Documentation Files

5. **`IMPORTANT_EMAIL_TIMING.md`** ⭐ **READ THIS FIRST**
   - Critical information about when to send and which sprints to include
   - Checklist before sending
   - Common mistakes to avoid

6. **`QUICK_START_EMAIL.md`**
   - Quick reference guide
   - Step-by-step instructions
   - FAQ section

7. **`EMAIL_TEMPLATE_INSTRUCTIONS.md`**
   - Detailed instructions
   - Troubleshooting guide
   - Advanced tips

8. **`README_EMAIL_TEMPLATES.md`**
   - Overview of all templates
   - Which template to use when
   - Best practices

9. **`EMAIL_TEMPLATES_SUMMARY.txt`**
   - Quick text summary
   - Template comparison table

## 🚀 Quick Start

### Step 1: Read the Important Timing Guide
```
Open: IMPORTANT_EMAIL_TIMING.md
```
This explains when to send and which sprints to include.

### Step 2: Generate Your Report
```bash
cd ..
py sprint_capacity_app.py --analyze
```

### Step 3: Use the Template
```
Open: email_template_simple.html
Fill in Sprint 2 and Sprint 3 data
Preview in browser
Copy and paste to email
Send!
```

## ⚠️ IMPORTANT: Email Timing

**Send on the LAST DAY of the current sprint**

**Show the NEXT 2 UPCOMING SPRINTS (not the current sprint)**

### Example:
- **Today**: January 13, 2026 (last day of Sprint 1)
- **Email Shows**: Sprint 2 (Jan 14-27) and Sprint 3 (Jan 28-Feb 10)
- **DON'T Show**: Sprint 1 (current sprint)

## 📖 Recommended Reading Order

1. **`IMPORTANT_EMAIL_TIMING.md`** - Understand timing and sprint selection
2. **`QUICK_START_EMAIL.md`** - Learn how to use the templates
3. **`email_template_simple_SAMPLE.html`** - See the example
4. **`email_template_simple.html`** - Use this for your email

## 🎯 Which Template Should I Use?

| Situation | Use This Template |
|-----------|-------------------|
| Regular team updates | `email_template_simple.html` |
| Need to see an example | `email_template_simple_SAMPLE.html` |
| Plain text email needed | `email_template_simple.txt` |
| Need all 4 sprints | `email_template.html` |

## 📝 Key Points to Remember

✓ Send on the **last day of the current sprint**  
✓ Show **Sprint 2 and Sprint 3** (next 2 upcoming sprints)  
✓ **Don't** include the current sprint (Sprint 1)  
✓ Use `class="highlight"` for rows with planned leave  
✓ Test email to yourself first  

## 🔗 Related Files

- Main application: `../sprint_capacity_app.py`
- Generated reports: `../reports/`
- Configuration: `../config.json`
- Excel data: `../CapacityUpdate.xlsx`

## 💡 Tips

1. **Preview First**: Always open the HTML file in a browser before sending
2. **Test Email**: Send to yourself first to check formatting
3. **Consistency**: Use the same template format each time
4. **Subject Line**: "Sprint Capacity Report - Next 2 Sprints (Sprint 2 & 3)"

## 🆘 Need Help?

1. Check `IMPORTANT_EMAIL_TIMING.md` for timing questions
2. Check `QUICK_START_EMAIL.md` for quick answers
3. Check `EMAIL_TEMPLATE_INSTRUCTIONS.md` for detailed help
4. Look at `email_template_simple_SAMPLE.html` for an example

## 📞 Support

For questions or issues:
- Review the documentation files in this folder
- Contact your Scrum Master
- Check the main project README in the parent folder

---

**Last Updated**: 2026-01-13  
**Version**: 1.0  
**Status**: Temporary solution until programmatic email sending is implemented

