# Google-drive-sync-tool
Create a mirror backup of a local folder to Google Drive root folder

Automatically check files on Google Drive

Prerequisite:

1. Python 3

2. Install google-api-python-client

3. Download your client_secret.json and leave it in the main folder (The client_secrets.json file format is a JSON formatted file containing the client ID, client secret, and other OAuth 2.0 parameters. 

For more: 
https://developers.google.com/drive/v3/web/quickstart/python#prerequisites 
https://developers.google.com/drive/v3/web/about-auth#OAuth2Authorizing https://www.youtube.com/watch?v=Z5G0luBohCg )

Usage:

Run main.py

It will prompt you to authorize access at the first time

Then just input the path of a folder, example: mirror(r'D:\My Data')

Keep the sync_record.txt

To-do:

Adjust algorithm




