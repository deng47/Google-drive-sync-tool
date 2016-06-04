"""
Input a path tree list
Return a dictionary contains all paths as Key, and ['ParentId', 'FileId'] as Value
"""

def Dict_Name_ParentId_Id(pathTree):
    
    uploadList = {}
    for each in pathTree:
        uploadList[each] = ['ParentId', 'FileId']
        
    return uploadList
