from get_creds import *

def search_by_name(file_name):

    q="name='%s' and trashed=false" % file_name
    response = DRIVE.files().list(q=q,fields='files(id, name, md5Checksum)').execute()
    for file in response.get('files', []):
        # Process change
        print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        print(file.get('md5Checksum'))
        return file.get('id')
