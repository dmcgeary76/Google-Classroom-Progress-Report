from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.courses.readonly'
course_id = courseId

def get_course_list():
    '''
    Get a list of the students (and their corresponding ids) from the target course roster.
    :param temp_id:
    :return:
    '''
    store = file.Storage('tokencl.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('classroom', 'v1', http=creds.authorize(Http()))

    results = service.courses().list().execute()
    course_list = results.get('courses', [])

    for course in course_list:
        print(course)
    return course_list

if __name__ == '__main__':
    get_course_list()
