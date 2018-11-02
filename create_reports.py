from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from get_grade_data import get_progress_list
from get_assignment_list import get_assignments
from get_student_list import get_students
import csv
from pprint import pprint

course_id = courseId

'''
There is, no doubt, a much more elegant way to do all of this.  I welcome any feedback.
'''

# The student roster pull doesn't contain email info so I made a master list of users and emails
email_key = [[Name, Email],
            ...,
            ...]

# Collect a list of assignments, students, and coursework entries
assignment_key = get_assignments(course_id)
student_key = get_students(course_id)
progress_list = get_progress_list(assignment_key, course_id)

# Create a new document for a progress_report csv file
def write_hdr(message):
    with open('progress_list.csv', mode='w') as progress_file:
        progress_writer = csv.writer(progress_file, delimiter=',', quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)

        progress_writer.writerow(message)

# Append to an existing CSV
def write_entry(message):
    with open('progress_list.csv', mode='a') as progress_file:
        progress_writer = csv.writer(progress_file, delimiter=',', quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)

        progress_writer.writerow(message)

if __name__ == '__main__':
    
    # Write the headers for the progress_file
    hdr_text = ['first_name', 'email']

    for assignment in assignment_key:
        hdr_text.append(assignment[1] + '_link')
        hdr_text.append(assignment[1] + '_grade')

    write_hdr(hdr_text)

    # append additional rows for student data
    for student in student_key:
        new_row = []
        new_row.append(student[1].split(' ')[0])
        for addy in email_key:
            if student[1] == addy[0]:
                new_row.append(addy[1])
        for i in progress_list:                 #this is a messy recursion through the progress_list
            for j in i:                         #every courseWork item is buried in two nested null lists
                for k in j:
                    if student[0] == k[0]:      #if the studentId matches, then add content for the courseWork
                        new_row.append(k[1])
                        new_row.append(k[2])
        write_entry(new_row)                    #append the new record listing to the CSV
