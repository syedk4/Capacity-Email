@echo off
REM ============================================================================
REM Sprint Capacity Analysis - Automated Task Scheduler Wrapper
REM ============================================================================
REM This script is called by Windows Task Scheduler to run the sprint capacity
REM analysis and generate email reports automatically.
REM
REM Usage: Double-click this file or call from Task Scheduler
REM ============================================================================

REM Change to project directory
cd /d "c:\Users\slatheef\Documents\Capacity Email 19012026\Capacity Email"

REM Log start time
echo. >> sprint_capacity.log
echo ============================================================================ >> sprint_capacity.log
echo Task started at %date% %time% >> sprint_capacity.log
echo ============================================================================ >> sprint_capacity.log

REM Run the Python script with analysis flag
REM This will:
REM   1. Load the Excel file
REM   2. Calculate sprint capacity
REM   3. Generate reports (text, HTML, email template)
REM   4. Send email (if SMTP is configured)
py sprint_capacity_app.py --analyze

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

REM Log completion
if %EXIT_CODE% equ 0 (
    echo Task completed successfully at %date% %time% >> sprint_capacity.log
    echo Exit code: %EXIT_CODE% >> sprint_capacity.log
) else (
    echo Task FAILED at %date% %time% >> sprint_capacity.log
    echo Exit code: %EXIT_CODE% >> sprint_capacity.log
)

echo ============================================================================ >> sprint_capacity.log
echo. >> sprint_capacity.log

REM Exit with the same code as Python script
exit /b %EXIT_CODE%

