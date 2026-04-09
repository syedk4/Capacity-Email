# 🚀 SharePoint REST API Implementation Guide

## 📐 1. Architecture Overview

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    Server (Scheduled Task)                   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  sprint_capacity_app.py                            │    │
│  │                                                     │    │
│  │  1. Read SharePoint credentials from .env          │    │
│  │  2. Authenticate with Microsoft Graph/SharePoint   │    │
│  │  3. Download Excel file via REST API               │    │
│  │  4. Save to temporary local file                   │    │
│  │  5. Process Excel file (existing logic)            │    │
│  │  6. Send email report                              │    │
│  │  7. Clean up temporary file                        │    │
│  └────────────────────────────────────────────────────┘    │
│                           ↓                                  │
│                    Authentication                            │
│                           ↓                                  │
└───────────────────────────┼──────────────────────────────────┘
                            ↓
                    ┌───────────────┐
                    │   Microsoft   │
                    │   Identity    │
                    │   Platform    │
                    │  (Azure AD)   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │  SharePoint   │
                    │    Online     │
                    │               │
                    │  Excel File   │
                    └───────────────┘
```

### Authentication Flow

1. **Client Credentials Flow** (OAuth 2.0)
   - Application authenticates using Client ID + Client Secret
   - No user interaction required (daemon/service app)
   - Receives access token from Azure AD

2. **API Access**
   - Access token used to call Microsoft Graph API
   - Downloads file content from SharePoint
   - Token automatically refreshed when expired

---

## 🔑 2. Prerequisites

### A. Azure AD App Registration (Required)

You need to register an application in Azure AD to get API access.

**Required Information:**
- ✅ **Tenant ID** (Your organization's Azure AD tenant)
- ✅ **Client ID** (Application ID)
- ✅ **Client Secret** (Application password)

**Required Permissions:**
- `Sites.Read.All` - Read items in all site collections
- `Files.Read.All` - Read files in all site collections

### B. SharePoint Site Information

- ✅ **Site URL**: Your SharePoint site URL
- ✅ **File Path**: Relative path to the Excel file in SharePoint

### C. Python Packages

New dependencies (already added to `requirements.txt`):
- `msal>=1.20.0` - Microsoft Authentication Library
- `requests>=2.28.0` - HTTP library for API calls

---

## 🛠️ 3. Implementation Steps

### STEP 1: Azure AD App Registration

#### A. Access Azure Portal

1. Go to: https://portal.azure.com
2. Sign in with your Ashley Furniture account

#### B. Register Application

1. Navigate to: **Azure Active Directory** → **App registrations** → **New registration**
2. Fill in:
   - **Name**: `Sprint-Capacity-SharePoint-Access`
   - **Supported account types**: `Accounts in this organizational directory only`
   - **Redirect URI**: Leave blank
3. Click **Register**

#### C. Note Application IDs

After registration, copy these values:
- **Application (client) ID**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Directory (tenant) ID**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Save these values!**

#### D. Create Client Secret

1. Go to: **Certificates & secrets** → **New client secret**
2. Description: `SharePoint Access Secret`
3. Expires: Choose `24 months`
4. Click **Add**
5. **IMPORTANT**: Copy the **Value** immediately!

**Save this secret value!**

#### E. Grant API Permissions

1. Go to: **API permissions** → **Add a permission**
2. Choose: **Microsoft Graph**
3. Choose: **Application permissions** (not Delegated)
4. Add these permissions:
   - `Sites.Read.All`
   - `Files.Read.All`
5. Click **Add permissions**
6. **IMPORTANT**: Click **Grant admin consent for [Your Organization]**
7. Wait for green checkmarks

---

### STEP 2: Find SharePoint Site Information

#### A. Find SharePoint Site URL

1. On your local machine, open File Explorer
2. Navigate to the OneDrive folder with your Excel file
3. Right-click the folder → **View online**
4. Copy the URL from browser (e.g., `https://ashleyfurniture.sharepoint.com/sites/IT-Finance-IndiaFinanceTeam`)

#### B. Find File Path

1. In SharePoint, navigate to your Excel file
2. Right-click → **Details**
3. Note the path structure (e.g., `/Shared Documents/Daily Updates/filename.xlsx`)

---

### STEP 3: Install Python Packages

On the **server**, run:

```powershell
cd C:\Users\slatheef\Documents\Capacity-Email
python -m pip install -r requirements.txt
```

This will install:
- `msal` - Microsoft Authentication Library
- `requests` - HTTP library
- All existing dependencies

---

### STEP 4: Configure Environment Variables

1. On the **server**, navigate to: `C:\Users\slatheef\Documents\Capacity-Email\`
2. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```
3. Edit `.env` file and fill in your values:

```env
# Azure AD Configuration
AZURE_TENANT_ID=your-tenant-id-from-azure-portal
AZURE_CLIENT_ID=your-client-id-from-app-registration
AZURE_CLIENT_SECRET=your-client-secret-from-app-registration

# SharePoint Configuration
SHAREPOINT_SITE_URL=https://ashleyfurniture.sharepoint.com/sites/YourSiteName
SHAREPOINT_FILE_PATH=/Shared Documents/Your Folder/2026- India Finance team Daily work status.xlsx

# Email Configuration (existing)
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SENDER_EMAIL=DONOTREPLY@ashleyfurniture.com
SENDER_PASSWORD=your-password
SCRUM_MASTER_EMAIL=slatheef@ashleyfurniture.com
```

---

### STEP 5: Update config.json

On the **server**, edit `config.json` and set:

```json
{
  "use_sharepoint": true,
  ...
}
```

