from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Import a student_list function so that we can identify course participants
from get_student_list import get_students

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.coursework.students.readonly'
course_id = '16954164213'
courseWork_id = '17368122104'

student_master = get_students(course_id)

activity_master = [['Are you interested in a Google Hangouts Tutorial Session?', '17447959824'],
                   ['Flubaroo and You!', '17418001075'],
                   ['Importing Data from an Online Source', '17414066482'],
                   ['Pivot Power!', '17412675728'],
                   ['Google Sheets Pre-Skills Assessment', '17368122104'],
                   ['In the space below describe a way that you might be able to use Fusion Table in your classroom.',
                    '17334714619'], ['Practicing the Basics of Google Sheets', '17334447819']]

def get_grades(temp_id, tempWork_id):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('classroom', 'v1', http=creds.authorize(Http()))

    results = service.courses().courseWork().studentSubmissions().list(courseId=temp_id, courseWorkId=tempWork_id).execute()
    activity_list = results.get('studentSubmissions', [])

    activity_master = [[] for i in range(len(activity_list))]
