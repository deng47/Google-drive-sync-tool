"""
Input the path of a file and its parent id
Upload the file
Return its id on Google Drive
"""

import os
from get_creds import *
from apiclient.http import MediaFileUpload

def create_file(path, parentId=None):
    media_body = MediaFileUpload(path)

    body = {'name': os.path.basename(path)}
    if parentId:
        body['parents'] = [parentId]

    file_id = DRIVE.files().create(body=body, media_body=media_body, fields="id").execute()
    print('Uploaded:   ', path)
    return file_id['id']
