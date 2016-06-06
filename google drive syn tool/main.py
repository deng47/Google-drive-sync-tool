"""
Input the path of a folder
Example: mirror(r'D:\My Data')
Create a mirror backup of the local folder to Google Drive root folder
"""

import os
from get_creds import *
from gen_pathTree import *
from list_root import *
from Dict_Name_ParentId_Id import *
from getId_byName import *
from getId_byParentId import *
from getParentId_byId import *
from getMd5Id_by_name import *
from getParentIdId_byName import *
from create_file import *
from create_folder import *
from copy_file import *
from generate_md5 import *
from delete_file import *

def mirror(folder_path):
    #list all files inside
    upload_order = gen_pathTree(folder_path)
    
    #record all file names and their ids and parent ids on Google Drive
    upload_record = Dict_Name_ParentId_Id(upload_order)
    
    #find out whether the top-level folder exists in the root folder of Google Drive
    top_folder_name = os.path.split(folder_path)[1]
    
    #list all files and folders in the root folder
    files_in_root = list_root()
    
    for each in files_in_root:
        #if exist, record its parent id and id
        if top_folder_name == each[0]:
            upload_record[upload_order[0]] = ['root',each[1]]
            break
        
    #if not exist, create it and record its parent id and id
    if upload_record[upload_order[0]] == ['ParentId', 'FileId']:
        id = create_folder(upload_order[0])
        upload_record[upload_order[0]] = ['root',id]
    
    #find out whether files and folders exist on Google Drive, upload/pass them and record their parent id and id
    for each in upload_order[1:]:
        #record parent id
        parent_id = upload_record[os.path.split(each)[0]][1]
        upload_record[each][0] = parent_id
        
        #when it is a file
        if os.path.isfile(each):
            file_name = os.path.basename(each)
            
            #check md5 hash
            local_file_md5 = generate_md5(each)          
            drive_file_md5 = getMd5Id_by_name(file_name)
            #if exist, check parent id
            if local_file_md5 in drive_file_md5:
                id_by_md5 = drive_file_md5[local_file_md5]
                #record id
                if parent_id == getParentId_byId(id_by_md5):
                    upload_record[each][1] = id_by_md5
                #copy file and modify its parent id and record it
                else:
                    upload_record[each][1] = copy_file(id_by_md5, parent_id, file_name)                    
                    
            #if not, create it and record id
            else:
                upload_record[each][1] = create_file(each, parent_id)
                
        #when it is a folder     
        else:
            file_name = os.path.split(each)[1]
            
            #check folder id and parent id
            path = getParentIdId_byName(file_name)
            
            #if exist, record id
            if parent_id in path:
                upload_record[each][1] = path[parent_id]
            #if not, create it and record id
            else:
                upload_record[each][1] = create_folder(each, parent_id)
    
    #delete files
    #try to find out whether there is a sync record
    try:
        file = open(folder_path+'\\sync_record.txt')
        sync_record = eval(file.read())
        for each in sync_record:
            if each not in upload_record:
                try:
                    delete_file(sync_record[each][1])
                except:
                    pass
    except:
        print('Can not read sync_record.txt')
    
    finally:
        file = open(folder_path+'\\sync_record.txt','w')
        file.write(str(upload_record))
        file.close()
        print('\nsync_record.txt saved\n')
    
    print('\n\n++++++++++++++++++++++++\n+++ Backup Completed +++\n++++++++++++++++++++++++\n\n')
    
    
    
    
    
    
    
    
