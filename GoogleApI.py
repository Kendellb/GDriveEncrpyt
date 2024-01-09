from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import io
import auth 
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'FinalProject'


authIntsance = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authIntsance.get_credentials()
http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive','v3',http=http)

def uploadFile(fileName):
    try:
        file_metadata = {'name': fileName}
        filePath = "/home/kendell/Documents/Cosc460/FinalProjectKB/"+fileName
        media = MediaFileUpload(filePath,mimetype="text/plain")
        file = drive_service.files().create(body=file_metadata,media_body=media,fields = 'id').execute()
        fileID = file.get('id')
        print('File ID: ' + fileID)
    except FileNotFoundError:
        print("\n File does not exist please double check\n")

def downloadFile(file_id,fileName):
    try:
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            #print("Ready to dowload!")
            print("Download %d%%." % int(status.progress()*100))
        with io.open("/home/kendell/Documents/Cosc460/FinalProjectKB/" + fileName,'wb') as f:
            fh.seek(0)
            f.write(fh.read())
    except FileNotFoundError:
        print("\nFile does not exist please double check\n")
    except Exception:
        pass

def searchFile(query):
        results = drive_service.files().list(
            pageSize=100,fields="nextPageToken,files(id,name)", q = "name contains  '" + query +
            "'").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            for item in items:
                print("file found:")
                #print(item['id'])
                print(item['name'])

def fileID(query):
    results = drive_service.files().list(
        pageSize=100,fields="nextPageToken,files(id,name)", q = "name contains  '" + query +
            "'").execute()
    items = results.get('files', [])
    if not items:
            print('No files found.')
    else:
        for item in items:
            print("file found:")
            print(item['id'])
            return item['id']




def main():
    userid = input()
    searchFile(userid)
    file = fileID(userid)
    downloadFile(file,userid)

if __name__ == '__main__':
    main()