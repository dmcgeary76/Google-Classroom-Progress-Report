from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from mysql_demo import insert_course

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.courses.readonly'

def get_courses():
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

    simple_list = [[] for course in course_list]

    count = 0
    for course in course_list:
        simple_list[count].append(course['id'])
        simple_list[count].append(course['name'])
        count += 1
    return simple_list

if __name__ == '__main__':
    courses = get_courses()
    for course in courses:
        insert_course(course)
