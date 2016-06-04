from get_creds import *

files = DRIVE.files().list().execute()
items = files.get('files', [])
for item in items:
    print('\nname',item['name'],item['id'])
    
print('Done')


