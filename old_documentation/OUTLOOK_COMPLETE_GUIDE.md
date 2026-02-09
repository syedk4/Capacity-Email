# 📧 Outlook Email Setup - Complete Guide

**Status:** ✅ **QUICK FIX - 10 MINUTES**  
**Email Provider:** Microsoft Outlook  
**Difficulty:** Easy

---

## 🎯 What You'll Do

Configure your Outlook email to send Sprint Capacity Reports automatically.

---

## 📋 Prerequisites

Before starting, you need:
- ✅ Outlook email address (your.email@outlook.com)
- ✅ Outlook password
- ✅ Scrum master's email address

---

## 🚀 Step 1: Get Your Outlook Credentials (2 minutes)

### **Option A: If You DON'T Have 2-Factor Authentication**

Simply use your regular Outlook password.

### **Option B: If You DO Have 2-Factor Authentication**

1. Go to: **https://account.microsoft.com/security**
2. Sign in with your Outlook email
3. Click **"App passwords"** (left sidebar)
4. Select **"Mail"** from first dropdown
5. Select **"Windows"** from second dropdown
6. Click **"Create"**
7. **Copy the 16-character password** (format: `xxxx xxxx xxxx xxxx`)
8. Save it somewhere safe

---

## 🖥️ Step 2: Set Windows Environment Variables (5 minutes)

### **Part A: Open Environment Variables**

1. **Press Windows Key + X** (hold Windows, press X)
2. Click **"System"**
3. Click **"Advanced system settings"** (left side)
4. Click **"Environment Variables"** button (bottom right)

### **Part B: Add 5 Variables**

In the Environment Variables dialog, click **"New"** and add these:

**Variable 1:**
```
Name:  GMAIL_SMTP_SERVER
Value: smtp-mail.outlook.com
```

**Variable 2:**
```
Name:  GMAIL_SMTP_PORT
Value: 587
```

**Variable 3:**
```
Name:  GMAIL_SENDER_EMAIL
Value: your.email@outlook.com
```

**Variable 4:**
```
Name:  GMAIL_SENDER_PASSWORD
Value: [Your password or app password from Step 1]
```

**Variable 5:**
```
Name:  SCRUM_MASTER_EMAIL
Value: scrum.master@company.com
```

### **Part C: Save and Close**

1. Click "OK" on each variable dialog
2. Click "OK" on Environment Variables dialog
3. Click "OK" on System Properties dialog

---

## ✅ Step 3: Test Email Sending (3 minutes)

### **Part A: Restart Terminal**

1. **Close PowerShell/Terminal** (if open)
2. **Open PowerShell/Terminal** again
   - Press Windows Key + R
   - Type: `powershell`
   - Press Enter

### **Part B: Run Application**

Type this command:
```powershell
python sprint_capacity_app.py --analyze
```

Press Enter and wait for completion.

### **Part C: Check Success**

Look for this message:
```
✅ Email sent successfully to scrum.master@company.com
```

**If you see this, email is working!** ✅

---

## 📊 Outlook SMTP Configuration

| Setting | Value |
|---------|-------|
| SMTP Server | smtp-mail.outlook.com |
| SMTP Port | 587 |
| Encryption | TLS |
| Authentication | Required |

---

## 🔐 Important Notes

- **App Password:** Use if 2FA is enabled (more secure)
- **Regular Password:** Use if 2FA is NOT enabled
- **Never share:** Keep your password confidential
- **Environment Variables:** More secure than storing in config file

---

## 🆘 Troubleshooting

### **Error: "Invalid login credentials"**
- Check email address is correct
- Check password is correct
- If 2FA enabled, use app password (not regular password)

### **Error: "Connection refused"**
- Verify SMTP server: smtp-mail.outlook.com
- Verify SMTP port: 587
- Check internet connection

### **Error: "Recipient rejected"**
- Check scrum master email is correct
- Verify email address exists

### **Error: "TLS error"**
- Ensure port is 587 (not 25 or 465)
- Check firewall settings

### **Environment variables not working**
- Close and reopen terminal
- Check variable names are EXACTLY as shown
- Verify no extra spaces in values

---

## 📧 Expected Result

After successful setup:

**Command:**
```powershell
python sprint_capacity_app.py --analyze
```

**Output:**
```
✅ Email sent successfully to scrum.master@company.com
```

**Email Received:**
- Subject: Sprint Capacity Report - 2026-01-14
- Body: Text and HTML reports
- Attachment: Text report file

---

## ✅ Verification Checklist

- [ ] Got Outlook email address
- [ ] Got Outlook password or app password
- [ ] Opened Environment Variables dialog
- [ ] Added GMAIL_SMTP_SERVER = smtp-mail.outlook.com
- [ ] Added GMAIL_SMTP_PORT = 587
- [ ] Added GMAIL_SENDER_EMAIL = your.email@outlook.com
- [ ] Added GMAIL_SENDER_PASSWORD = [your password]
- [ ] Added SCRUM_MASTER_EMAIL = [recipient email]
- [ ] Closed all dialogs
- [ ] Closed and reopened terminal
- [ ] Ran application
- [ ] Saw success message
- [ ] Email received in inbox

---

## 📚 Quick Reference Documents

| Document | Purpose |
|----------|---------|
| OUTLOOK_QUICK_REFERENCE.md | 1-page quick reference |
| OUTLOOK_STEP_BY_STEP.md | Detailed step-by-step |
| OUTLOOK_EMAIL_SETUP.md | Quick setup guide |

---

## 🎯 Timeline

- **Step 1:** 2 minutes
- **Step 2:** 5 minutes
- **Step 3:** 3 minutes
- **Total:** 10 minutes

---

## 💡 Tips

✅ Save your app password somewhere safe  
✅ Test immediately after setup  
✅ Check spam folder if email doesn't arrive  
✅ Keep environment variables for future use  

---

**Status:** ✅ **READY TO SETUP**

You're just 10 minutes away from having email working! 🚀

