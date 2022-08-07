from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import base64
from bs4 import BeautifulSoup

def ten_events():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    if os.path.exists('tokenCalendar.json'):
        creds = Credentials.from_authorized_user_file('tokenCalendar.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('tokenCalendar.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('calendar', 'v3',credentials=creds)

        now = datetime.datetime.now().isoformat() + 'Z'
        print('[INFO]: GETTING THE UPCOMING 10 EVENTS')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True, 
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print("no upcoming events found.")
            return
        
        return events

    except HttpError as error:
        print('An error occurred: %s' % error)
        return

def gmail_main():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    if os.path.exists('tokenGmail.json'):
        creds = Credentials.from_authorized_user_file('tokenGmail.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokenGmail.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return
        print('Mails:')
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            try:
                payload = txt['payload']
                headers = payload['headers']
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']
                    
                    # body of the msg is encrypted format so have to decode it
                    # with base64 decoder
                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace("-","+").replace("_", "/")
                decoded_data = base64.b64decode(data)

                    # now the data is on lxml format will parse it with
                    # BeautifulSoup library

                soup = BeautifulSoup(decoded_data, "lxml")
                body = soup.body()
                #Subject = " ".join(["Subject: ", str(subject)])
            except:
                pass

            Subject = "Subject: " + str(subject)
                #Sender = " ".join(["Sender: ", str(sender)])
            Sender = "Sender: " + str(sender)
            Sender = re.sub("[\(\[].*?[\)\]]", "", Sender)
                #Body = " ".join(["Body: ", str(body)])
            Body = "Body: " + str(body)
            mail = Subject + Sender + Body
        return mail
    
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

#gmail_main()
#ten_events()