from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.coursework.students.readonly'
course_id = '20106357846'

def get_assignments(temp_id):
    '''
    Get a list of the assignments (and their ids) from the target course roster.
    :param temp_id:
    :return:
    '''
    store = file.Storage('token3.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('classroom', 'v1', http=creds.authorize(Http()))

    results = service.courses().courseWork().list(courseId=temp_id).execute()
    activity_list = results.get('courseWork', [])

    activity_master = [[] for i in range(len(activity_list))]

    #return an activity list with id and title to simplify table references
    count = 0
    for activity in activity_list:
        activity_master[count].append(activity['id'])
        activity_master[count].append(activity['title'])
        count += 1

    return activity_master

# Useful as a one-off to get a list of courses.
if __name__ == '__main__':
    print(get_assignments(course_id))
