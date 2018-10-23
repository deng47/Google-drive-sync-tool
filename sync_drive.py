#!/usr/bin/env python3

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
import os
import hashlib
import argparse


class File():

    def __init__(self, name, file_id=None, parent_id=None):
        if name.startswith('/'):
            self.directory = os.path.split(name)[0]
            self.name = os.path.split(name)[1]
        else:
            self.directory = os.getcwd()
            self.name = name
        self.path = self.directory + '/' + self.name
        self.isfolder = os.path.isdir(self.path)
        self.file_id = file_id
        if parent_id == None:
            self.parent_id='root'
        else:
            self.parent_id = parent_id
        self.local_md5 = ''
        self.remote_md5 = ''
        self.children = None

    def get_children(self):
        if self.isfolder:
            children = [ self.path + '/' + each for each in os.listdir(self.path) ]
            self.children = { each:self.file_id for each in children }

    def get_local_md5(self, path):
            
        def read_chunks(fp):
            fp.seek(0)
            chunk = fp.read(8 * 1024)
            while chunk:
                yield chunk
                chunk = fp.read(8 * 1024)
            else:
                fp.seek(0)

        m = hashlib.md5()
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                for chunk in read_chunks(fp):
                    m.update(chunk)
        elif path.__class__.name__ in ["StringIO", "cStringIO"] \
                or isinstance(path, file):
            for chunk in read_chunks(path):
                m.update(chunk)
        else:
            self.local_md5 = ''
        self.local_md5 = m.hexdigest()

    def get_remote_md5(self, drive):
        self.remote_md5 = drive.get_id_md5(self.name, self.parent_id)

    def upload_file(self, drive):
        if self.isfolder:
            self.file_id = drive.create_folder(self.path, self.parent_id)
        else:
            self.file_id = drive.create_file(self.path, self.parent_id)
        print("%s uploaded" % self.name)

    def upload_correctly(self, drive):
        md5_match = False
        if self.isfolder and drive.get_id(self.name, self.parent_id):
            self.file_id = drive.get_id(self.name, self.parent_id)[0]
            md5_match = True
            return md5_match
        if self.isfolder and not drive.get_id(self.name, self.parent_id):
            self.upload_file(drive)
            md5_match = True
            return md5_match
        self.get_remote_md5(drive)
        self.get_local_md5(self.path)
        for each in self.remote_md5:
            if self.remote_md5[each] != self.local_md5:
                self.remove_drive_file(each, drive)
                print("%s removed" % self.name)
            else:
                self.file_id = each
                md5_match = True
        return md5_match

    def remove_drive_file(self, file_id, drive):
        drive.remove(file_id)


class My_drive():

    def __init__(self, json_file, destination_path):
        store = file.Storage(json_file)
        creds = store.get()
        self.connection = build('drive', 'v3', http=creds.authorize(Http()))
        self.path_names = destination_path.split('/')
        self.parent_id = self.get_dst_id(self.path_names)

    def create_folder(self, path, parent_id=None):
        folder_name = os.path.split(path)[1]
        if parent_id==None:
            parent_id = self.parent_id
        folder = {'name' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder', 'parents':[parent_id]}
        folder_id = self.connection.files().create(body=folder, fields='id').execute()
        print("Created folder %s" % folder_name)
        return folder_id['id']

    def create_file(self, path, parent_id=None):
        print("Uploading %s" % path)
        DEFAULT_CHUNK_SIZE = 512*1024
        media_body = MediaFileUpload(path, None, DEFAULT_CHUNK_SIZE, True)
        body = {'name': os.path.basename(path)}
        if parent_id == None:
            parent_id = self.parent_id
        body['parents'] = [parent_id]
        file_id = self.connection.files().create(body=body, media_body=media_body, fields="id").execute()
        return file_id['id']

    def get_id(self, name, parent_id):
        q="name='%s' and parents='%s' and trashed=false" % (name, parent_id)
        response = self.connection.files().list(q=q,fields='files(id)').execute()
        ids = [ each.get('id') for each in response.get('files') ]
        return ids
    
    def get_dst_id(self, path_names, parent_id=None):
        for index in range(len(path_names)):
            if index == len(path_names) - 1:
                return parent_id
            if index == 0:
                parent_id = 'root'
            q="name='%s' and parents='%s' and trashed=false" % (path_names[index+1], parent_id)
            response = self.connection.files().list(q=q,fields='files(id)').execute()
            if response.get('files'):
                parent_id = [ each.get('id') for each in response.get('files') ][0]
            else:
                parent_id = self.create_folder(path_names[index+1], parent_id)

    def get_id_md5(self, name, parent_id):
        files = {}
        q="name='%s' and parents='%s' and trashed=false" % (name, parent_id)
        response = self.connection.files().list(q=q,fields='files(id, md5Checksum)').execute()
        for each in response.get('files'):
            files[each.get('id')] = each.get('md5Checksum')
        return files

    def remove(self, file_id):
        self.connection.files().delete(fileId=file_id).execute()
        self.file_id = ''

def sync(path, drive, file_id=None, parent_id=None):
    if parent_id==None:
        parent_id=drive.parent_id
    file_tree = File(path, file_id, parent_id)
    if file_tree.upload_correctly(drive):
        print("%s found" % file_tree.name)
        if file_tree.isfolder:
            file_tree.get_children()
            if file_tree.children == []:
                return None
            for each in file_tree.children:
                sync(each, drive, None, file_tree.file_id)
    else:
        file_tree.upload_file(drive)
        if file_tree.isfolder:
            file_tree.get_children()
            if file_tree.children == []:
                return None
            for each in file_tree.children:
                sync(each, drive, None, file_tree.file_id)


def parse_args():
    parser = argparse.ArgumentParser(
        description = "A command line tool talks to Google Drive API. It uploads a local folder to Google Drive, and checks md5 checksum to ensure the integrity of data"
                        )
    parser.add_argument(
        "--src", required = True)
    parser.add_argument(
        "--dst", required = True)
    return parser.parse_args()


def main():
    args = parse_args()
    source_path = args.src
    destination_path = args.dst
    if destination_path.endswith('/'):
        destination_path = source_path[:-1]
    if source_path.endswith('/'):
        source_path = source_path[:-1]

    gd = My_drive('/project/Google-drive-sync-tool/storage.json', destination_path)
    sync(source_path, gd)


if __name__ == '__main__':
    main()
