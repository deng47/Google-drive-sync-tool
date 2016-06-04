"""
Input the path of a folder
Return a path tree list sorted by their lengths
"""

import os

def gen_pathTree(path):
    pathTree = []
    for dirName,subdirList,fileList in os.walk(path):
        pathTree.append(dirName)
        for fname in fileList:
            pathTree.append(dirName+os.sep+fname)
            
    pathTree = sorted(pathTree,key=len)
    
    return pathTree
            
