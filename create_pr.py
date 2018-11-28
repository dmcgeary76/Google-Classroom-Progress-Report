from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from get_grade_data import get_progress_list
from get_assignment_list import get_assignments
from get_student_list import get_students
from get_course_list import get_courses
import csv
from pprint import pprint

c_id = <your course_id number>   #Just for testing


def pr(course_id):
    # Email addresses don't come out of the GC API, so we need a reference for them.  This is that reference.
    email_key = [['John Doe', 'john.doe@example.com'],
             ['Jane Doe', 'jane.doe@example.com'],
             ]
    
    # We need to pull assignment names, student names, progress on assignments, and the course title.
    assignment_key = get_assignments(course_id)
    student_key = get_students(course_id)
    progress_list = get_progress_list(course_id)
    course_list = get_courses()
    
    # Couple of variables to initialize
    master_record = []
    offset = 0
    
    # Need to discount optional assignments for the course status value
    for assignment in assignment_key:
        if 'Optional' in assignment[1]:
            offset += 1

    # append additional rows for student data
    for student in student_key:
        new_row = []
        asn_list = []
        new_row.append(student[1].split(' ')[0])
        for addy in email_key:
            if student[1] == addy[0]:
                new_row.append(addy[1])
        for i in progress_list:
            for j in i:
                for k in j:
                    if student[0] == k[0]:
                        asn_list.append([k[1], k[2]])
        as_count = 0
        for assignment in assignment_key:
            new_row.append(assignment[1])
            new_row.append(asn_list[as_count][0])
            new_row.append(asn_list[as_count][1])
            as_count += 1
        target_total = len(assignment_key) - offset
        count = 0
        for entry in asn_list:
            if isinstance(entry[1], int):
                count += 1
        if count >= target_total:
            new_row.append('You have completed this course.  You will ' +
                            'receive your completion certificate later today.')
        else:
            new_row.append('You are almost done with the course! Try to finish'+
                            ' the last remaining activities to stay current with your credits.')
        for course in course_list:
            if course[0] == course_id:
                new_row.append(course[1])
        master_record.append(new_row)
    return master_record


if __name__ == '__main__':
    print(pr(c_id))  # Just to test
