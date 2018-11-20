from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Import a student_list function so that we can identify course participants
from get_student_list import get_students
from get_assignment_list import get_assignments

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.coursework.students.readonly'
course_id = '20106357846'


def get_grades(temp_id, tempwork_id):
    '''
    get the grade data from each submitted assignment.  The only information of value here is the id value for the
    student, the link to the student's grade file, and the grade or grade status as a string
    :param temp_id:
    :param tempwork_id:
    :return:
    '''
    student_key = get_students(temp_id)
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('classroom', 'v1', http=creds.authorize(Http()))

    results = service.courses().courseWork().studentSubmissions().list(courseId=temp_id, courseWorkId=tempwork_id).execute()
    submission_list = results.get('studentSubmissions', [])

    submission_master = [[] for i in range(len(submission_list))]

    count = 0
    for submission in submission_list:
        submission_master[count].append(submission['userId'])
        submission_master[count].append(submission['alternateLink'])
        if submission['state'] == 'RETURNED':
            submission_master[count].append(submission['assignedGrade'])
        elif submission['state'] == 'TURNED_IN':
            submission_master[count].append('Assignment is being graded.')
        else:
            submission_master[count].append('Assignment not yet completed')
        count += 1
    return submission_master


def get_progress_list(temp_id):
    '''
    The progress_list is meant to pull all grade data into one large list.  This is necessary for the creation of the
    progress report pdf document and the email that is automatically sent out.
    :param temp_assignment_key:
    :param temp_id:
    :return:
    '''
    assignment_key = get_assignments(temp_id)
    progress_list = [[] for i in range(len(assignment_key))]
    count = 0
    for assignment in assignment_key:
        progress_list[count].append(get_grades(temp_id, assignment[0]))
        count += 1
    return progress_list

if __name__ == '__main__':
    get_progress_list(course_id)
