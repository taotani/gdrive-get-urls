from __future__ import print_function
import pickle
import sys
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import functools
import pandas as pd

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def share_file(service, file):
    file_id = file['id']
    user_permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(
            fileId=file_id,
            supportsAllDrives = True,
            body=user_permission
    ).execute()
    result = service.files().get(fileId=file_id, supportsAllDrives = True, fields='webViewLink').execute()
    return result


def get_parent_folders(service, title):
    page_token = None
    files = []
    while True:
        response = service.files().list(q=f"name = '{title}'",
                                          spaces = 'drive',
                                          includeItemsFromAllDrives = True,
                                          supportsAllDrives = True,
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            files.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files

def list_files(service, parent):
    page_token = None
    files = []
    while True:
        response = service.files().list(q=f"\'{parent['id']}\' in parents",
                                          spaces = 'drive',
                                          fields='nextPageToken, files(id, name)',
                                          supportsAllDrives = True,
                                          includeItemsFromAllDrives = True,
                                          pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            files.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    print(sys.argv[1])
    # Call the Drive v3 API
    candidates = get_parent_folders(service, sys.argv[1])
    print(candidates)
    files = functools.reduce(lambda x, y: x + list_files(service, y), candidates, [])
    print(files)
    links = list(map(lambda x: {'file_name': x['name'], 'url' : share_file(service, x)['webViewLink']}, files))
    df = pd.DataFrame(links)
    df.to_csv('urls.csv')
    

if __name__ == '__main__':
    main()
