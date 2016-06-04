"""
Input a file name
Return a dictionary of file md5s and ids on drive
Use md5 as key and id as value

"""

from get_creds import *

def getMd5Id_by_name(file_name):

    Dict = {}
    q="name='%s' and trashed=false" % file_name
    response = DRIVE.files().list(q=q,fields='files(id, name, md5Checksum)').execute()
    for file in response.get('files'):
        print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        Dict[file.get('md5Checksum')] = file.get('id')

    return Dict
