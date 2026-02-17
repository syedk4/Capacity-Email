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
cd /d "c:\Users\slatheef\Documents\Capacity-Email"

REM Create logs folder if it doesn't exist
if not exist "%~dp0logs" mkdir "%~dp0logs"

REM Define log file path within logs folder
set LOG_FILE="%~dp0logs\sprint_capacity.log"

REM Log start time
echo. >> %LOG_FILE%
echo ============================================================================ >> %LOG_FILE%
echo Task started at %date% %time% >> %LOG_FILE%
echo ============================================================================ >> %LOG_FILE%

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
    echo Task completed successfully at %date% %time% >> %LOG_FILE%
    echo Exit code: %EXIT_CODE% >> %LOG_FILE%
) else (
    echo Task FAILED at %date% %time% >> %LOG_FILE%
    echo Exit code: %EXIT_CODE% >> %LOG_FILE%
)

echo ============================================================================ >> %LOG_FILE%
echo. >> %LOG_FILE%

REM Exit with the same code as Python script
exit /b %EXIT_CODE%

