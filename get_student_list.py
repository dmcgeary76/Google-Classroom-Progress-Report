from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.rosters.readonly'
course_id = courseId

def get_students(temp_id):
    '''
    Get a list of the students (and their corresponding ids) from the target course roster.
    :param temp_id:
    :return:
    '''
    store = file.Storage('token2.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('classroom', 'v1', http=creds.authorize(Http()))

    results = service.courses().students().list(courseId=temp_id).execute()
    student_list = results.get('students', [])

    student_master = [[] for i in range(len(student_list))]

    count = 0
    for student in student_list:
        student_master[count].append(student['userId'])
        student_master[count].append(student['profile']['name']['fullName'])
        count += 1

    return student_master

if __name__ == '__main__':
    get_students(course_id)
