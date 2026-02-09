#!/usr/bin/env python3
"""
Sprint Capacity Automation Application

This application automates the process of collecting team leave plans
and generating capacity reports for Agile sprint planning.

Features:
- Parse Excel files with team leave data
- Calculate 2-week sprint periods
- Generate capacity reports for scrum masters
- Email automation for report delivery
- Support for multiple leave types (planned, public holidays, optional)

Author: Sprint Capacity Automation System
Date: 2025-09-09
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
from typing import Dict, List, Tuple, Optional, NamedTuple
import re
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sprint_capacity.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Employee:
    """Employee data structure"""
    emp_id: str
    name: str


@dataclass
class LeaveEntry:
    """Leave entry data structure"""
    employee: Employee
    leave_dates: List[date]
    leave_type: str  # 'planned', 'public_holiday', 'optional_holiday'
    description: str


@dataclass
class OnCallSchedule:
    """On-call schedule data structure"""
    start_date: date
    end_date: date
    primary: str
    secondary: str


@dataclass
class Sprint:
    """Sprint data structure"""
    number: int
    start_date: date
    end_date: date
    oncall_primary: str = ""
    oncall_secondary: str = ""

    def contains_date(self, check_date: date) -> bool:
        """Check if a date falls within this sprint"""
        return self.start_date <= check_date <= self.end_date

    def get_working_days(self, gcc_holidays: set = None) -> int:
        """Calculate working days in sprint (excluding weekends and GCC holidays)"""
        if gcc_holidays is None:
            gcc_holidays = set()

        working_days = 0
        current_date = self.start_date
        while current_date <= self.end_date:
            # Count only weekdays that are not GCC holidays
            if current_date.weekday() < 5 and current_date not in gcc_holidays:
                working_days += 1
            current_date += timedelta(days=1)
        return working_days


@dataclass
class SprintCapacity:
    """Sprint capacity calculation result"""
    sprint: Sprint
    total_team_members: int
    available_members: int
    members_on_leave: List[Tuple[Employee, str]]  # (employee, leave_reason)
    # All employees with their leave status
    all_members_status: List[Tuple[Employee, str]]
    capacity_percentage: float
    working_days: int
    ideal_capacity_hours: float  # Total capacity if everyone was available
    actual_capacity_hours: float  # Actual capacity after deductions


class SprintCapacityCalculator:
    """Main class for sprint capacity calculations"""

    def __init__(self, config_file: str = "config.json"):
        """Initialize the calculator with configuration"""
        self.config = self.load_config(config_file)
        self.employees: List[Employee] = []
        self.leave_entries: List[LeaveEntry] = []
        self.oncall_schedules: List[OnCallSchedule] = []

    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file and merge with environment variables"""
        default_config = {
            "sprint_start_date": "2025-01-06",  # First sprint start date
            "sprint_duration_days": 14,
            "excel_file_path": "CapacityUpdate.xlsx",
            "excel_sheet_name": "",  # Optional: specify sheet name, otherwise auto-detect
            "email_settings": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "scrum_master_email": ""
            },
            "team_members": []
        }

        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value

                # Override email settings with environment variables if they exist
                email_settings = config.get('email_settings', {})
                email_settings['smtp_server'] = os.getenv(
                    'GMAIL_SMTP_SERVER', email_settings.get('smtp_server', 'smtp.gmail.com'))
                email_settings['smtp_port'] = int(
                    os.getenv('GMAIL_SMTP_PORT', email_settings.get('smtp_port', 587)))
                email_settings['sender_email'] = os.getenv(
                    'GMAIL_SENDER_EMAIL', email_settings.get('sender_email', ''))
                email_settings['sender_password'] = os.getenv(
                    'GMAIL_SENDER_PASSWORD', email_settings.get('sender_password', ''))
                email_settings['scrum_master_email'] = os.getenv(
                    'SCRUM_MASTER_EMAIL', email_settings.get('scrum_master_email', ''))
                config['email_settings'] = email_settings

                # Debug: Log the email configuration
                logger.info(
                    f"Email config loaded - sender_email: {email_settings.get('sender_email')}, scrum_master_email: {email_settings.get('scrum_master_email')}")

                return config
            except Exception as e:
                logger.warning(
                    f"Error loading config file: {e}. Using defaults.")

        # Create default config file
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        logger.info(f"Created default config file: {config_file}")

        return default_config

    def parse_date_string(self, date_str: str, month: int, year: int) -> List[date]:
        """Parse date string and return list of dates

        Handles various formats:
        - Single: 15th, 15
        - Multiple: 1st, 4th, 15th
        - Range: 16 to 27, 16-27
        """
        if pd.isna(date_str) or not date_str or str(date_str).strip() == '':
            return []

        dates = []
        date_str = str(date_str).strip()

        # First, handle range patterns (e.g., "16 to 27" or "16-27")
        range_patterns = [
            # "16 to 27"
            r'(\d{1,2})(?:st|nd|rd|th)?\s+to\s+(\d{1,2})(?:st|nd|rd|th)?',
            r'(\d{1,2})(?:st|nd|rd|th)?\s*-\s*(\d{1,2})(?:st|nd|rd|th)?',    # "16-27"
        ]

        for pattern in range_patterns:
            range_matches = re.findall(pattern, date_str)
            for start_str, end_str in range_matches:
                try:
                    start_day = int(start_str)
                    end_day = int(end_str)

                    # Create dates for all days in range
                    if 1 <= start_day <= 31 and 1 <= end_day <= 31:
                        for day in range(start_day, end_day + 1):
                            try:
                                parsed_date = date(year, month, day)
                                if parsed_date not in dates:
                                    dates.append(parsed_date)
                            except ValueError:
                                # Invalid date (e.g., Feb 30)
                                continue
                except ValueError:
                    continue

            # Remove the matched ranges from the string to avoid double-processing
            date_str = re.sub(pattern, '', date_str)

        # Then handle individual dates
        patterns = [
            # 1st, 2nd, 3rd, 4th, or just numbers
            r'(\d{1,2})(?:st|nd|rd|th)?',
            r'(\d{1,2})',  # Simple numbers
        ]

        for pattern in patterns:
            matches = re.findall(pattern, date_str)
            for match in matches:
                try:
                    day = int(match)
                    if 1 <= day <= 31:
                        try:
                            parsed_date = date(year, month, day)
                            if parsed_date not in dates:
                                dates.append(parsed_date)
                        except ValueError:
                            # Invalid date (e.g., Feb 30)
                            continue
                except ValueError:
                    continue

        return sorted(dates)

    def format_dates_as_ranges(self, dates: List[date]) -> str:
        """Format a list of dates as ranges where possible

        Example: [Feb 16, Feb 17, Feb 18, Feb 19, Feb 20, Feb 21, Feb 22, Feb 23, Feb 24]
        Returns: "Feb 16-24"

        Example: [Feb 16, Feb 17, Feb 18, Feb 20, Feb 21]
        Returns: "Feb 16-18, Feb 20-21"
        """
        if not dates:
            return ""

        sorted_dates = sorted(dates)
        ranges = []
        range_start = sorted_dates[0]
        range_end = sorted_dates[0]

        for i in range(1, len(sorted_dates)):
            current_date = sorted_dates[i]
            # Check if current date is consecutive (next day)
            if (current_date - range_end).days == 1:
                # Extend the range
                range_end = current_date
            else:
                # Range is broken, save the current range and start a new one
                if range_start == range_end:
                    # Single date
                    ranges.append(range_start.strftime("%b %d"))
                else:
                    # Date range
                    ranges.append(
                        f"{range_start.strftime('%b %d')}-{range_end.strftime('%d')}")
                range_start = current_date
                range_end = current_date

        # Don't forget the last range
        if range_start == range_end:
            ranges.append(range_start.strftime("%b %d"))
        else:
            ranges.append(
                f"{range_start.strftime('%b %d')}-{range_end.strftime('%d')}")

        return ", ".join(ranges)

    def determine_month_year(self, column_name: str) -> Tuple[int, int]:
        """Determine month and year from column name"""
        current_year = datetime.now().year

        # Extract month from column name
        month_mapping = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }

        column_lower = column_name.lower()
        for month_name, month_num in month_mapping.items():
            if month_name in column_lower:
                return month_num, current_year

        # Default to current month if not found
        return datetime.now().month, current_year


