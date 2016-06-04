"""
Input a file id
Delete the file
"""

from get_creds import *

def delete_file(file_id):
    file_name = DRIVE.files().get(fileId=file_id).execute()
    DRIVE.files().delete(fileId=file_id).execute()
      
    print('Deleted', file_name.get('name'))
