# Email Template Instructions

This folder contains email templates for sending Sprint Capacity Reports manually until the programmatic email sending feature is implemented.

## Available Templates

### 1. `email_template_simple.html` - Simple HTML Email Template (RECOMMENDED)
- **Use for**: Clean, professional emails matching the standard report format
- **Best for**: Outlook, Gmail, and other modern email clients
- **Features**:
  - Shows only the next 2 upcoming sprints (not the current sprint)
  - Sent on the last day of the current sprint
  - Simple table layout matching the screenshot
  - Light blue sprint headers
  - Yellow highlighting for rows with planned leave
  - Clean, easy to read format

### 2. `email_template_simple.txt` - Plain Text Email Template
- **Use for**: Simple text-based emails
- **Best for**: Email clients that don't support HTML or when you prefer plain text
- **Features**:
  - Shows only the next 2 upcoming sprints (not the current sprint)
  - Sent on the last day of the current sprint
  - Clean, readable format
  - Works in all email clients
  - Easy to copy/paste

### 3. `email_template.html` - Advanced HTML Email Template
- **Use for**: Rich formatted emails with all 4 sprints
- **Features**:
  - Shows all 4 sprints
  - Professional gradient header
  - Color-coded capacity indicators
  - More detailed styling

## How to Use the Templates

### Step 1: Generate the Sprint Capacity Report
Run the analysis tool to generate the latest report:
```bash
py sprint_capacity_app.py --analyze
```

This will create two files in the `reports` folder:
- `sprint_capacity_report_YYYYMMDD_HHMMSS.txt`
- `sprint_capacity_report_YYYYMMDD_HHMMSS.html`

**IMPORTANT:** The email should be sent on the **last day of the current sprint** and should show the **next 2 upcoming sprints** (not the current sprint).

**Example:** If today is Jan 13 (last day of Sprint 1), the email should show:
- Sprint 2 (2026-01-14 to 2026-01-27)
- Sprint 3 (2026-01-28 to 2026-02-10)

### Step 2: Choose Your Template

#### For Simple HTML Email (RECOMMENDED):
1. Open `email_template_simple.html` in a text editor
2. Open the generated TXT report from the `reports` folder
3. Copy data from Sprint 2 and Sprint 3 only (the next 2 upcoming sprints)
4. Replace the placeholders and example data in the template

#### For Plain Text Email:
1. Open `email_template_simple.txt` in a text editor
2. Open the generated TXT report from the `reports` folder
3. Copy data from Sprint 2 and Sprint 3 only (the next 2 upcoming sprints)
4. Replace the placeholders and example data in the template

#### For Advanced HTML Email (All 4 Sprints):
1. Open `email_template.html` in a text editor
2. Open the generated HTML report from the `reports` folder
3. Copy the relevant data from all 4 sprints and replace the placeholders

### Step 3: Replace Placeholders

Replace all placeholders (text in square brackets) with actual data:

| Placeholder | Example Value | Where to Find |
|------------|---------------|---------------|
| `[DATE]` | 2026-01-13 14:41:12 | Top of the report |
| `[TOTAL_MEMBERS]` | 7 | "Total Team Members" line |
| `[PERIOD]` | Jan 2026 - Feb 2026 | Sprint date ranges |
| `[NUM_SPRINTS]` | 4 | Count of sprints in report |
| `[SPRINT1_PERIOD]` | 2025-12-31 to 2026-01-13 | Sprint 1 section |
| `[SPRINT1_WORKING_DAYS]` | 9 | Sprint 1 "Working Days" |
| `[SPRINT1_CAPACITY]` | 96.8 | Sprint 1 "GCC Team Capacity" |
| `[SPRINT1_TEAM_MEMBERS]` | (See below) | Sprint 1 team table |

### Step 4: Format Team Members Data

#### For Simple HTML Template:
Replace the example rows in the `<tbody>` section with actual data. Each team member row should be formatted as:
```html
<tr>
    <td>200071</td>
    <td>BindhuMadhuri Maddela</td>
    <td>Jan 12</td>
    <td>Jan 01</td>
</tr>
```

For rows with planned leave, add `class="highlight"` to highlight them in yellow:
```html
<tr class="highlight">
    <td>200071</td>
    <td>BindhuMadhuri Maddela</td>
    <td>Jan 12</td>
    <td>Jan 01</td>
</tr>
```

#### For Text Template:
Each team member row should be formatted as:
```
200071     BindhuMadhuri Maddela          Jan 12               Jan 01
```

### Step 5: Send the Email

#### For HTML Email:
1. Open the completed template in a web browser
2. Select all content (Ctrl+A)
3. Copy (Ctrl+C)
4. Paste into your email client's compose window
5. Add recipients and send

#### For Plain Text Email:
1. Copy the entire content of the completed template
2. Paste into your email client's compose window
3. Add recipients and send

## Tips

- **Test First**: Send a test email to yourself before sending to the team
- **Subject Line**: Use a clear subject like "Sprint Capacity Report - Next 2 Sprints (Sprint 2 & 3)"
- **Recipients**: Include Scrum Master, Product Owner, and team members
- **Timing**: Send the report on the **last day of the current sprint**
- **Attachments**: Consider attaching the generated HTML report as a backup
- **Next 2 Sprints Only**: The simple templates show only the next 2 upcoming sprints (not the current sprint)
- **Highlighting**: Use the `class="highlight"` attribute to highlight rows with planned leave in yellow
- **Sprint Selection**: Always use Sprint 2 and Sprint 3 data when sending on the last day of Sprint 1

## Capacity Color Coding

The HTML template uses color coding for capacity percentages:
- 🟢 **Green (>= 80%)**: Healthy capacity
- 🟡 **Yellow (60-79%)**: Needs attention
- 🔴 **Red (< 60%)**: Critical - action required

## Future Enhancement

This is a temporary solution. In the future, the tool will automatically:
- Generate and send emails programmatically
- Auto-populate all data from the reports
- Support multiple recipients from configuration
- Include attachments automatically

## Troubleshooting

**Q: The HTML email looks broken in my email client**
- Try using the plain text template instead
- Some email clients strip certain HTML/CSS

**Q: The formatting is off when I paste**
- Make sure you're pasting into a rich text editor (not plain text mode)
- Try "Paste Special" > "Keep Source Formatting"

**Q: Where do I find the latest report?**
- Check the `reports` folder
- Files are named with timestamp: `sprint_capacity_report_YYYYMMDD_HHMMSS.*`
- Use the most recent file

## Contact

For questions or issues with the templates, please contact your Scrum Master or the tool administrator.

