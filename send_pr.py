from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import mimetypes
import os
import base64
from apiclient import errors

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.send'


def send_msg(message_text, recipient, subject):
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token_gm.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials_gm.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
        """
    user_id = 'me'
    message = MIMEText(message_text, 'html')
    message['to'] = recipient
    message['from'] = user_id
    message['subject'] = subject
    msg = {'raw': base64.urlsafe_b64encode(message.as_string())}
    message = (service.users().messages().send(userId=user_id, body=msg)
               .execute())

if __name__ == '__main__':
    send_msg(create_main('David'))
