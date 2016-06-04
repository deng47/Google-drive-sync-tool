"""
Input a file id
Return its parent id

"""
from get_creds import *

def getParentId_byId(file_id):

    response = DRIVE.files().get(fileId=file_id,fields='parents').execute()

    return response['parents'][0]
