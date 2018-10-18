from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Import a student_list function so that we can identify course participants
from get_student_list import get_students
from get_assignment_list import get_assignments

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.coursework.students.readonly'
course_id = '16954164213'

student_key = get_students(course_id)
assignment_key = get_assignments(course_id)

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
