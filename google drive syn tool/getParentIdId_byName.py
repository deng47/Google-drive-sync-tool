"""
Input a file name
Return a dictionary of file parent ids and file ids on drive
Use parent id as key and file id as value
"""

from get_creds import *

def getParentIdId_byName(file_name):

    Dict = {}
    q="name='%s' and trashed=false" % file_name
    response = DRIVE.files().list(q=q,fields='files(id, name, parents)').execute()
    for file in response.get('files'):
        print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        Dict[file.get('parents')[0]] = file.get('id')

    return Dict
