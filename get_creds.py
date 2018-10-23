"""
Get credentials and store it into storage.json
"""

from __future__ import print_function
import os

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def get_creds():
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    CLIENT_SECRET = 'client_secret.json'
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata https://www.googleapis.com/auth/drive'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPES)
        creds = tools.run_flow(flow, store)

    return creds

creds = get_creds()
http=creds.authorize(Http())
DRIVE = build('drive','v3', http=http)
