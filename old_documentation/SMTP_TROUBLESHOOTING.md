# 📧 SMTP Connection Troubleshooting Guide

**Issue:** Email not sending due to SMTP connection failure  
**Error:** `No connection could be made because the target machine actively refused it`

---

## Quick Diagnosis

### Step 1: Check if You're on VPN
Most corporate SMTP servers require VPN access.

```powershell
# Check if you can reach the SMTP server
ping smtp.ashleyfurniture.com
```

**Expected:** If not on VPN, ping will fail  
**Action:** Connect to Ashley Furniture VPN and try again

---

### Step 2: Verify SMTP Server Settings

Current settings in `.env`:
```
GMAIL_SMTP_SERVER=smtp.ashleyfurniture.com
GMAIL_SMTP_PORT=587
```

**Questions to verify:**
- ✓ Is `smtp.ashleyfurniture.com` the correct SMTP server?
- ✓ Is `587` the correct port?
- ✓ Does your email account work in Outlook?

---

### Step 3: Test SMTP Connection

You can test if the SMTP server is reachable:

```powershell
# Test port 587 connectivity
Test-NetConnection -ComputerName smtp.ashleyfurniture.com -Port 587 -Verbose
```

**Expected output if working:**
```
TcpTestSucceeded : True
```

**If False:** You may need VPN or firewall adjustment

---

## Solutions by Scenario

### Scenario 1: Not on VPN
**Symptom:** Can't reach smtp.ashleyfurniture.com  
**Solution:**
1. Connect to Ashley Furniture VPN
2. Run: `py sprint_capacity_app.py --analyze` again
3. Email should send

### Scenario 2: SMTP Server Address Wrong
**Symptom:** Connection refused on correct port  
**Solution:**
1. Check with IT what the correct SMTP server is
2. Update `.env` with correct address:
   ```
   GMAIL_SMTP_SERVER=correct-smtp-server.ashleyfurniture.com
   ```
3. Run application again

### Scenario 3: Port Wrong
**Symptom:** Connection timeout  
**Common ports:**
- `25` - SMTP (plain text, old)
- `587` - SMTP TLS (recommended, current)
- `465` - SMTP SSL (alternative)

**Solution:**
1. Ask IT which port to use
2. Update `.env`:
   ```
   GMAIL_SMTP_PORT=25    # or 465
   ```
3. Restart and test

### Scenario 4: Firewall Blocking
**Symptom:** Connection refused even with VPN  
**Solution:**
1. Contact IT to allow outbound SMTP
2. Verify firewall exceptions for port 587

---

## Workaround: Manual Email Send

Even if SMTP fails, you can still send emails manually!

### Option A: From HTML Template

1. **Find the email template:**
   - Check: `reports/email_template_filled_*.html` (latest file)
   - Example: `reports/email_template_filled_20260114_143805.html`

2. **Open in browser:**
   - Double-click the HTML file
   - It opens in your default browser

3. **Copy content:**
   - Select all (Ctrl+A)
   - Copy (Ctrl+C)

4. **Paste in Outlook:**
   - New email
   - Click "Format" → "Edit in HTML" (or equivalent)
   - Paste the content

5. **Send:**
   - Add recipients
   - Send!

### Option B: Direct HTML Send

```powershell
# Using PowerShell to send email from template
$TemplateFile = "reports/email_template_filled_20260114_143805.html"
$Content = Get-Content $TemplateFile -Raw

$EmailParams = @{
    To = "slatheef@ashleyfurniture.com"
    From = "slatheef@ashleyfurniture.com"
    Subject = "Sprint Capacity Report - Jan 14, 2026"
    Body = $Content
    BodyAsHtml = $True
    SmtpServer = "smtp.ashleyfurniture.com"
    Port = 587
    UseSsl = $True
    Credential = (Get-Credential)
}

Send-MailMessage @EmailParams
```

---

## Testing Checklist

- [ ] VPN connected?
- [ ] Can ping smtp.ashleyfurniture.com?
- [ ] Correct SMTP server address?
- [ ] Correct port number?
- [ ] Email works in Outlook?
- [ ] Credentials correct in .env?

---

## When to Contact IT

Contact Ashley Furniture IT if:
- [ ] You cannot reach smtp.ashleyfurniture.com on port 587
- [ ] You need firewall exceptions
- [ ] You need different SMTP settings
- [ ] Your email account isn't working for SMTP

**Provide them:**
- Current error: `No connection could be made because the target machine actively refused it`
- Your SMTP settings: `smtp.ashleyfurniture.com:587`
- Your email: `slatheef@ashleyfurniture.com`

---

## Quick Test Script

Save as `test_smtp.py`:

```python
import smtplib
import sys

try:
    print("Testing SMTP connection...")
    server = smtplib.SMTP("smtp.ashleyfurniture.com", 587)
    server.starttls()
    print("✅ Connection successful!")
    print("✅ TLS enabled!")
    server.quit()
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)
```

**Run:**
```powershell
py test_smtp.py
```

---

## Email Still Not Sending?

If after trying these steps email still won't send:

1. ✅ Use the HTML template workaround (manual send)
2. ✅ Contact IT with SMTP test results
3. ✅ Check if Outlook works (verify credentials)
4. ✅ Try a different email address for testing

---

**Status:** Following these steps should resolve the SMTP connection issue.  
**Next:** Once SMTP works, email will send automatically every time you run the application.