This enables SharePoint mode instead of local file access.

---

## 📝 4. Code Changes Required

The following files have been created/modified:

### New Files Created:
1. ✅ `sharepoint_client.py` - SharePoint API client module
2. ✅ `.env.example` - Template for environment variables
3. ✅ `docs/SHAREPOINT_API_IMPLEMENTATION_GUIDE.md` - This guide

### Files Modified:
1. ✅ `requirements.txt` - Added `msal` and `requests`
2. ✅ `config.json` - Added `use_sharepoint` flag

### Files To Be Modified (Next):
1. ⏳ `sprint_capacity_app.py` - Integration with SharePoint client

---

## 🔒 5. Security Considerations

### Credential Storage

- ✅ **Never commit `.env` file to git** (already in `.gitignore`)
- ✅ **Use strong client secrets** (24-month expiry recommended)
- ✅ **Limit API permissions** (only Sites.Read.All and Files.Read.All)
- ✅ **Use application permissions** (not delegated - no user context needed)

### Access Control

- ✅ **Principle of least privilege** - App only has read access
- ✅ **Admin consent required** - IT admin must approve permissions
- ✅ **Audit logging** - All API calls are logged in Azure AD

---

## ⚠️ 6. Error Handling

The SharePoint client handles these scenarios:

| Error | Handling |
|-------|----------|
| **Authentication failure** | Logs error, returns False, app exits gracefully |
| **File not found** | Logs 404 error, suggests checking file path |
| **Token expired** | Automatically re-authenticates and retries |
| **Network timeout** | Logs timeout, suggests checking connectivity |
| **Permission denied** | Logs 403 error, suggests checking API permissions |
| **Rate limiting** | Logs 429 error, suggests retry with backoff |

---

## 🧪 7. Testing Instructions

### Local Testing (Before Server Deployment)

1. **Test Authentication**:
   ```powershell
   python -c "from sharepoint_client import SharePointClient; import os; from dotenv import load_dotenv; load_dotenv(); client = SharePointClient(os.getenv('AZURE_TENANT_ID'), os.getenv('AZURE_CLIENT_ID'), os.getenv('AZURE_CLIENT_SECRET')); print('Auth:', client.authenticate())"
   ```

2. **Test File Download**:
   ```powershell
   # Will be added after sprint_capacity_app.py integration
   python sprint_capacity_app.py --test-sharepoint
   ```

3. **Test Full Application**:
   ```powershell
   python sprint_capacity_app.py --analyze
   ```

### Server Testing

1. Copy all files to server
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` file
4. Run manual test: `.\run_sprint_analysis.bat`
5. Check logs: `type logs\sprint_capacity.log`
6. Verify Task Scheduler execution

---

## ✅ 8. Advantages and Disadvantages

### Advantages ✅

| Advantage | Description |
|-----------|-------------|
| **No OneDrive sync required** | Works without OneDrive installed on server |
| **Always up-to-date** | Fetches latest file directly from SharePoint |
| **Enterprise-grade** | Uses Microsoft's official APIs |
| **Secure** | OAuth 2.0 authentication, no passwords in code |
| **Auditable** | All access logged in Azure AD |
| **Scalable** | Can access multiple files/sites easily |
| **Reliable** | Automatic token refresh, retry logic |

### Disadvantages ❌

| Disadvantage | Description |
|--------------|-------------|
| **Initial setup complexity** | Requires Azure AD app registration |
| **Dependency on Azure AD** | Requires admin consent for permissions |
| **API rate limits** | Microsoft Graph has throttling limits |
| **Network dependency** | Requires internet connectivity |
| **Token expiry** | Client secret expires (need renewal) |
| **Learning curve** | More complex than simple file copy |

---

## 📊 9. Comparison with Other Options

| Option | Complexity | Reliability | Maintenance | Best For |
|--------|-----------|-------------|-------------|----------|
| **Copy file to server** | ⭐ Low | ⭐⭐ Medium | ⭐ High (manual) | Quick testing |
| **OneDrive sync** | ⭐⭐ Medium | ⭐⭐⭐ High | ⭐⭐ Medium | User-based access |
| **Network share** | ⭐⭐ Medium | ⭐⭐ Medium | ⭐⭐ Medium | On-premise files |
| **SharePoint API** | ⭐⭐⭐ High | ⭐⭐⭐⭐ Very High | ⭐⭐⭐ Low (automated) | **Production (Recommended)** |

---

## 🎯 10. Next Steps

1. ✅ Azure AD app registration
2. ✅ Get SharePoint site URL and file path
3. ✅ Install Python packages on server
4. ✅ Configure `.env` file
5. ⏳ Integrate SharePoint client into `sprint_capacity_app.py`
6. ⏳ Test locally
7. ⏳ Deploy to server
8. ⏳ Test with Task Scheduler

---

## 📞 11. Troubleshooting

### Common Issues

**Issue**: "Authentication failed"
- **Solution**: Verify Tenant ID, Client ID, and Client Secret in `.env`

**Issue**: "File not found (404)"
- **Solution**: Check SharePoint file path, ensure file exists

**Issue**: "Permission denied (403)"
- **Solution**: Verify API permissions granted and admin consent given

**Issue**: "Token expired"
- **Solution**: Client automatically re-authenticates, check logs

**Issue**: "Network timeout"
- **Solution**: Check server internet connectivity, firewall rules

---

## 📚 12. Additional Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)
- [Azure AD App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [SharePoint REST API Reference](https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service)

---

**Implementation Status**: 🟡 In Progress - Awaiting integration into main application

