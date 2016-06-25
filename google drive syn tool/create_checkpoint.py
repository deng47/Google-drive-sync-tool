"""
Input file path, folder_path and the upload_record list
Create or update checkpoint.txt and sync_checkpoint.txt as checkpoint
checkpoint.txt record which file was processing before last breakdown
sync_checkpoint.txt record created file IDs and ParentIDs

"""

def create_checkpoint(path, folder_path, upload_record):
    file = open(folder_path+'\\checkpoint.txt','w', encoding='utf-8')
    file.write(path)
    file.close()
    file = open(folder_path+'\\sync_checkpoint.txt','w', encoding='utf-8')
    file.write(str(upload_record))
    file.close()
