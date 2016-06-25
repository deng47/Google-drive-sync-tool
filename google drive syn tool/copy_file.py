"""
Input a file id and a parent id
Create a copy and modify its parent id
Return it id
"""

from get_creds import *

def copy_file(file_id, parent_id, file_name):
    body = {'name': file_name}
    body['parents'] = [parent_id]
    copy_id = DRIVE.files().copy(fileId=file_id, body=body).execute()
    return copy_id['id']
