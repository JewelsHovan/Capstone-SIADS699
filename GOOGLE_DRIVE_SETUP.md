# Google Drive Upload Setup Guide

This guide walks you through setting up Google Drive API access to upload your ML datasets.

## Quick Start

```bash
# 1. Install required packages
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# 2. Set up credentials (see detailed steps below)

# 3. Run upload
python scripts/upload_to_gdrive.py
```

---

## Detailed Setup Steps

### Step 1: Install Required Packages

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Add to requirements.txt:
```
google-api-python-client>=2.100.0
google-auth-httplib2>=0.1.1
google-auth-oauthlib>=1.1.0
```

---

### Step 2: Set Up Google Cloud Project

#### 2.1 Go to Google Cloud Console
- Visit: https://console.cloud.google.com/
- Sign in with your Google account

#### 2.2 Create/Select Project
- Click the project dropdown at the top
- Click "New Project"
- Name: "MADS Capstone" (or any name)
- Click "Create"

#### 2.3 Enable Google Drive API
- In the left sidebar, go to: **APIs & Services > Library**
- Search for: "Google Drive API"
- Click on it
- Click "Enable"

#### 2.4 Create OAuth 2.0 Credentials
- Go to: **APIs & Services > Credentials**
- Click "Create Credentials" → "OAuth client ID"
- If prompted, configure OAuth consent screen:
  - User Type: **External**
  - App name: "MADS Capstone Data Upload"
  - User support email: Your email
  - Developer contact: Your email
  - Click "Save and Continue" through the scopes (no scopes needed)
  - Add your email as a test user
  - Click "Save and Continue"
- Back to Create OAuth Client ID:
  - Application type: **Desktop app**
  - Name: "Desktop Client" (or any name)
  - Click "Create"

#### 2.5 Download Credentials
- You'll see a popup with Client ID and Client Secret
- Click "Download JSON"
- Save the file as `credentials.json` in your project root:
  ```
  /Users/julienh/Desktop/MADS/Capstone/credentials.json
  ```

⚠️ **Important**: Add `credentials.json` and `token.json` to `.gitignore`!

```bash
# Add to .gitignore
echo "credentials.json" >> .gitignore
echo "token.json" >> .gitignore
```

---

### Step 3: First Run (Authentication)

```bash
cd /Users/julienh/Desktop/MADS/Capstone
python scripts/upload_to_gdrive.py
```

**What happens:**
1. Script will open your browser
2. You'll be asked to log in with Google
3. Grant permission to access Google Drive
4. Credentials are saved to `token.json` for future use
5. Upload begins automatically

**First-time output:**
```
🔐 Authenticating with Google Drive...
   (Browser will open for authorization)

Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?...

✅ Credentials saved
✅ Successfully authenticated with Google Drive
```

---

## Usage Examples

### Upload Both Datasets (Default)
```bash
python scripts/upload_to_gdrive.py
```

Uploads:
- `data/processed/crash_level/*.csv` → `crash_level/` subfolder
- `data/processed/segment_level/*.csv` → `segment_level/` subfolder

### Upload Only Crash-Level Data
```bash
python scripts/upload_to_gdrive.py --crash-level-only
```

### Upload Only Segment-Level Data
```bash
python scripts/upload_to_gdrive.py --segment-level-only
```

### Upload to Different Folder
```bash
python scripts/upload_to_gdrive.py --folder-id YOUR_FOLDER_ID
```

To get folder ID from Google Drive URL:
```
https://drive.google.com/drive/folders/1xVGXbxUFHSdSawo2C9wnmABj15wPEX3A
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                         This is the folder ID
```

### Skip Existing Files
```bash
python scripts/upload_to_gdrive.py --no-replace
```

By default, existing files are replaced. Use `--no-replace` to skip them.

---

## What Gets Uploaded

### Directory Structure in Google Drive

```
Your Shared Folder (1xVGXbxUFHSdSawo2C9wnmABj15wPEX3A)
├── crash_level/
│   ├── train_20251026_160909.csv     (479 MB)
│   ├── val_20251026_160909.csv       (90 MB)
│   ├── test_20251026_160909.csv      (14 MB)
│   ├── train_20251026_160211.csv     (older version)
│   └── ...
│
└── segment_level/
    ├── segment_train_20251026_162447.csv  (79.5 MB)
    ├── segment_val_20251026_162447.csv    (0 MB)
    └── segment_test_20251026_162447.csv   (0 MB)
```

**Note**: Symlinks (like `train_latest.csv`) are skipped. Only actual files are uploaded.

### File Sizes

- Crash-level datasets: ~583 MB total
- Segment-level datasets: ~79.5 MB total
- **Total upload**: ~662 MB

Estimated upload time (depends on connection):
- Fast (100 Mbps): ~1 minute
- Medium (25 Mbps): ~4 minutes
- Slow (10 Mbps): ~10 minutes

---

## Troubleshooting

### Error: `credentials.json not found`

**Solution**: Download credentials from Google Cloud Console (Step 2.5 above)

### Error: `Access blocked: This app's request is invalid`

**Solution**: Make sure you:
1. Added your email as a test user in OAuth consent screen
2. Selected "Desktop app" as application type (not "Web application")

### Error: `The user has not granted the app permission`

**Solution**:
1. Delete `token.json`
2. Run script again
3. Make sure to click "Allow" when prompted in browser

### Upload Very Slow

**Tips**:
- Use `--crash-level-only` first, then `--segment-level-only`
- Close other bandwidth-heavy applications
- Consider uploading from a faster network

### Files Not Appearing in Google Drive

**Check**:
1. Make sure you're looking at the correct folder
2. Refresh the Google Drive page
3. Check subfolders (`crash_level/` and `segment_level/`)

---

## Security Notes

### Files to Keep Private

⚠️ **Never commit these files to Git**:
- `credentials.json` - Your OAuth credentials
- `token.json` - Your access token

Already added to `.gitignore`:
```bash
credentials.json
token.json
```

### Revoking Access

If you need to revoke access:
1. Go to: https://myaccount.google.com/permissions
2. Find "MADS Capstone Data Upload" (or your app name)
3. Click "Remove Access"
4. Delete `token.json` locally

---

## Advanced Usage

### Automating Uploads

Create a shell script for regular uploads:

```bash
#!/bin/bash
# upload_latest_data.sh

echo "Building latest datasets..."
python scripts/build_segment_dataset.py

echo "Uploading to Google Drive..."
python scripts/upload_to_gdrive.py

echo "Done!"
```

Make it executable:
```bash
chmod +x upload_latest_data.sh
./upload_latest_data.sh
```

### Checking What's Already Uploaded

The script automatically detects existing files and replaces them by default. To see what exists:

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json')
service = build('drive', 'v3', credentials=creds)

# List files in folder
results = service.files().list(
    q="'1xVGXbxUFHSdSawo2C9wnmABj15wPEX3A' in parents",
    fields="files(id, name, size)"
).execute()

for file in results.get('files', []):
    print(f"{file['name']}: {int(file.get('size', 0)) / 1024 / 1024:.1f} MB")
```

---

## References

- Google Drive API Documentation: https://developers.google.com/drive/api/guides/about-sdk
- Python Quickstart: https://developers.google.com/drive/api/quickstart/python
- OAuth 2.0 Guide: https://developers.google.com/identity/protocols/oauth2

---

## Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all setup steps were completed
3. Check Google Cloud Console for API errors
4. Ensure you have sufficient Google Drive storage space (need ~1 GB free)

**Last Updated**: 2025-10-26