class ExcelDataParser:
    """Parser for Excel capacity data"""

    def __init__(self, calculator: SprintCapacityCalculator):
        self.calculator = calculator

    def parse_excel_file(self, file_path: str) -> Tuple[List[Employee], List[LeaveEntry]]:
        """Parse Excel file and extract employee and leave data

        This parser handles Excel files where data is organized by month in row groups.
        Each month section starts with a header row containing month names in column headers.
        Automatically detects and uses the current year's sheet.
        """
        try:
            # Get current year
            current_year = datetime.now().year

            # Read Excel file and get all sheet names
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            logger.info(f"Available sheets in Excel file: {sheet_names}")

            # Check if sheet name is specified in config
            sheet_name = None
            config_sheet_name = self.calculator.config.get(
                'excel_sheet_name', None)

            if config_sheet_name:
                # Use sheet name from config if specified
                if config_sheet_name in sheet_names:
                    sheet_name = config_sheet_name
                    logger.info(f"Using sheet from config: {sheet_name}")
                else:
                    logger.warning(
                        f"Configured sheet '{config_sheet_name}' not found in {sheet_names}")

            # If no config sheet or not found, try to find sheet with current year name
            if not sheet_name:
                if str(current_year) in sheet_names:
                    sheet_name = str(current_year)
                    logger.info(f"Using sheet for current year: {sheet_name}")
                else:
                    # Fallback to first sheet if current year sheet not found
                    sheet_name = sheet_names[0] if sheet_names else None
                    logger.warning(
                        f"Sheet '{current_year}' not found. Using default sheet: {sheet_name}")

            if not sheet_name:
                raise ValueError("No sheets found in Excel file")

            # Read the specific sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(
                f"Successfully loaded Excel file: {file_path}, Sheet: {sheet_name}")
            logger.info(f"Data shape: {df.shape}")

            # Detect the correct column name for Employee ID
            # Different sheets may use different column names
            emp_id_column = None
            emp_name_column = None

            # Check first row for actual headers
            first_row = df.iloc[0] if len(df) > 0 else None
            if first_row is not None:
                for col in df.columns:
                    cell_value = str(first_row[col]).strip(
                    ) if not pd.isna(first_row[col]) else ''
                    if cell_value == 'Emp Id':
                        emp_id_column = col
                    elif cell_value == 'Emp Name':
                        emp_name_column = col

            # If not found in first row, check column names directly
            if emp_id_column is None:
                if 'Emp Id' in df.columns:
                    emp_id_column = 'Emp Id'
                else:
                    # Use first column as fallback
                    emp_id_column = df.columns[0]
                    logger.info(
                        f"Using first column as Emp Id column: {emp_id_column}")

            if emp_name_column is None:
                if 'Emp Name' in df.columns:
                    emp_name_column = 'Emp Name'
                else:
                    # Use second column as fallback
                    emp_name_column = df.columns[1] if len(
                        df.columns) > 1 else None
                    logger.info(
                        f"Using second column as Emp Name column: {emp_name_column}")

            logger.info(
                f"Detected columns - Emp Id: {emp_id_column}, Emp Name: {emp_name_column}")

            employees = []
            leave_entries = []

            # Parse the multi-month structure
            current_month = None
            current_year = datetime.now().year

            # Map column names to their actual headers from the first header row
            column_headers = {}

            for idx, row in df.iterrows():
                emp_id_val = str(row[emp_id_column]).strip(
                ) if not pd.isna(row[emp_id_column]) else ''

                # Check if this is a month separator row
                # These rows have "Finance Systems" or similar in the first column and a month name in the third column
                month_col = df.columns[2]  # Third column
                month_val_str = str(row[month_col]).strip(
                ) if not pd.isna(row[month_col]) else ''

                month_mapping = {
                    'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
                    'apr': 4, 'april': 4, 'may': 5, 'june': 6, 'jul': 7, 'july': 7,
                    'aug': 8, 'august': 8, 'sep': 9, 'september': 9, 'oct': 10, 'october': 10,
                    'nov': 11, 'november': 11, 'dec': 12, 'december': 12
                }

                # Check if this row is a month separator (has month name in third column)
                if emp_id_val in ['Finance Systems', 'Emp Id'] or emp_id_val == '':
                    for month_name, month_num in month_mapping.items():
                        if month_name == month_val_str.lower():
                            current_month = month_num
                            # Keep the current year or infer it
                            if current_month < datetime.now().month:
                                current_year = datetime.now().year + 1
                            else:
                                current_year = datetime.now().year
                            logger.info(
                                f"Found month separator: {month_name.title()} {current_year} (month {month_num})")
                            break

                # Check if this is a month header row
                # Header rows have 'Emp Id' in the Emp Id column
                if emp_id_val == 'Emp Id':
                    # Map column names to their actual header values
                    for col in df.columns:
                        header_val = str(row[col]).strip(
                        ) if not pd.isna(row[col]) else ''
                        if header_val and header_val not in ['Emp Id', 'Emp Name']:
                            column_headers[col] = header_val

                    # Extract month from the third column (which contains month name)
                    month_header = str(row[month_col]).strip(
                    ) if not pd.isna(row[month_col]) else ''

                    # Determine month from header if not already set by separator
                    if 'planned' not in month_header.lower():
                        for month_name, month_num in month_mapping.items():
                            if month_name in month_header.lower():
                                current_month = month_num

                                # Extract year from header if present (e.g., "2026 January")
                                import re
                                year_match = re.search(
                                    r'(20\d{2})', month_header)
                                if year_match:
                                    current_year = int(year_match.group(1))
                                else:
                                    # If no year in header, infer based on month
                                    # If month is earlier than current month, assume next year
                                    if current_month < datetime.now().month:
                                        current_year = datetime.now().year + 1
                                    else:
                                        current_year = datetime.now().year

                                logger.info(
                                    f"Found month section: {month_name.title()} {current_year} (month {month_num})")
                                break

                    continue  # Skip header row

                # Check if this row is a month separator (has datetime in planned leave column)
                month_val = row[month_col]
                if pd.notna(month_val) and isinstance(month_val, datetime):
                    # Only use datetime if we haven't already detected month from string
                    if current_month is None:
                        current_month = month_val.month
                        current_year = month_val.year
                        logger.info(
                            f"Found month section from datetime: {month_val.strftime('%B %Y')} (month {current_month})")
                    continue

                # Skip rows without valid employee ID
                if not emp_id_val or not emp_id_val.isdigit():
                    continue

                # If we haven't found a month yet, try to extract from column names
                if current_month is None:
                    for col in df.columns:
                        # Handle datetime columns
                        if isinstance(col, datetime):
                            current_month = col.month
                            current_year = col.year
                            logger.info(
                                f"Inferred month from datetime column: {col.strftime('%B %Y')} (month {current_month})")
                            break

                        # Handle string columns
                        col_str = str(col)
                        month_mapping = {
                            'january': 1, 'february': 2, 'march': 3, 'april': 4,
                            'may': 5, 'june': 6, 'july': 7, 'august': 8,
                            'september': 9, 'october': 10, 'november': 11, 'december': 12
                        }
                        for month_name, month_num in month_mapping.items():
                            if month_name in col_str.lower():
                                current_month = month_num
                                logger.info(
                                    f"Inferred month from column: {month_name.title()} (month {month_num})")
                                break
                        if current_month:
                            break

                # Create employee
                emp_name_val = ''
                if emp_name_column:
                    emp_name_val = str(row[emp_name_column]).strip() if not pd.isna(
                        row[emp_name_column]) else ''

                employee = Employee(
                    emp_id=emp_id_val,
                    name=emp_name_val
                )

                if employee not in employees:
                    employees.append(employee)

                # Process leave columns for this employee
                # Skip the ID and Name columns
                skip_columns = [emp_id_column, emp_name_column] if emp_name_column else [
                    emp_id_column]
                # Add any other columns to skip
                skip_columns.extend(['Unnamed: 5'])

                # Find the "Opting?" column to check if optional holidays are opted
                opting_column = None
                for col in df.columns:
                    header_val = column_headers.get(col, str(col))
                    if 'opting' in str(header_val).lower():
                        opting_column = col
                        break

                # Get the opting value for this employee
                is_opting_optional_holiday = False
                if opting_column is not None:
                    opting_value = str(row[opting_column]).strip(
                    ).lower() if not pd.isna(row[opting_column]) else ''
                    is_opting_optional_holiday = opting_value in [
                        'yes', 'y', 'true']

                for col in df.columns:
                    if col in skip_columns:
                        continue

                    leave_value = row[col]
                    if pd.isna(leave_value) or str(leave_value).strip() == '':
                        continue

                    # Skip if this looks like a header value
                    leave_value_str = str(leave_value).strip()
                    if leave_value_str in ['Public Holiday', 'Optional Holiday', 'Planned Leave', 'Holiday', 'Opting?', 'GCC Holiday', 'NA', 'No', 'Yes']:
                        continue

                    # Determine leave type using the actual header value if available
                    header_name = column_headers.get(col, col)
                    leave_type = self.determine_leave_type(header_name)

                    # Skip optional holidays if employee is not opting for them
                    if leave_type == 'optional_holiday' and not is_opting_optional_holiday:
                        continue

                    # Use current month context
                    month = current_month if current_month else datetime.now().month
                    year = current_year

                    # Parse dates
                    leave_dates = self.calculator.parse_date_string(
                        leave_value_str, month, year)

                    if leave_dates:
                        leave_entry = LeaveEntry(
                            employee=employee,
                            leave_dates=leave_dates,
                            leave_type=leave_type,
                            description=leave_value_str
                        )
                        leave_entries.append(leave_entry)

            # Return all leave entries (both past and future)
            # This allows users to see complete leave history in reports
            logger.info(
                f"Parsed {len(employees)} employees and {len(leave_entries)} total leave entries")
            return employees, leave_entries

        except Exception as e:
            logger.error(f"Error parsing Excel file: {e}")
            raise

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe by removing duplicate headers and invalid rows"""
        # Find rows where 'Emp Id' column contains 'Emp Id' (header rows)
        header_mask = df['Emp Id'].astype(str).str.contains('Emp Id', na=False)

        # Remove header rows that appear in the middle of data
        df_clean = df[~header_mask].copy()

        # Reset index
        df_clean.reset_index(drop=True, inplace=True)

        return df_clean

    def determine_leave_type(self, column_name) -> str:
        """Determine leave type from column name"""
        # Handle datetime columns
        if isinstance(column_name, datetime):
            return 'planned'

        # Convert to string and check
        column_lower = str(column_name).lower()

        # Check for GCC Holiday or Public Holiday
        if 'gcc' in column_lower or 'public' in column_lower:
            return 'public_holiday'
        elif 'optional' in column_lower and 'holiday' in column_lower:
            return 'optional_holiday'
        elif 'holiday' in column_lower:
            return 'public_holiday'
        else:
            return 'planned'

    def parse_oncall_schedules(self, file_path: str) -> List[OnCallSchedule]:
        """Parse on-call schedules from the 'On Call Schedules' sheet"""
        try:
            # Read the On Call Schedules sheet
            excel_file = pd.ExcelFile(file_path)
            if 'On Call Schedules' not in excel_file.sheet_names:
                logger.warning(
                    "'On Call Schedules' sheet not found in Excel file")
                return []

            df = pd.read_excel(file_path, sheet_name='On Call Schedules')
            logger.info(f"Reading On Call Schedules sheet, shape: {df.shape}")

            oncall_schedules = []
            current_year = datetime.now().year

            for idx, row in df.iterrows():
                try:
                    # Get year (default to current year if not specified)
                    year = int(row['Year']) if pd.notna(
                        row['Year']) else current_year

                    # Get month
                    month_str = str(row['Month']).strip(
                    ) if pd.notna(row['Month']) else ''
                    month_mapping = {
                        'jan': 1, 'january': 1,
                        'feb': 2, 'february': 2,
                        'mar': 3, 'march': 3,
                        'apr': 4, 'april': 4,
                        'may': 5,
                        'jun': 6, 'june': 6,
                        'jul': 7, 'july': 7,
                        'aug': 8, 'august': 8,
                        'sep': 9, 'september': 9,
                        'oct': 10, 'october': 10,
                        'nov': 11, 'november': 11,
                        'dec': 12, 'december': 12
                    }
                    month = month_mapping.get(month_str.lower(), None)
                    if not month:
                        logger.warning(f"Could not parse month: {month_str}")
                        continue

                    # Parse start and end dates
                    from_date_str = str(row['From Date']).strip(
                    ) if pd.notna(row['From Date']) else ''
                    to_date_str = str(row['To date']).strip(
                    ) if pd.notna(row['To date']) else ''

                    # Extract day numbers from strings like "31st", "13th", "14th", "27th"
                    from_day = int(
                        re.search(r'(\d+)', from_date_str).group(1)) if from_date_str else 1
                    to_day_match = re.search(r'(\d+)', to_date_str)

                    # Handle month transitions (e.g., "Dec 31st - Jan 13th")
                    to_month = month
                    to_year = year
                    if to_day_match:
                        to_day = int(to_day_match.group(1))
                        # If to_day < from_day, it's likely next month
                        if to_day < from_day:
                            to_month = month + 1 if month < 12 else 1
                            if to_month == 1:
                                to_year = year + 1
                    else:
                        to_day = from_day

                    start_date = date(year, month, from_day)
                    end_date = date(to_year, to_month, to_day)

                    # Get primary and secondary on-call persons
                    primary = str(row['Primary']).strip(
                    ) if pd.notna(row['Primary']) else ''
                    secondary = str(row['Secondary']).strip(
                    ) if pd.notna(row['Secondary']) else ''

                    oncall = OnCallSchedule(
                        start_date=start_date,
                        end_date=end_date,
                        primary=primary,
                        secondary=secondary
                    )
                    oncall_schedules.append(oncall)
                    logger.info(
                        f"Parsed on-call: {start_date} to {end_date}, Primary: {primary}, Secondary: {secondary}")

                except Exception as e:
                    logger.warning(f"Error parsing on-call row {idx}: {e}")
                    continue

            logger.info(f"Parsed {len(oncall_schedules)} on-call schedules")
            return oncall_schedules

        except Exception as e:
            logger.error(f"Error parsing on-call schedules: {e}")
            return []


class SprintManager:
    """Manages sprint calculations and capacity analysis"""

    def __init__(self, calculator: SprintCapacityCalculator):
        self.calculator = calculator

    def calculate_sprints(self, start_date: date, num_sprints: int = 6, oncall_schedules: List[OnCallSchedule] = None) -> List[Sprint]:
        """Calculate sprint periods starting from given date"""
        sprints = []
        current_start = start_date

        for i in range(num_sprints):
            sprint_end = current_start + \
                timedelta(
                    days=self.calculator.config['sprint_duration_days'] - 1)
            sprint = Sprint(
                number=i + 1,
                start_date=current_start,
                end_date=sprint_end
            )

            # Assign on-call information if available
            if oncall_schedules:
                self.assign_oncall_to_sprint(sprint, oncall_schedules)

            sprints.append(sprint)
            current_start = sprint_end + timedelta(days=1)

        return sprints

    def assign_oncall_to_sprint(self, sprint: Sprint, oncall_schedules: List[OnCallSchedule]):
        """Assign on-call information to a sprint based on date overlap"""
        # Find the on-call schedule that overlaps with this sprint
        for oncall in oncall_schedules:
            # Check if there's any overlap between sprint and on-call period
            if (oncall.start_date <= sprint.end_date and oncall.end_date >= sprint.start_date):
                sprint.oncall_primary = oncall.primary
                sprint.oncall_secondary = oncall.secondary
                logger.info(
                    f"Assigned on-call to Sprint {sprint.number}: Primary={oncall.primary}, Secondary={oncall.secondary}")
                break  # Use the first matching schedule

    def get_current_and_upcoming_sprints(self, oncall_schedules: List[OnCallSchedule] = None) -> List[Sprint]:
        """Get current and upcoming sprints based on today's date"""
        today = date.today()
        sprint_start_str = self.calculator.config['sprint_start_date']
        first_sprint_start = datetime.strptime(
            sprint_start_str, '%Y-%m-%d').date()

        # Calculate which sprint we're currently in
        days_since_start = (today - first_sprint_start).days
        sprint_duration = self.calculator.config['sprint_duration_days']
        current_sprint_number = max(0, days_since_start // sprint_duration)

        # Generate all sprints from the first sprint
        # Include previous sprint (if available) + current + next 3 sprints
        # Include previous sprint if available
        start_index = max(0, current_sprint_number - 1)
        all_sprints = self.calculate_sprints(
            first_sprint_start, current_sprint_number + 5, oncall_schedules)

        # Return previous (if available), current, and next 3 sprints
        return all_sprints[start_index:start_index + 4]

    def calculate_sprint_capacity(self, sprint: Sprint) -> SprintCapacity:
        """Calculate capacity for a specific sprint"""
        total_members = len(self.calculator.employees)
        members_on_leave = []
        all_members_status = []

        # First, identify all GCC holidays (public holidays) in this sprint
        # These apply to EVERYONE
        gcc_holidays = set()

        # # Get GCC holidays from config
        # gcc_holiday_strings = self.calculator.config.get('gcc_holidays', [])
        # for holiday_str in gcc_holiday_strings:
        #     try:
        #         holiday_date = datetime.strptime(
        #             holiday_str, '%Y-%m-%d').date()
        #         if sprint.contains_date(holiday_date):
        #             gcc_holidays.add(holiday_date)
        #     except ValueError:
        #         logger.warning(
        #             f"Invalid GCC holiday date format: {holiday_str}")

        # Also check leave entries for public holidays
        for leave_entry in self.calculator.leave_entries:
            if leave_entry.leave_type == 'public_holiday':
                dates_in_sprint = [
                    leave_date for leave_date in leave_entry.leave_dates
                    if sprint.contains_date(leave_date)
                ]
                gcc_holidays.update(dates_in_sprint)

        # Format GCC holidays for display
        gcc_holidays_display = ""
        if gcc_holidays:
            gcc_date_strings = [d.strftime("%b %d")
                                for d in sorted(gcc_holidays)]
            gcc_holidays_display = ", ".join(gcc_date_strings)

        # Check each employee for leave during this sprint
        for employee in self.calculator.employees:
            leave_info_by_type = {}  # Group by leave type

            # Add GCC holidays to everyone (if any exist)
            if gcc_holidays_display:
                leave_info_by_type['public_holiday'] = [gcc_holidays_display]

            # Check all leave entries for this employee
            for leave_entry in self.calculator.leave_entries:
                if leave_entry.employee.emp_id == employee.emp_id:
                    # Get only the leave dates that fall within this sprint
                    dates_in_sprint = [
                        leave_date for leave_date in leave_entry.leave_dates
                        if sprint.contains_date(leave_date)
                    ]

                    if dates_in_sprint:
                        # Skip public holidays as we already added them above
                        if leave_entry.leave_type == 'public_holiday':
                            continue

                        # Format the dates as ranges where possible
                        dates_display = self.calculator.format_dates_as_ranges(
                            dates_in_sprint)

                        # Group by leave type
                        if leave_entry.leave_type not in leave_info_by_type:
                            leave_info_by_type[leave_entry.leave_type] = []
                        leave_info_by_type[leave_entry.leave_type].append(
                            dates_display)

            if leave_info_by_type:
                # Format leave reasons with dates
                leave_reasons = []
                for leave_type, date_lists in leave_info_by_type.items():
                    # If there's only one date list, use it directly (already formatted)
                    if len(date_lists) == 1:
                        all_dates = date_lists[0]
                    else:
                        # Multiple date lists need to be combined and re-sorted
                        # Combine all dates and sort them
                        all_date_strings = []
                        for date_list in date_lists:
                            all_date_strings.extend(
                                [d.strip() for d in date_list.split(', ')])

                        # Parse dates back to date objects for proper sorting
                        date_objects = []
                        for date_str in all_date_strings:
                            try:
                                # Parse "Jan 15" format back to date
                                parsed = datetime.strptime(
                                    f"{date_str} {sprint.start_date.year}", "%b %d %Y").date()
                                date_objects.append(parsed)
                            except:
                                # If parsing fails, keep the string as is
                                pass

                        # Sort and format as ranges where possible
                        if date_objects:
                            sorted_dates = sorted(date_objects)
                            all_dates = self.calculator.format_dates_as_ranges(
                                sorted_dates)
                        else:
                            all_dates = ", ".join(all_date_strings)

                    leave_reasons.append(f"{leave_type}: {all_dates}")

                leave_status = "; ".join(leave_reasons)

                # Check if employee has any PLANNED leave (exclude GCC holidays from capacity calc)
                has_planned_leave = any(
                    lt in ['planned', 'optional_holiday'] for lt in leave_info_by_type.keys())
                if has_planned_leave:
                    members_on_leave.append((employee, leave_status))

                all_members_status.append((employee, leave_status))
            else:
                # Employee has no leave - mark as available
                all_members_status.append((employee, "Available"))

        # Calculate working days excluding GCC holidays
        working_days = sprint.get_working_days(gcc_holidays)

        # Calculate GCC-based capacity
        # Total person-days available = total_members * working_days
        # For each member on leave, subtract their leave days from total
        total_person_days = total_members * working_days
        leave_person_days = 0

        for employee in self.calculator.employees:
            # Count only planned and optional holiday leave days (not GCC holidays)
            employee_leave_days = 0
            for leave_entry in self.calculator.leave_entries:
                if leave_entry.employee.emp_id == employee.emp_id:
                    if leave_entry.leave_type in ['planned', 'optional_holiday']:
                        # Count leave days that fall within this sprint and are working days
                        for leave_date in leave_entry.leave_dates:
                            if sprint.contains_date(leave_date) and leave_date.weekday() < 5 and leave_date not in gcc_holidays:
                                employee_leave_days += 1
            leave_person_days += employee_leave_days

        # Calculate capacity percentage
        available_person_days = total_person_days - leave_person_days
        capacity_percentage = (
            available_person_days / total_person_days * 100) if total_person_days > 0 else 0

        # For backward compatibility, keep available_members calculation
        available_members = total_members - len(members_on_leave)

        # Calculate ideal and actual capacity in hours (configurable hours per working day)
        HOURS_PER_DAY = self.calculator.config.get('hours_per_day', 6)
        ONCALL_REDUCTION_HOURS = self.calculator.config.get(
            'oncall_primary_hours_reduction', 3)

        # Calculate base capacity for regular team members (excluding on-call person)
        # We'll add on-call person's capacity separately
        regular_team_person_days = total_person_days
        regular_team_available_days = available_person_days

        # Find and handle on-call person separately
        oncall_employee = None
        oncall_ideal_hours = 0
        oncall_actual_hours = 0

        if sprint.oncall_primary:
            # Find the primary on-call employee
            oncall_name_lower = sprint.oncall_primary.strip().lower()

            for employee in self.calculator.employees:
                emp_name_lower = employee.name.strip().lower()

                # Try multiple matching strategies:
                # 1. Exact match
                if emp_name_lower == oncall_name_lower:
                    oncall_employee = employee
                    break

                # 2. One name contains the other
                if emp_name_lower in oncall_name_lower or oncall_name_lower in emp_name_lower:
                    oncall_employee = employee
                    break

                # 3. Match individual name parts (e.g., "Siva Guru" matches "Sivaguru")
                # Remove common separators and compare
                emp_name_parts = emp_name_lower.replace(
                    ',', ' ').replace('.', ' ').split()
                oncall_name_parts = oncall_name_lower.replace(
                    ',', ' ').replace('.', ' ').split()

                # Check if any significant part of oncall name matches employee name
                for oncall_part in oncall_name_parts:
                    if len(oncall_part) > 3:  # Only match significant parts (not "mr", "ms", etc.)
                        for emp_part in emp_name_parts:
                            if oncall_part in emp_part or emp_part in oncall_part:
                                oncall_employee = employee
                                break
                    if oncall_employee:
                        break

                if oncall_employee:
                    break

            if oncall_employee:
                # Calculate on-call person's working days
                # On-call person works on ALL weekdays (Mon-Fri) including GCC holidays
                oncall_working_days = 0
                current_date = sprint.start_date
                while current_date <= sprint.end_date:
                    # Count only weekdays (Mon-Fri), holidays ARE working days for on-call
                    if current_date.weekday() < 5:
                        oncall_working_days += 1
                    current_date += timedelta(days=1)

                # Calculate on-call person's leave days
                oncall_leave_days = 0
                for leave_entry in self.calculator.leave_entries:
                    if leave_entry.employee.emp_id == oncall_employee.emp_id:
                        if leave_entry.leave_type in ['planned', 'optional_holiday']:
                            for leave_date in leave_entry.leave_dates:
                                if sprint.contains_date(leave_date) and leave_date.weekday() < 5:
                                    oncall_leave_days += 1

                # On-call person's available days (excluding leave)
                oncall_available_days = oncall_working_days - oncall_leave_days

                # On-call person works reduced hours per day (HOURS_PER_DAY - ONCALL_REDUCTION_HOURS)
                oncall_hours_per_day = HOURS_PER_DAY - ONCALL_REDUCTION_HOURS

                # Calculate on-call person's capacity
                oncall_ideal_hours = oncall_working_days * oncall_hours_per_day
                oncall_actual_hours = oncall_available_days * oncall_hours_per_day

                # Subtract on-call person from regular team calculation
                # Remove on-call person's days from regular team
                regular_team_person_days -= working_days
                # Adjust for on-call person
                regular_team_available_days -= (working_days -
                                                oncall_leave_days)

        # Calculate capacity for regular team members (6 people at full hours)
        regular_team_ideal_hours = regular_team_person_days * HOURS_PER_DAY
        regular_team_actual_hours = regular_team_available_days * HOURS_PER_DAY

        # Total capacity = Regular team + On-call person
        ideal_capacity_hours = regular_team_ideal_hours + oncall_ideal_hours
        actual_capacity_hours = regular_team_actual_hours + oncall_actual_hours

        # Calculate capacity percentage based on final values
        capacity_percentage = (
            actual_capacity_hours / ideal_capacity_hours * 100) if ideal_capacity_hours > 0 else 0

        return SprintCapacity(
            sprint=sprint,
            total_team_members=total_members,
            available_members=available_members,
            members_on_leave=members_on_leave,
            all_members_status=all_members_status,
            capacity_percentage=capacity_percentage,
            working_days=working_days,
            ideal_capacity_hours=ideal_capacity_hours,
            actual_capacity_hours=actual_capacity_hours
        )


class ReportGenerator:
    """Generates capacity reports for scrum masters"""

    def __init__(self, calculator: SprintCapacityCalculator):
        self.calculator = calculator

    def generate_text_report(self, sprint_capacities: List[SprintCapacity]) -> str:
        """Generate a text-based capacity report"""
        report_lines = []

        # Calculate absolute sprint number from reference date (2025-12-31)
        reference_date = datetime.strptime('2025-12-31', '%Y-%m-%d').date()

        report_lines.append("=" * 60)
        report_lines.append("SPRINT CAPACITY REPORT")
        report_lines.append("=" * 60)
        report_lines.append(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(
            f"Total Team Members: {sprint_capacities[0].total_team_members if sprint_capacities else 0}")
        report_lines.append("")

        for capacity in sprint_capacities:
            sprint = capacity.sprint
            # Calculate absolute sprint number from reference date
            days_from_reference = (sprint.start_date - reference_date).days
            absolute_sprint_number = (days_from_reference // 14) + 1
            report_lines.append(f"SPRINT {absolute_sprint_number}")
            report_lines.append(
                f"Period: {sprint.start_date.strftime('%Y-%m-%d')} to {sprint.end_date.strftime('%Y-%m-%d')}")
            report_lines.append(f"Working Days: {capacity.working_days}")
            report_lines.append(
                f"GCC Members Count: {capacity.total_team_members}")
            report_lines.append(
                f"GCC Team Capacity: {capacity.capacity_percentage:.1f}%")
            report_lines.append(
                f"Ideal Capacity: {capacity.ideal_capacity_hours:.1f} hours")
            report_lines.append(
                f"Actual Capacity: {capacity.actual_capacity_hours:.1f} hours")

            # Add on-call information if available
            if sprint.oncall_primary or sprint.oncall_secondary:
                report_lines.append(
                    f"On-Call Primary: {sprint.oncall_primary}")
                report_lines.append(
                    f"On-Call Secondary: {sprint.oncall_secondary}")

            # Show all team members with their status
            report_lines.append("\nTeam Member Status:")
            report_lines.append("")

            # Create table header
            report_lines.append(
                f"{'Emp Id':<10} {'Emp Name':<30} {'Planned Leave':<20} {'GCC Holiday':<20}")
            report_lines.append("-" * 92)

            for employee, reason in capacity.all_members_status:
                # Parse the leave reason to separate by type
                planned_leave = []
                gcc_holiday = []

                if reason != "Available":
                    # Split by semicolon to get different leave types
                    leave_parts = reason.split('; ')
                    for part in leave_parts:
                        if part.startswith('planned:'):
                            dates = part.replace('planned:', '').strip()
                            planned_leave.append(dates)
                        elif part.startswith('public_holiday:'):
                            dates = part.replace('public_holiday:', '').strip()
                            gcc_holiday.append(dates)
                        # Note: optional_holiday is still used in capacity calculation but not displayed

                planned_str = ', '.join(
                    planned_leave) if planned_leave else '-'
                gcc_str = ', '.join(gcc_holiday) if gcc_holiday else '-'

                # Truncate long strings for text display
                planned_display = (
                    planned_str[:17] + '...') if len(planned_str) > 20 else planned_str
                gcc_display = (
                    gcc_str[:17] + '...') if len(gcc_str) > 20 else gcc_str

                report_lines.append(
                    f"{employee.emp_id:<10} {employee.name:<30} {planned_display:<20} {gcc_display:<20}"
                )

            report_lines.append("-" * 40)
            report_lines.append("")

        return "\n".join(report_lines)

    def generate_html_report(self, sprint_capacities: List[SprintCapacity]) -> str:
        """Generate an HTML-based capacity report"""

        # Calculate absolute sprint number from reference date (2025-12-31)
        reference_date = datetime.strptime('2025-12-31', '%Y-%m-%d').date()

        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sprint Capacity Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1100px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .report-container {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background-color: #ffffff;
            padding: 30px;
            text-align: center;
            border-bottom: 3px solid #2563eb;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 600;
            color: #000000;
        }
        .header-subtitle {
            color: #64748b;
            font-size: 14px;
            margin-top: 8px;
        }
        .header-info {
            background-color: #f8fafc;
            padding: 20px 30px;
            border-bottom: 1px solid #e2e8f0;
        }
        .info-grid {
            width: 100%;
            border-collapse: separate;
            border-spacing: 15px;
        }
        .info-item {
            text-align: center;
            padding: 12px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .info-label {
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .info-value {
            font-size: 18px;
            color: #1e293b;
            font-weight: 700;
            margin-top: 4px;
        }
        .content {
            padding: 30px;
        }
        .sprint-section {
            margin-bottom: 30px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
        }
        .sprint-title {
            background-color: #2563eb;
            padding: 16px 24px;
            color: white;
            font-weight: 600;
            font-size: 16px;
        }
        .metrics-grid {
            width: 100%;
            border-collapse: collapse;
            background-color: #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
        }
        .metric-card {
            background: white;
            padding: 16px;
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        .metric-label {
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 20px;
            color: #1e293b;
            font-weight: 700;
        }
        .metric-value.capacity {
            font-size: 24px;
        }
        .metric-value.capacity.good {
            color: #10b981;
        }
        .metric-value.capacity.warning {
            color: #f59e0b;
        }
        .metric-value.capacity.critical {
            color: #ef4444;
        }
        .metric-value.oncall {
            font-size: 13px;
        }
        .team-status-header {
            background: #f8fafc;
            padding: 14px 24px;
            font-weight: 600;
            font-size: 13px;
            color: #475569;
            border-top: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
        }
        .team-table {
            width: 100%;
            border-collapse: collapse;
            background-color: #fff;
        }
        .team-table th {
            background-color: #e2e8f0;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            font-size: 12px;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .team-table td {
            padding: 12px 16px;
            font-size: 13px;
            color: #334155;
            border-bottom: 1px solid #f1f5f9;
        }
        .team-table tr:hover {
            background-color: #f8fafc;
        }
        .team-table tr.on-leave {
            background-color: #fef3c7;
        }
        .team-table tr.on-leave:hover {
            background-color: #fde68a;
        }
        .leave-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            margin: 2px;
        }
        .leave-planned {
            background: #fee2e2;
            color: #991b1b;
        }
        .leave-holiday {
            background: #dbeafe;
            color: #1e40af;
        }
    </style>
</head>
<body>
    <div class="report-container">
        <!-- Header -->
        <div class="header">
            <h1>📊 Sprint Capacity Report</h1>
            <div class="header-subtitle">Finance Aspirants Team - Sprint Planning</div>
        </div>

        <!-- Header Info -->
        <div class="header-info">
            <table class="info-grid">
                <tr>
                    <td class="info-item">
                        <div class="info-label">Generated</div>
                        <div class="info-value">""" + datetime.now().strftime('%Y-%m-%d') + """</div>
                    </td>
                    <td class="info-item">
                        <div class="info-label">Team Members</div>
                        <div class="info-value">""" + str(sprint_capacities[0].total_team_members if sprint_capacities else 0) + """</div>
                    </td>
                    <td class="info-item">
                        <div class="info-label">Sprints Shown</div>
                        <div class="info-value">""" + str(len(sprint_capacities)) + """</div>
                    </td>
                </tr>
            </table>
        </div>

        <!-- Content -->
        <div class="content">
"""

        for capacity in sprint_capacities:
            sprint = capacity.sprint

            # Calculate absolute sprint number from reference date
            days_from_reference = (sprint.start_date - reference_date).days
            absolute_sprint_number = (days_from_reference // 14) + 1

            # Determine capacity status color
            capacity_class = "good"
            if capacity.capacity_percentage < 80:
                capacity_class = "critical"
            elif capacity.capacity_percentage < 90:
                capacity_class = "warning"

            # Build on-call metric cells if available
            oncall_cells = ""
            if sprint.oncall_primary or sprint.oncall_secondary:
                oncall_cells = f"""
                    <td class="metric-card">
                        <div class="metric-label">On-Call Primary</div>
                        <div class="metric-value oncall">{sprint.oncall_primary or '-'}</div>
                    </td>
                    <td class="metric-card">
                        <div class="metric-label">On-Call Secondary</div>
                        <div class="metric-value oncall">{sprint.oncall_secondary or '-'}</div>
                    </td>"""

            html += f"""
            <!-- Sprint {absolute_sprint_number} -->
            <div class="sprint-section">
                <div class="sprint-title">
                    <span>Sprint {absolute_sprint_number} ({sprint.start_date.strftime('%b %d')} - {sprint.end_date.strftime('%b %d, %Y')})</span>
                </div>

                <table class="metrics-grid">
                    <tr>
                        <td class="metric-card">
                            <div class="metric-label">Working Days</div>
                            <div class="metric-value">{capacity.working_days}</div>
                        </td>
                        <td class="metric-card">
                            <div class="metric-label">Team Members</div>
                            <div class="metric-value">{capacity.total_team_members}</div>
                        </td>
                        <td class="metric-card">
                            <div class="metric-label">Team Capacity</div>
                            <div class="metric-value capacity {capacity_class}">{capacity.capacity_percentage:.1f}%</div>
                        </td>
                        <td class="metric-card">
                            <div class="metric-label">Ideal Capacity</div>
                            <div class="metric-value">{capacity.ideal_capacity_hours:.1f} hrs</div>
                        </td>
                        <td class="metric-card">
                            <div class="metric-label">Actual Capacity</div>
                            <div class="metric-value">{capacity.actual_capacity_hours:.1f} hrs</div>
                        </td>{oncall_cells}
                    </tr>
                </table>
            """

            # Show all team members with their status
            html += """
                <div class="team-status-header">👥 Team Member Status</div>

                <table class="team-table">
                    <thead>
                        <tr>
                            <th>Emp ID</th>
                            <th>Employee Name</th>
                            <th>Planned Leave</th>
                            <th>GCC Holiday</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            for employee, reason in capacity.all_members_status:
                # Parse the leave reason to separate by type
                planned_leave = []
                gcc_holiday = []

                if reason != "Available":
                    # Split by semicolon to get different leave types
                    leave_parts = reason.split('; ')
                    for part in leave_parts:
                        if part.startswith('planned:'):
                            dates = part.replace('planned:', '').strip()
                            planned_leave.append(dates)
                        elif part.startswith('public_holiday:'):
                            dates = part.replace('public_holiday:', '').strip()
                            gcc_holiday.append(dates)

                # Create badge HTML for planned leave
                planned_str = '-'
                if planned_leave:
                    badges = [
                        f'<span class="leave-badge leave-planned">{date}</span>' for date in planned_leave]
                    planned_str = ''.join(badges)

                # Create badge HTML for GCC holidays
                gcc_str = '-'
                if gcc_holiday:
                    badges = [
                        f'<span class="leave-badge leave-holiday">{date}</span>' for date in gcc_holiday]
                    gcc_str = ''.join(badges)

                # Highlight rows with any leave
                row_class = ' class="on-leave"' if (
                    planned_leave or gcc_holiday) else ''

                html += f"""
                        <tr{row_class}>
                            <td>{employee.emp_id}</td>
                            <td>{employee.name}</td>
                            <td>{planned_str}</td>
                            <td>{gcc_str}</td>
                        </tr>
                """

            html += """
                    </tbody>
                </table>
            </div>
            """

        html += """
        </div>
    </div>
</body>
</html>"""
        return html

    def generate_email_template(self, sprint_capacities: List[SprintCapacity]) -> str:
        """Generate a pre-filled email template with next 2 upcoming sprints"""
        # Show next 2 upcoming sprints (indices 2 and 3 from the 4 available sprints)
        # Available sprints: [Previous, Current, Next, Next+1]
        # Email template shows: [Next, Next+1]
        if len(sprint_capacities) < 4:
            logger.warning(
                "Not enough sprints to generate email template (need at least 4)")
            return ""

        # Use the same reference date as the text report for consistency
        reference_date = datetime.strptime('2025-12-31', '%Y-%m-%d').date()

        # Show next 2 upcoming sprints (skip previous and current)
        # Get indices 2 and 3 (Next and Next+1)
        sprints_to_show = sprint_capacities[2:4]
        sprint_labels = ["Next Sprint", "Next Sprint +1"]

        # Calculate absolute sprint numbers for all sprints
        absolute_sprint_numbers = []
        for sprint_cap in sprints_to_show:
            days_from_ref = (sprint_cap.sprint.start_date -
                             reference_date).days
            absolute_sprint_num = (days_from_ref // 14) + 1
            absolute_sprint_numbers.append(absolute_sprint_num)

        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sprint Capacity Report - Modern Design</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1100px;
            margin: 0 auto;
            padding: 0;
            background-color: #f5f5f5;
        }
        .email-container {
            background-color: #ffffff;
            margin: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background-color: #ffffff;
            padding: 30px;
            text-align: center;
            border-bottom: 3px solid #2563eb;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 600;
            color: #000000;
        }
        .header-subtitle {
            color: #64748b;
            font-size: 14px;
            margin-top: 8px;
        }
        .header-info {
            background-color: #f8fafc;
            padding: 20px 30px;
            border-bottom: 1px solid #e2e8f0;
        }
        .info-grid {
            width: 100%;
            border-collapse: separate;
            border-spacing: 15px;
        }
        .info-item {
            text-align: center;
            padding: 12px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .info-label {
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .info-value {
            font-size: 18px;
            color: #1e293b;
            font-weight: 700;
            margin-top: 4px;
        }
        .content {
            padding: 30px;
        }
        .sprint-section {
            margin-bottom: 30px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
        }
        .sprint-title {
            background-color: #2563eb;
            padding: 16px 24px;
            color: white;
            font-weight: 600;
            font-size: 16px;
        }
        .metrics-grid {
            width: 100%;
            border-collapse: collapse;
            background-color: #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
        }
        .metric-card {
            background: white;
            padding: 16px;
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        .metric-label {
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 20px;
            color: #1e293b;
            font-weight: 700;
        }
        .metric-value.capacity {
            font-size: 24px;
        }
        .metric-value.capacity.good {
            color: #10b981;
        }
        .metric-value.capacity.warning {
            color: #f59e0b;
        }
        .metric-value.capacity.critical {
            color: #ef4444;
        }
        .metric-value.oncall {
            font-size: 13px;
        }
        .team-status-header {
            background: #f8fafc;
            padding: 14px 24px;
            font-weight: 600;
            font-size: 13px;
            color: #475569;
            border-top: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
        }
        .team-table {
            width: 100%;
            border-collapse: collapse;
            background-color: #fff;
        }
        .team-table th {
            background-color: #e2e8f0;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            font-size: 12px;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .team-table td {
            padding: 12px 16px;
            font-size: 13px;
            color: #334155;
            border-bottom: 1px solid #f1f5f9;
        }
        .team-table tr:hover {
            background-color: #f8fafc;
        }
        .team-table tr.on-leave {
            background-color: #fef3c7;
        }
        .team-table tr.on-leave:hover {
            background-color: #fde68a;
        }
        .leave-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            margin: 2px;
        }
        .leave-planned {
            background: #fee2e2;
            color: #991b1b;
        }
        .leave-holiday {
            background: #dbeafe;
            color: #1e40af;
        }
        .footer {
            background: #f8fafc;
            padding: 20px 30px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
            border-top: 1px solid #e2e8f0;
        }
    </style>
</head>

<body>
    <div class="email-container">
        <!-- Header -->
        <div class="header">
            <h1>📊 Sprint Capacity Report</h1>
            <div class="header-subtitle">Finance Aspirants Team - Sprint Planning</div>
        </div>

        <!-- Header Info -->
        <div class="header-info">
            <table class="info-grid">
                <tr>
                    <td class="info-item">
                        <div class="info-label">Generated</div>
                        <div class="info-value">""" + datetime.now().strftime('%Y-%m-%d') + """</div>
                    </td>
                    <td class="info-item">
                        <div class="info-label">Team Members</div>
                        <div class="info-value">""" + str(sprints_to_show[0].total_team_members) + """</div>
                    </td>
                    <td class="info-item">
                        <div class="info-label">Sprints Shown</div>
                        <div class="info-value">Next 2</div>
                    </td>
                </tr>
            </table>
        </div>

        <!-- Content -->
        <div class="content">
"""

        # Generate HTML for all 2 sprints
        for idx, sprint_cap in enumerate(sprints_to_show):
            sprint_label = sprint_labels[idx]
            absolute_sprint_num = absolute_sprint_numbers[idx]

            # Determine capacity color class
            capacity_class = "good"
            if sprint_cap.capacity_percentage < 80:
                capacity_class = "critical"
            elif sprint_cap.capacity_percentage < 90:
                capacity_class = "warning"

            # Build on-call metric cells if available
            oncall_cells = ""
            if sprint_cap.sprint.oncall_primary or sprint_cap.sprint.oncall_secondary:
                oncall_cells = f"""
                    <td class="metric-card">
                        <div class="metric-label">On-Call Primary</div>
                        <div class="metric-value oncall">{sprint_cap.sprint.oncall_primary or '-'}</div>
                    </td>
                    <td class="metric-card">
                        <div class="metric-label">On-Call Secondary</div>
                        <div class="metric-value oncall">{sprint_cap.sprint.oncall_secondary or '-'}</div>
                    </td>"""

            html += f"""
            <!-- Sprint {idx + 1} -->
            <div class="sprint-section">
                <div class="sprint-title">
                    <span>Sprint {absolute_sprint_num} - {sprint_label} ({sprint_cap.sprint.start_date.strftime('%b %d')} - {sprint_cap.sprint.end_date.strftime('%b %d, %Y')})</span>
                </div>

                <table class="metrics-grid">
                    <tr>
                        <td class="metric-card">
                            <div class="metric-label">Working Days</div>
                            <div class="metric-value">{sprint_cap.working_days}</div>
                        </td>
                        <td class="metric-card">
                            <div class="metric-label">Team Members</div>
                            <div class="metric-value">{sprint_cap.total_team_members}</div>
                        </td>
                        <td class="metric-card">
                            <div class="metric-label">Team Capacity</div>
                            <div class="metric-value capacity {capacity_class}">{sprint_cap.capacity_percentage:.1f}%</div>
                        </td>
                        <td class="metric-card">
                            <div class="metric-label">Ideal Capacity</div>
                            <div class="metric-value">{sprint_cap.ideal_capacity_hours:.1f} hrs</div>
                        </td>
                        <td class="metric-card">
                            <div class="metric-label">Actual Capacity</div>
                            <div class="metric-value">{sprint_cap.actual_capacity_hours:.1f} hrs</div>
                        </td>{oncall_cells}
                    </tr>
                </table>

                <div class="team-status-header">👥 Team Member Status</div>

                <table class="team-table">
                    <thead>
                        <tr>
                            <th>Emp ID</th>
                            <th>Employee Name</th>
                            <th>Planned Leave</th>
                            <th>GCC Holiday</th>
                        </tr>
                    </thead>
                    <tbody>
"""

            # Add team members for this sprint
            for employee, reason in sprint_cap.all_members_status:
                planned_leave = []
                gcc_holiday = []

                if reason != "Available":
                    leave_parts = reason.split('; ')
                    for part in leave_parts:
                        if part.startswith('planned:'):
                            dates = part.replace('planned:', '').strip()
                            planned_leave.append(dates)
                        elif part.startswith('public_holiday:'):
                            dates = part.replace('public_holiday:', '').strip()
                            gcc_holiday.append(dates)

                # Create badge HTML for planned leave
                planned_str = '-'
                if planned_leave:
                    badges = [
                        f'<span class="leave-badge leave-planned">{date}</span>' for date in planned_leave]
                    planned_str = ''.join(badges)

                # Create badge HTML for GCC holidays
                gcc_str = '-'
                if gcc_holiday:
                    badges = [
                        f'<span class="leave-badge leave-holiday">{date}</span>' for date in gcc_holiday]
                    gcc_str = ''.join(badges)

                # Highlight rows with any leave
                row_class = ' class="on-leave"' if (
                    planned_leave or gcc_holiday) else ''

                html += f"""                        <tr{row_class}>
                            <td>{employee.emp_id}</td>
                            <td>{employee.name}</td>
                            <td>{planned_str}</td>
                            <td>{gcc_str}</td>
                        </tr>
"""

            html += """                    </tbody>
                </table>
            </div>
"""

        html += """
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>🤖 This report was automatically generated by Sprint Capacity Automation System</p>
            <p style="margin-top: 8px; color: #94a3b8;">For questions or issues, please contact the Scrum Master</p>
        </div>
    </div>
</body>
</html>"""

        return html

    def save_report(self, content: str, filename: str, format_type: str = "txt"):
        """Save report to file in reports folder"""
        try:
            # Create reports folder if it doesn't exist
            reports_folder = "reports"
            if not os.path.exists(reports_folder):
                os.makedirs(reports_folder)
                logger.info(f"Created reports folder: {reports_folder}")

            # Save file in reports folder
            filepath = os.path.join(reports_folder, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Report saved to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            raise


class EmailSender:
    """Handles email automation for sending reports"""

    def __init__(self, calculator: SprintCapacityCalculator):
        self.calculator = calculator
        self.email_config = calculator.config.get('email_settings', {})

    def send_capacity_report(self, text_report: str, html_report: str,
                             sprint_capacities: List[SprintCapacity], email_template: str = "") -> bool:
        """Send capacity report via email with email template as body and HTML report as attachment"""
        try:
            # Validate email configuration
            # Note: password is optional for DONOTREPLY accounts
            if not all([
                self.email_config.get('sender_email'),
                self.email_config.get('scrum_master_email')
            ]):
                logger.warning(
                    "Email configuration incomplete. Skipping email send.")
                return False

            # Build recipient list: scrum master + additional recipients
            recipients = [self.email_config['scrum_master_email']]

            # Get additional recipients from environment variable
            additional_recipients_env = os.getenv('ADDITIONAL_RECIPIENTS', '')
            if additional_recipients_env:
                # Split by comma and strip whitespace
                additional_recipients = [
                    email.strip() for email in additional_recipients_env.split(',') if email.strip()]
                recipients.extend(additional_recipients)
                logger.info(
                    f"Additional recipients from environment: {additional_recipients}")

            # Remove duplicates while preserving order
            recipients = list(dict.fromkeys(recipients))

            logger.info(f"Email will be sent to: {', '.join(recipients)}")

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Sprint Capacity Report - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = self.email_config['sender_email']
            msg['To'] = ', '.join(recipients)

            # Use email template as the body if available, otherwise use HTML report
            if email_template:
                # Email template is already HTML, so use it as the main body
                html_part = MIMEText(email_template, 'html')
                msg.attach(html_part)
            else:
                # Fallback to HTML report if no template
                html_part = MIMEText(html_report, 'html')
                msg.attach(html_part)

            # Add HTML report as attachment
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(html_report.encode('utf-8'))
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="sprint_capacity_report_{datetime.now().strftime("%Y%m%d")}.html"'
            )
            msg.attach(attachment)

            # Send email
            smtp_port = self.email_config.get('smtp_port', 587)
            server = smtplib.SMTP(
                self.email_config.get('smtp_server', 'smtp.gmail.com'),
                smtp_port
            )

            # Only use STARTTLS for ports other than 25 (port 25 is plain SMTP)
            if smtp_port != 25:
                server.starttls()

            # Only login if password is provided (DONOTREPLY accounts don't need authentication)
            if self.email_config.get('sender_password'):
                server.login(
                    self.email_config['sender_email'], self.email_config['sender_password'])

            text = msg.as_string()
            server.sendmail(
                self.email_config['sender_email'],
                recipients,
                text
            )
            server.quit()

            logger.info(
                f"Email sent successfully to {', '.join(recipients)}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False


class SprintCapacityApp:
    """Main application class that orchestrates the entire process"""

    def __init__(self, config_file: str = "config.json"):
        """Initialize the application"""
        self.calculator = SprintCapacityCalculator(config_file)
        self.parser = ExcelDataParser(self.calculator)
        self.sprint_manager = SprintManager(self.calculator)
        self.report_generator = ReportGenerator(self.calculator)
        self.email_sender = EmailSender(self.calculator)

    def run_capacity_analysis(self) -> bool:
        """Run the complete capacity analysis process"""
        try:
            logger.info("Starting sprint capacity analysis...")

            # Step 1: Parse Excel data
            excel_file = self.calculator.config['excel_file_path']
            if not os.path.exists(excel_file):
                logger.error(f"Excel file not found: {excel_file}")
                return False

            employees, leave_entries = self.parser.parse_excel_file(excel_file)
            self.calculator.employees = employees
            self.calculator.leave_entries = leave_entries

            if not employees:
                logger.warning("No employees found in Excel file")
                return False

            # Step 1.5: Parse on-call schedules
            oncall_schedules = self.parser.parse_oncall_schedules(excel_file)
            self.calculator.oncall_schedules = oncall_schedules

            # Step 2: Calculate sprint capacities
            sprints = self.sprint_manager.get_current_and_upcoming_sprints(
                oncall_schedules)
            sprint_capacities = []

            for sprint in sprints:
                capacity = self.sprint_manager.calculate_sprint_capacity(
                    sprint)
                sprint_capacities.append(capacity)

            # Step 3: Generate reports
            text_report = self.report_generator.generate_text_report(
                sprint_capacities)
            html_report = self.report_generator.generate_html_report(
                sprint_capacities)

            # Step 4: Save reports to files in reports folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            text_filename = f"sprint_capacity_report_{timestamp}.txt"
            html_filename = f"sprint_capacity_report_{timestamp}.html"
            email_template_filename = f"email_template_filled_{timestamp}.html"

            text_filepath = self.report_generator.save_report(
                text_report, text_filename, "txt")
            html_filepath = self.report_generator.save_report(
                html_report, html_filename, "html")

            # Step 4.5: Generate and save email template (Sprint 2 & 3 only)
            email_template = self.report_generator.generate_email_template(
                sprint_capacities)
            email_template_filepath = None
            if email_template:
                email_template_filepath = self.report_generator.save_report(
                    email_template, email_template_filename, "html")
                logger.info(
                    f"✅ Email template created: {email_template_filepath}")

            # Step 5: Send email (if configured)
            email_sent = self.email_sender.send_capacity_report(
                text_report, html_report, sprint_capacities, email_template)

            # Step 6: Display summary
            self.display_summary(
                sprint_capacities, text_filepath, html_filepath, email_sent, email_template_filepath)

            logger.info("Sprint capacity analysis completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error during capacity analysis: {e}")
            return False

    def display_summary(self, sprint_capacities: List[SprintCapacity],
                        text_file: str, html_file: str, email_sent: bool,
                        email_template_file: str = None):
        """Display analysis summary"""
        print("\n" + "="*60)
        print("SPRINT CAPACITY ANALYSIS SUMMARY")
        print("="*60)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(
            f"Team Members Analyzed: {sprint_capacities[0].total_team_members if sprint_capacities else 0}")
        print(f"Sprints Analyzed: {len(sprint_capacities)}")
        print(f"Reports Generated: {text_file}, {html_file}")
        if email_template_file:
            print(f"📧 Email Template: {email_template_file}")
        print(f"Email Sent: {'Yes' if email_sent else 'No'}")
        print()

        for capacity in sprint_capacities:
            status = "🟢" if capacity.capacity_percentage >= 80 else "🟡" if capacity.capacity_percentage >= 60 else "🔴"
            print(f"{status} Sprint {capacity.sprint.number}: {capacity.capacity_percentage:.1f}% capacity "
                  f"(Members: {capacity.total_team_members})")

        print("="*60)

        if email_template_file:
            print("\n📧 Email Template Ready!")
            print(f"   Open: {email_template_file}")
            print("   This template contains the next 2 upcoming sprints data")
            print("   Copy and paste into your email client")
            print("="*60)

    def setup_configuration(self):
        """Interactive setup for configuration"""
        print("Sprint Capacity App Configuration Setup")
        print("="*40)

        config = self.calculator.config.copy()

        # Sprint configuration
        print("\n1. Sprint Configuration:")
        start_date = input(
            f"Sprint start date (YYYY-MM-DD) [{config['sprint_start_date']}]: ").strip()
        if start_date:
            config['sprint_start_date'] = start_date

        duration = input(
            f"Sprint duration in days [{config['sprint_duration_days']}]: ").strip()
        if duration and duration.isdigit():
            config['sprint_duration_days'] = int(duration)

        # File configuration
        print("\n2. File Configuration:")
        excel_file = input(
            f"Excel file path [{config['excel_file_path']}]: ").strip()
        if excel_file:
            config['excel_file_path'] = excel_file

        # Email configuration
        print("\n3. Email Configuration (optional):")
        sender_email = input(
            f"Sender email [{config['email_settings']['sender_email']}]: ").strip()
        if sender_email:
            config['email_settings']['sender_email'] = sender_email

        sender_password = input(
            "Sender email password (will be hidden): ").strip()
        if sender_password:
            config['email_settings']['sender_password'] = sender_password

        scrum_master_email = input(
            f"Scrum master email [{config['email_settings']['scrum_master_email']}]: ").strip()
        if scrum_master_email:
            config['email_settings']['scrum_master_email'] = scrum_master_email

        # Save configuration
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)

        print("\nConfiguration saved successfully!")
        self.calculator.config = config


def main():
    """Main entry point for the application"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Sprint Capacity Automation Tool")
    parser.add_argument('--config', default='config.json',
                        help='Configuration file path')
    parser.add_argument('--setup', action='store_true',
                        help='Run configuration setup')
    parser.add_argument('--analyze', action='store_true',
                        help='Run capacity analysis')
    parser.add_argument('--excel-file', help='Override Excel file path')
    parser.add_argument('--output-dir', default='.',
                        help='Output directory for reports')

    args = parser.parse_args()

    # Change to output directory
    if args.output_dir != '.':
        os.makedirs(args.output_dir, exist_ok=True)
        os.chdir(args.output_dir)

    # Initialize application
    app = SprintCapacityApp(args.config)

    # Override Excel file if specified
    if args.excel_file:
        app.calculator.config['excel_file_path'] = args.excel_file

    # Run setup if requested
    if args.setup:
        app.setup_configuration()
        return

    # Run analysis if requested or by default
    if args.analyze or not any([args.setup]):
        success = app.run_capacity_analysis()
        if not success:
            print("❌ Capacity analysis failed. Check logs for details.")
            return 1
        else:
            print("✅ Capacity analysis completed successfully!")
            return 0


if __name__ == "__main__":
    exit(main())
