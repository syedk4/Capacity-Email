#!/usr/bin/env python3
"""
SharePoint Client for accessing Excel files from SharePoint/OneDrive for Business

This module handles authentication and file download from SharePoint using Microsoft Graph API.
"""

import os
import logging
import tempfile
from typing import Optional, Tuple
import msal
import requests
from pathlib import Path

logger = logging.getLogger(__name__)


class SharePointClient:
    """Client for accessing SharePoint files via Microsoft Graph API"""
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """
        Initialize SharePoint client with Azure AD credentials
        
        Args:
            tenant_id: Azure AD Tenant ID
            client_id: Azure AD Application (Client) ID
            client_secret: Azure AD Client Secret
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.access_token = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with Microsoft Graph API using client credentials flow
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            logger.info("Authenticating with Microsoft Graph API...")
            
            # Create MSAL confidential client application
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret
            )
            
            # Acquire token for Microsoft Graph
            result = app.acquire_token_for_client(scopes=self.scope)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                logger.info("✅ Authentication successful")
                return True
            else:
                error = result.get("error", "Unknown error")
                error_description = result.get("error_description", "No description")
                logger.error(f"❌ Authentication failed: {error} - {error_description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Authentication exception: {str(e)}")
            return False
    
    def download_file_from_sharepoint(
        self, 
        site_url: str, 
        file_path: str, 
        download_path: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Download a file from SharePoint
        
        Args:
            site_url: SharePoint site URL (e.g., "https://company.sharepoint.com/sites/sitename")
            file_path: Relative path to file in SharePoint (e.g., "/Shared Documents/file.xlsx")
            download_path: Local path to save file (if None, uses temp directory)
            
        Returns:
            Tuple[bool, Optional[str]]: (Success status, Local file path)
        """
        try:
            # Ensure we're authenticated
            if not self.access_token:
                if not self.authenticate():
                    return False, None
            
            logger.info(f"Downloading file from SharePoint: {file_path}")
            
            # Extract site name from URL
            site_name = self._extract_site_name(site_url)
            
            # Construct Microsoft Graph API URL
            # Format: /sites/{site-id}/drive/root:/{file-path}:/content
            graph_url = f"https://graph.microsoft.com/v1.0/sites/{site_name}/drive/root:{file_path}:/content"
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/octet-stream"
            }
            
            response = requests.get(graph_url, headers=headers, timeout=60)
            
            if response.status_code == 200:
                # Determine download path
                if download_path is None:
                    # Create temp file
                    temp_dir = tempfile.gettempdir()
                    filename = os.path.basename(file_path)
                    download_path = os.path.join(temp_dir, filename)
                
                # Save file
                with open(download_path, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"✅ File downloaded successfully to: {download_path}")
                return True, download_path
                
            elif response.status_code == 401:
                logger.error("❌ Authentication token expired or invalid. Re-authenticating...")
                # Try to re-authenticate and retry once
                if self.authenticate():
                    return self.download_file_from_sharepoint(site_url, file_path, download_path)
                return False, None
                
            elif response.status_code == 404:
                logger.error(f"❌ File not found in SharePoint: {file_path}")
                return False, None
                
            else:
                logger.error(f"❌ Failed to download file. Status: {response.status_code}, Response: {response.text}")
                return False, None
                
        except requests.exceptions.Timeout:
            logger.error("❌ Request timeout while downloading file from SharePoint")
            return False, None
        except Exception as e:
            logger.error(f"❌ Error downloading file: {str(e)}")
            return False, None
    
    def _extract_site_name(self, site_url: str) -> str:
        """
        Extract site name from SharePoint URL
        
        Args:
            site_url: Full SharePoint site URL
            
        Returns:
            str: Site identifier for Graph API
        """
        # Example: https://company.sharepoint.com/sites/sitename
        # Returns: company.sharepoint.com:/sites/sitename
        
        if "/sites/" in site_url:
            parts = site_url.split("/sites/")
            domain = parts[0].replace("https://", "").replace("http://", "")
            site_path = parts[1].rstrip("/")
            return f"{domain}:/sites/{site_path}"
        else:
            # Root site
            domain = site_url.replace("https://", "").replace("http://", "").rstrip("/")
            return domain

