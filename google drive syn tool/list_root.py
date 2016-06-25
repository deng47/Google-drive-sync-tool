"""
Return a list of file names and their ids in the root folder of Google Drive

"""
from get_creds import *

def list_root():

    file_id = []
    q="'%s' in parents and trashed=false" % 'root'
    response = DRIVE.files().list(q=q,fields='files(id, name)').execute()
    for file in response.get('files'):
        file_id.append([file.get('name'), file.get('id')])
        
    return file_id
