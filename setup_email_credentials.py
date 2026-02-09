#!/usr/bin/env python3
"""
Email Credentials Setup Script

This script helps you securely set up email credentials as environment variables.
Run this once to configure your email settings.
"""

import os
import sys
import getpass
from pathlib import Path


def setup_email_credentials():
    """Interactive setup for email credentials"""
    print("=" * 70)
    print("EMAIL CREDENTIALS SECURE SETUP")
    print("=" * 70)
    print()
    print("This script will help you set up secure email credentials.")
    print("Your credentials will be stored as environment variables.")
    print()

    # Check if credentials are already set
    existing_email = os.getenv('GMAIL_SENDER_EMAIL')
    if existing_email:
        print(f"✓ Existing email found: {existing_email}")
        update = input("Update existing credentials? (y/n): ").lower()
        if update != 'y':
            print("Keeping existing credentials.")
            return

    print()
    print("STEP 1: Gmail Information")
    print("-" * 70)

    # Get email address
    while True:
        sender_email = input("Enter your Gmail address: ").strip()
        if '@gmail.com' in sender_email:
            break
        print("Error: Please enter a valid Gmail address (e.g., user@gmail.com)")

    print()
    print("STEP 2: Gmail App Password")
    print("-" * 70)
    print("For Gmail security, you must use an 'App Password', not your regular password.")
    print()
    print("To get your App Password:")
    print("1. Go to https://myaccount.google.com/security")
    print("2. Enable '2-Step Verification' (if not already enabled)")
    print("3. Go to 'App passwords'")
    print("4. Select 'Mail' and 'Windows Computer'")
    print("5. Copy the 16-character password")
    print()

    while True:
        sender_password = getpass.getpass(
            "Enter your 16-character App Password: ").strip()
        if len(sender_password) >= 14:  # App passwords are typically 16 chars
            break
        print("Error: App password should be at least 14 characters long")

    print()
    print("STEP 3: SMTP Configuration (Usually not needed for Gmail)")
    print("-" * 70)
    smtp_server = input(
        "Enter SMTP server [smtp.gmail.com]: ").strip() or "smtp.gmail.com"
    smtp_port = input("Enter SMTP port [587]: ").strip() or "587"

    print()
    print("STEP 4: Scrum Master Email")
    print("-" * 70)
    scrum_master_email = input("Enter Scrum Master email address: ").strip()

    print()
    print("=" * 70)
    print("CONFIRMATION")
    print("=" * 70)
    print(f"Gmail Address:        {sender_email}")
    print(f"SMTP Server:          {smtp_server}")
    print(f"SMTP Port:            {smtp_port}")
    print(f"Scrum Master Email:   {scrum_master_email}")
    print(f"App Password:         {'*' * len(sender_password)}")
    print()

    confirm = input("Save these credentials? (y/n): ").lower()
    if confirm != 'y':
        print("Setup cancelled.")
        return False

    # Set environment variables
    print()
    print("Setting environment variables...")

    try:
        # Use Windows registry to set environment variables permanently
        import subprocess

        setx_commands = [
            f'setx GMAIL_SENDER_EMAIL "{sender_email}"',
            f'setx GMAIL_SENDER_PASSWORD "{sender_password}"',
            f'setx GMAIL_SMTP_SERVER "{smtp_server}"',
            f'setx GMAIL_SMTP_PORT "{smtp_port}"',
            f'setx SCRUM_MASTER_EMAIL "{scrum_master_email}"'
        ]

        for cmd in setx_commands:
            subprocess.run(cmd, shell=True, capture_output=True)

        print("✓ Environment variables set successfully!")
        print()
        print("IMPORTANT: You must RESTART your terminal/IDE for changes to take effect.")
        print()

        return True

    except Exception as e:
        print(f"✗ Error setting environment variables: {e}")
        print()
        print("Alternative: Set them manually using Control Panel:")
        print("1. Open Control Panel → System → Advanced system settings")
        print("2. Click 'Environment Variables'")
        print("3. Under 'User variables', click 'New' and add:")
        print(f"   GMAIL_SENDER_EMAIL = {sender_email}")
        print(f"   GMAIL_SENDER_PASSWORD = {sender_password}")
        print(f"   GMAIL_SMTP_SERVER = {smtp_server}")
        print(f"   GMAIL_SMTP_PORT = {smtp_port}")
        print(f"   SCRUM_MASTER_EMAIL = {scrum_master_email}")
        print()
        return False


def verify_credentials():
    """Verify that credentials are properly set"""
    print()
    print("=" * 70)
    print("VERIFYING CREDENTIALS")
    print("=" * 70)

    required_vars = [
        'GMAIL_SENDER_EMAIL',
        'GMAIL_SENDER_PASSWORD',
        'SCRUM_MASTER_EMAIL'
    ]

    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            display_value = value if var == 'GMAIL_SENDER_EMAIL' or var == 'SCRUM_MASTER_EMAIL' else '*' * \
                len(value)
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: NOT SET")
            all_set = False

    print()
    if all_set:
        print("✓ All credentials are properly set!")
        print("You can now use the Sprint Capacity application with email functionality.")
    else:
        print("✗ Some credentials are missing. Please run setup again.")

    return all_set


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--verify':
            verify_credentials()
            return
        elif sys.argv[1] == '--clear':
            print("To clear credentials, remove the environment variables manually:")
            print("1. Open Control Panel → System → Advanced system settings")
            print("2. Click 'Environment Variables'")
            print("3. Delete: GMAIL_SENDER_EMAIL, GMAIL_SENDER_PASSWORD, etc.")
            return

    # Run interactive setup
    if setup_email_credentials():
        print()
        print("Setup complete! Please restart your terminal/IDE and run:")
        print("  py setup_email_credentials.py --verify")
        print()
        print("Then test by running:")
        print("  py sprint_capacity_app.py --analyze")


if __name__ == '__main__':
    main()
