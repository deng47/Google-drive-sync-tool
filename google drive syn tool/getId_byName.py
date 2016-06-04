"""
Input file name
Return a list of file ids on drive

"""
from get_creds import *

def getId_byName(file_name):
    
    file_id = []
    q="name='%s' and trashed=false" % file_name
    response = DRIVE.files().list(q=q,fields='files(id, name)').execute()
    for file in response.get('files'):
        print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        file_id.append(file.get('id'))

    return file_id
