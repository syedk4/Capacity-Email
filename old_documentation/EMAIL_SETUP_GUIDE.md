# Secure Email Configuration Guide

## Overview
The application now supports secure email credential management using **Windows Environment Variables**. This prevents credentials from being stored in plain text in `config.json`.

## How It Works

1. **Environment Variables** (Most Secure) - Checked first
2. **config.json** (Fallback) - Used if environment variables not set

Environment variables take precedence, so you can keep empty values in config.json.

## Step 1: Get Your Email Credentials

### For Gmail Users:
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Google will generate a **16-character app password**
4. Copy this password (you'll need it in Step 2)

### For Other Email Providers:
- Use your regular email password
- Or contact your email provider for app-specific passwords

## Step 2: Set Windows Environment Variables

### Method 1: Using GUI (Recommended)

1. Press **Windows Key + X**
2. Select **System**
3. Click **Advanced system settings** (on the left)
4. Click **Environment Variables** button
5. Under "User variables", click **New**
6. Add these three variables:

**Variable 1:**
- Variable name: `SMTP_SENDER_EMAIL`
- Variable value: `your-email@gmail.com`
- Click OK

**Variable 2:**
- Variable name: `SMTP_SENDER_PASSWORD`
- Variable value: `your-16-char-app-password` (from Step 1)
- Click OK

**Variable 3:**
- Variable name: `SMTP_RECIPIENT_EMAIL`
- Variable value: `scrum-master@example.com`
- Click OK

**Variable 4 (Optional - for additional recipients):**
- Variable name: `ADDITIONAL_RECIPIENTS`
- Variable value: `email1@example.com, email2@example.com, email3@example.com`
- Click OK
- Note: Separate multiple emails with commas

6. Click **OK** to close Environment Variables window
7. **Restart your terminal/PowerShell** for changes to take effect

### Method 2: Using PowerShell (Advanced)

```powershell
[Environment]::SetEnvironmentVariable("SMTP_SENDER_EMAIL", "your-email@gmail.com", "User")
[Environment]::SetEnvironmentVariable("SMTP_SENDER_PASSWORD", "your-16-char-app-password", "User")
[Environment]::SetEnvironmentVariable("SMTP_RECIPIENT_EMAIL", "scrum-master@example.com", "User")
[Environment]::SetEnvironmentVariable("ADDITIONAL_RECIPIENTS", "email1@example.com, email2@example.com", "User")
```

Then restart PowerShell.

**Note:** The `ADDITIONAL_RECIPIENTS` variable is optional. Separate multiple emails with commas.

## Step 3: Verify Environment Variables Are Set

Run this command in PowerShell:

```powershell
$env:SMTP_SENDER_EMAIL
$env:SMTP_SENDER_PASSWORD
$env:SMTP_RECIPIENT_EMAIL
$env:ADDITIONAL_RECIPIENTS
```

You should see your values displayed. The `ADDITIONAL_RECIPIENTS` line may be empty if you didn't set it (which is fine - it's optional).

## Step 4: Update sprint_capacity_app.py

Replace the EmailSender class initialization with the new secure version.

See `IMPLEMENTATION_GUIDE.md` for code changes.

## Security Best Practices

✅ **DO:**
- Use environment variables for credentials
- Use app passwords for Gmail (not your main password)
- Keep config.json empty for email credentials
- Add config.json to .gitignore

❌ **DON'T:**
- Store passwords in config.json
- Commit config.json with credentials to Git
- Share your app password
- Use your main Gmail password

## Troubleshooting

### Email not sending?
1. Check environment variables are set: `$env:SMTP_SENDER_EMAIL`
2. Verify app password is correct (16 characters)
3. Check logs for error messages
4. Ensure recipient email is valid

### "Email configuration incomplete" warning?
- One or more environment variables are not set
- Check Step 2 and Step 3 above
- Restart terminal after setting variables

### Still having issues?
- Check that you're using an app password (for Gmail)
- Verify email addresses are correct
- Check firewall/antivirus isn't blocking SMTP

