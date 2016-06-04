"""
Input folder id
Return a list of file ids in the folder on drive or None

"""
from get_creds import *

def getId_byParentId(ParentId):

    file_id = []
    q="'%s' in parents and trashed=false" % ParentId
    response = DRIVE.files().list(q=q,fields='files(id, name)').execute()
    for file in response.get('files'):
        print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        file_id.append(file.get('id'))
        
    return file_id
