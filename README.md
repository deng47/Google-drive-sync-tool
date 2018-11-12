# Google-drive-sync-tool
Upload a local folder to Google Drive



Prerequisite:

1. Python 3

2. Install google-api-python-client

3. Download your client_secret.json and leave it in the main folder (The client_secrets.json file format is a JSON formatted file containing the client ID, client secret, and other OAuth 2.0 parameters. 

For more: 
https://developers.google.com/drive/v3/web/quickstart/python#prerequisites 
https://developers.google.com/drive/v3/web/about-auth#OAuth2Authorizing
https://www.youtube.com/watch?v=Z5G0luBohCg )


##Usage:
  - Make sure you have the client_secret.json
  - Run ./get_creds.py to get credentials and store it into storage.json
  - ./sync_drive.py --rsc /local path --dst /Google Drive path

