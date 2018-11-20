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

offset = 0
course_id = '24471685026'
email_key = [['Andrew Simmons', 'asimmons@wallerisd.net'],
             ['Ashauna Lindo', 'ashaunalindo@gmail.com'],
             ['Brenda Arteaga', 'barteaga@hcde-texas.org'],
             ['Candice Arthur', 'carthur@pasadenaisd.org'],
             ['Cindy Garcia', 'cgarcia@pasadenaisd.org'],
             ['Janet Nuzzie', 'jnuzzie@pasadenaisd.org'],
             ['John Fletcher', 'jfletcher@wallerisd.net'],
             ['Kathryn Palmer', 'kpalmer@humbleisd.net'],
             ['Kristi Archer', 'klarcher@katyisd.org'],
             ['Rebecca Terry', 'rterry@pasadenaisd.org'],
             ['Traci Powell', 'tpowell@pasadenaisd.org'],
             ['Vickie Cooper', 'vcooper@msn.com'],
             ['Wynette Fobbs', 'wfobbs@kleinisd.net'],
             ['Teacher21 Teacher21', 'dmcgeary@hcde-texas.org'],
             ['Kasey Davis', 'kasey.davis@humbleisd.net'],
             ['Guy James', 'guydjames@katyisd.org'],
             ['Debbie Hall', 'debhall945@gmail.com']]

assignment_key = get_assignments(course_id)
student_key = get_students(course_id)
progress_list = get_progress_list(course_id)
course_list = get_courses()

def write_hdr(message):
    with open('progress_list.csv', mode='w') as progress_file:
        progress_writer = csv.writer(progress_file, delimiter=',', quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)

        progress_writer.writerow(message)


def write_entry(message):
    with open('progress_list.csv', mode='a') as progress_file:
        progress_writer = csv.writer(progress_file, delimiter=',', quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)

        progress_writer.writerow(message)


# Write the headers for the progress_file
hdr_text = ['first_name', 'email']

title_list = []
count = 0
for assignment in assignment_key:
    if 'Optional' in assignment[1]:
        offset += 1
    hdr_text.append('Assign_Link_' + str(count))
    hdr_text.append('Assign_Grade_' + str(count))
    title_list.append('Assign_Title_' + str(count))
    count += 1

hdr_text.append('Status')
hdr_text.append('CourseTitle')
hdr_text.extend(title_list)

write_hdr(hdr_text)

# append additional rows for student data
for student in student_key:
    new_row = []
    new_row.append(student[1].split(' ')[0])
    for addy in email_key:
        if student[1] == addy[0]:
            new_row.append(addy[1])
    for i in progress_list:
        for j in i:
            for k in j:
                if student[0] == k[0]:
                    new_row.append(k[1])
                    new_row.append(k[2])
    target_total = len(assignment_key) - offset
    count = 0
    for entry in new_row:
        if isinstance(entry, int):
            count += 1
    if count >= target_total:
        new_row.append('You have completed this course.  You will receive your completion certificate later today.')
    else:
        new_row.append('You are almost done with the course! Try to finish the last remaining activities by Monday.')
    for course in course_list:
        if course[0] == course_id:
            new_row.append(course[1])
    for assignment in assignment_key:
        new_row.append(assignment[1])
    write_entry(new_row)

#if __name__ == '__main__':
