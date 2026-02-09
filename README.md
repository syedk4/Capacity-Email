# 🚀 Sprint Capacity Automation System

> Automate your Agile team's capacity planning with intelligent leave tracking and sprint analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](README.md)

## 📋 Overview

The **Sprint Capacity Automation System** is a comprehensive tool designed for Agile teams working in 2-week sprint cycles. It automates the tedious process of collecting team leave plans, calculating sprint capacity, and generating professional reports for Scrum Masters.

### ✨ Key Features

- 📊 **Automated Capacity Calculation** - Instantly calculate team capacity for upcoming sprints
- 📅 **Intelligent Date Parsing** - Extracts dates from natural language text
- 📧 **Email Automation** - Automatically send reports to Scrum Masters
- 🌐 **Web Dashboard** - Modern web interface for real-time viewing
- 📄 **Multi-Format Reports** - Generate both text and HTML reports
- 🔧 **Highly Configurable** - Customize sprint dates, durations, and settings
- 🎯 **Multiple Leave Types** - Support for planned leave, public holidays, and optional holidays

## 🎯 Problem Solved

### Before (Manual Process)
- ❌ Manually collect leave plans from team members
- ❌ Calculate capacity using spreadsheets
- ❌ Error-prone manual calculations
- ❌ Time-consuming report generation
- ❌ Inconsistent reporting format

### After (Automated)
- ✅ One-click capacity analysis
- ✅ Accurate calculations every time
- ✅ Professional reports in seconds
- ✅ Automatic email delivery
- ✅ Real-time web dashboard

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Prepare your data**
   - Update `CapacityUpdate.xlsx` with your team's leave plans
   - Configure `config.json` with your settings

4. **Run the analysis**
```bash
python sprint_capacity_app.py --analyze
```

That's it! Your reports will be generated automatically.

## 📊 Usage

### Method 1: Command Line Interface

```bash
# Run capacity analysis
python sprint_capacity_app.py --analyze

# Setup configuration interactively
python sprint_capacity_app.py --setup

# Use custom Excel file
python sprint_capacity_app.py --excel-file "MyTeamLeave.xlsx"

# Specify output directory
python sprint_capacity_app.py --analyze --output-dir "./reports"
```

### Method 2: Simple Launcher

```bash
python run_capacity_analysis.py
```

### Method 3: Web Interface

```bash
python web_app.py
```
Then open your browser to `http://localhost:5000`

### Method 4: Manual Email Templates

For sending capacity reports via email manually:

1. **Navigate to the Email Templates folder**
   ```bash
   cd Email_Templates
   ```

2. **Read the timing guide first**
   - Open `IMPORTANT_EMAIL_TIMING.md` to understand when to send

3. **Use the simple template**
   - Open `email_template_simple.html` in a text editor
   - Fill in Sprint 2 and Sprint 3 data from your generated report
   - Preview in browser, then copy and paste to your email

4. **See the example**
   - Open `email_template_simple_SAMPLE.html` in a browser to see how it should look

📧 **Important**: Email should be sent on the **last day of the current sprint** and show the **next 2 upcoming sprints** (not the current sprint).

For detailed instructions, see `Email_Templates/README.md`

## 📁 Project Structure

```
Capacity Email/
├── sprint_capacity_app.py      # Main application
├── web_app.py                   # Web interface
├── run_capacity_analysis.py    # Simple launcher
├── config.json                  # Configuration
├── requirements.txt             # Dependencies
├── CapacityUpdate.xlsx          # Input data
├── README.md                    # This file
├── PROJECT_ANALYSIS.md          # Detailed analysis
├── Email_Templates/             # 📧 Email templates folder
│   ├── README.md                # Email templates guide
│   ├── IMPORTANT_EMAIL_TIMING.md # ⚠️ When to send emails
│   ├── email_template_simple.html # Recommended template
│   ├── email_template_simple_SAMPLE.html # Example
│   └── ... (other templates and docs)
└── reports/                     # Generated reports
```

## ⚙️ Configuration

Edit `config.json` to customize the application:

```json
{
  "sprint_start_date": "2025-01-06",
  "sprint_duration_days": 14,
  "excel_file_path": "CapacityUpdate.xlsx",
  "email_settings": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@example.com",
    "sender_password": "your-app-password",
    "scrum_master_email": "scrum-master@example.com"
  }
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `sprint_start_date` | First sprint start date (YYYY-MM-DD) | 2025-01-06 |
| `sprint_duration_days` | Sprint length in days | 14 |
| `excel_file_path` | Path to Excel file | CapacityUpdate.xlsx |
| `email_settings` | SMTP configuration for email | See above |

## 📊 Excel File Format

Your `CapacityUpdate.xlsx` should have these columns:

| Emp Id | Emp Name | August Planned Leave | Public Holiday | Optional Holiday |
|--------|----------|---------------------|----------------|------------------|
| 200071 | John Doe | 1st & 4th | 15th (Independence day) | - |
| 200325 | Jane Smith | 28th & 29th | - | - |

**Supported Date Formats:**
- `1st`, `2nd`, `3rd`, `4th`, etc.
- `14th August`
- `1st & 4th`
- `23rd and 29th September`

## 📈 Sample Output

### Console Output
```
============================================================
SPRINT CAPACITY ANALYSIS SUMMARY
============================================================
Analysis Date: 2025-12-28 06:37:19
Team Members Analyzed: 7
Sprints Analyzed: 4
Reports Generated: sprint_capacity_report_20251228_063719.txt
Email Sent: No

🟢 Sprint 1: 85.7% capacity (6/7 available)
🟢 Sprint 2: 100.0% capacity (7/7 available)
🟢 Sprint 3: 100.0% capacity (7/7 available)
🟢 Sprint 4: 100.0% capacity (7/7 available)
============================================================
```

### Generated Reports

**Text Report** (`sprint_capacity_report_*.txt`)
- Clean, readable format
- Easy to share via email
- Suitable for documentation

**HTML Report** (`sprint_capacity_report_*.html`)
- Professional styling
- Color-coded capacity indicators
- Browser-friendly viewing

## 🎨 Web Dashboard

The web interface provides:
- 📊 Real-time capacity visualization
- 🔄 One-click analysis execution
- 📥 Report downloads
- 📈 Interactive sprint cards
- 🎯 Capacity status indicators

## 📧 Email Automation

### Gmail Setup (Recommended)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App Passwords
   - Generate password for "Mail"
3. Use the app password in `config.json`

### Other Email Providers

Update SMTP settings in `config.json`:
- **Outlook:** `smtp.office365.com:587`
- **Yahoo:** `smtp.mail.yahoo.com:587`
- **Custom:** Your organization's SMTP server

## 🔍 How It Works

1. **Data Collection** - Reads team leave data from Excel file
2. **Date Parsing** - Intelligently extracts dates from text
3. **Sprint Calculation** - Determines current and upcoming sprints
4. **Capacity Analysis** - Calculates availability for each sprint
5. **Report Generation** - Creates professional reports
6. **Distribution** - Emails reports and saves to files

## 💡 Tips & Best Practices

### For Team Members
- Update Excel file before sprint planning
- Use consistent date formats
- Include leave type (planned/public/optional)
- Update as soon as leave plans change

### For Scrum Masters
- Run analysis 1-2 days before sprint planning
- Review capacity trends across sprints
- Plan sprint backlog based on capacity
- Archive reports for historical reference

### For Administrators
- Schedule weekly automated runs
- Monitor log files for errors
- Keep Excel template standardized
- Backup configuration regularly

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
pip install -r requirements.txt
```

**File Not Found**
- Check Excel file path in `config.json`
- Ensure file is in the correct directory

**Email Fails**
- Verify SMTP settings
- Check email credentials
- Enable "Less secure app access" or use app passwords

**Wrong Sprint Dates**
- Update `sprint_start_date` in `config.json`
- Ensure date format is YYYY-MM-DD

### Logs

Check `sprint_capacity.log` for detailed error messages and execution history.

## 📊 Technical Details

### Technology Stack
- **Language:** Python 3.8+
- **Data Processing:** pandas, numpy
- **Excel:** openpyxl
- **Web:** Flask
- **Email:** smtplib

### Architecture
- Object-oriented design
- Dataclass-based models
- Separation of concerns
- RESTful API (web interface)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Database integration for historical data
- Multi-team support
- Calendar integration (Google/Outlook)
- Mobile app
- Advanced analytics and forecasting

## 📄 License

This project is licensed under the MIT License.

## 👥 Support

For issues, questions, or suggestions:
- Check `PROJECT_ANALYSIS.md` for detailed documentation
- Review `sprint_capacity.log` for error details
- Contact your system administrator

## 🎓 Learn More

- **PROJECT_ANALYSIS.md** - Comprehensive project analysis
- **sprint_capacity.log** - Execution logs
- **config.json** - Configuration reference

---

**Made with ❤️ for Agile Teams**

*Automate capacity planning. Focus on delivering value.*

