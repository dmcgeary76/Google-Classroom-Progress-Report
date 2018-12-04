from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Import a student_list function so that we can identify course participants
from get_student_list import get_students
from get_assignment_list import get_assignments
from get_course_list import get_courses
from mysql_demo import insert_grade, get_course_id, get_assign_id, get_student_id
from get_config import get_config_vals


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.coursework.students.readonly'
course_id = '20106357846'


def get_grades(temp_id, tempwork_id):
    '''
    get the grade data from each submitted assignment.
    The only information of value here is the id value for the
    student, the link to the student's grade file, and the grade or
    grade status as a string
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

    # This needs to happen in all get_scripts.  Uses grade submission data to write new submissions to db.
    for submission in submission_list:
        insert_grade(submission)


def main():
    courses = get_courses()
    for course in courses:
        assignments = get_assignments(course[0])
        for assignment in assignments:
            get_grades(course[0],assignment[0])


if __name__ == '__main__':
    main()
