#!/usr/bin/env python3
"""
Google Drive Upload with Manual Authentication

This version prints the auth URL instead of auto-opening browser,
so you can paste it into an incognito window with the correct Google account.

Usage:
    python upload_to_gdrive_manual_auth.py
"""

import os
import sys
from pathlib import Path

# Temporarily override the auth flow to not auto-open browser
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

print("\n" + "="*70)
print("🔐 MANUAL AUTHENTICATION MODE")
print("="*70)
print("\nThis will give you a URL to paste in an incognito window")
print("so you can log in with your SCHOOL email.\n")

# Check for credentials file
if not os.path.exists(CREDENTIALS_FILE):
    print(f"❌ Error: {CREDENTIALS_FILE} not found")
    sys.exit(1)

# Delete old token if it exists
if os.path.exists(TOKEN_FILE):
    os.remove(TOKEN_FILE)
    print("🗑️  Deleted old token.json\n")

# Create flow
flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)

# Get authorization URL (don't auto-open browser)
flow.redirect_uri = flow._OOB_REDIRECT_URI if hasattr(flow, '_OOB_REDIRECT_URI') else 'urn:ietf:wg:oauth:2.0:oob'

auth_url, _ = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print("="*70)
print("📋 COPY THIS URL:")
print("="*70)
print(f"\n{auth_url}\n")
print("="*70)
print("\n✨ STEPS:")
print("  1. Open an INCOGNITO/PRIVATE browser window")
print("  2. Paste the URL above")
print("  3. Log in with your SCHOOL email")
print("  4. Click 'Allow'")
print("  5. Copy the authorization code")
print("  6. Paste it below\n")
print("="*70)

# Get authorization code from user
auth_code = input("\n🔑 Paste the authorization code here: ").strip()

# Exchange code for token
try:
    flow.fetch_token(code=auth_code)
    creds = flow.credentials

    # Save credentials
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

    print("\n✅ Authentication successful!")
    print(f"✅ Credentials saved to {TOKEN_FILE}")
    print("\n🎉 You can now run: python scripts/upload_to_gdrive.py")

except Exception as e:
    print(f"\n❌ Authentication failed: {e}")
    sys.exit(1)
