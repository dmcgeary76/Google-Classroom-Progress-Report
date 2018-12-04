import mysql.connector
from mysql.connector import errorcode
from get_config import get_config_vals


def get_student_id(qual):
    vals = get_config_vals()
    pwd = vals[0]
    usr = vals[1]
    dbs = vals[2]

    # Define the general MySQL Command String and define args
    #query = 'SELECT id FROM %s WHERE %s = %s'
    query = 'select id from students where s_id = %s'
    args = [str(qual)]

    conn = mysql.connector.connect(user=usr ,password=pwd ,database=dbs)
    cursor = conn.cursor()

    try:
        cursor.execute(query,args)
        pass_id = cursor.fetchone()[0]
    except:
        pass_id = 20
    finally:
        cursor.close()
        conn.close()

    return(pass_id)


def get_assign_id(qual):
    vals = get_config_vals()
    pwd = vals[0]
    usr = vals[1]
    dbs = vals[2]

    # Define the general MySQL Command String and define args
    #query = 'SELECT id FROM %s WHERE %s = %s'
    query = 'select id from assignments where assignid = %s'
    args = [str(qual)]

    conn = mysql.connector.connect(user=usr ,password=pwd ,database=dbs)
    cursor = conn.cursor()

    try:
        cursor.execute(query,args)
        pass_id = cursor.fetchone()[0]
    except:
        pass_id = 41
    finally:
        cursor.close()
        conn.close()

    return(pass_id)


def get_course_id(qual):
    vals = get_config_vals()
    pwd = vals[0]
    usr = vals[1]
    dbs = vals[2]

    # Define the general MySQL Command String and define args
    #query = 'SELECT id FROM %s WHERE %s = %s'
    query = 'select id from courses where courseid = %s'
    args = [str(qual)]

    conn = mysql.connector.connect(user=usr ,password=pwd ,database=dbs)
    cursor = conn.cursor()

    try:
        cursor.execute(query,args)
        pass_id = cursor.fetchone()[0]
    except:
        pass_id = 13
    finally:
        cursor.close()
        conn.close()

    return(pass_id)


def insert_grade(submission):
    # Get the database values from config control
    vals = get_config_vals()
    usr = vals[1]
    pwd = vals[0]
    dbs = vals[2]
    assignid = get_assign_id(submission['courseWorkId'])
    submissionid = submission['id']
    studentid = get_student_id(submission['userId'])

    if submission['state'] == 'CREATED':
        state = 'Assignment Not Started'
    elif submission['state'] == 'RETURNED':
        state = str(submission['assignedGrade'])
    elif submission['state'] == 'TURNED_IN':
        state = 'Waiting to be Graded'
    else:
        state = "User Hasn't Accessed Course"

    # Define the general MySQL Command String and define args
    query = 'INSERT INTO grades(studentid,assignid,state,submissionid) VALUES(%s,%s,%s,%s)'
    args = [studentid, assignid, state, submissionid]

    conn = mysql.connector.connect(user=usr ,password=pwd ,database=dbs)
    cursor = conn.cursor()

    # does the grade entry exist?
    cursor.execute("SELECT COUNT(*) FROM grades WHERE submissionid = %s"
                    , [submissionid])

    row_count = cursor.fetchone()[0]
    if row_count == 0:
        cursor.execute(query, args,)
        conn.commit()
    else:
        cursor.execute("SELECT COUNT(*) FROM grades where submissionid = %s AND state = %s"
                        , [submissionid, state])
        row_count = cursor.fetchone()[0]
        if row_count == 0:
            cursor.execute("UPDATE grades SET state = %s WHERE submissionid = %s"
                            , [state, submissionid])
            conn.commit()
            print('Record %s has been update.' % submissionid)

    cursor.close()
    conn.close()


def insert_assignment(assignment):
    # Get the database values from config control
    vals = get_config_vals()
    usr = vals[1]
    pwd = vals[0]
    dbs = vals[2]

    # Define the general MySQL Command String and define args
    query = 'INSERT INTO assignments(assignid,name,courseid) VALUES(%s,%s,%s)'
    args = (assignment[0],assignment[1],courseid)

    conn = mysql.connector.connect(user=usr ,password=pwd ,database=dbs)
    cursor = conn.cursor()

    # cursor.execute(query, args)
    cursor.execute("SELECT COUNT(*) FROM assignments WHERE assignid = %s", (assignment[0],))

    row_count = cursor.fetchone()[0]
    if row_count == 0:
        cursor.execute(query, args,)
    else:
        print('The record for %s already exists.' % assignment[1])

    # Tidy up.
    conn.commit()
    cursor.close()
    conn.close()


def insert_course(course):
    # Get the database values from config control
    vals = get_config_vals()
    usr = vals[1]
    pwd = vals[0]
    dbs = vals[2]

    # Define the general MySQL Command String and define args
    query = 'INSERT INTO courses(name,courseid) VALUES(%s,%s)'
    args = (course[1],course[0])

    conn = mysql.connector.connect(user=usr ,password=pwd ,database=dbs)
    cursor = conn.cursor()

    # cursor.execute(query, args)
    cursor.execute("SELECT COUNT(*) FROM courses WHERE courseid = %s", (course[1],))

    row_count = cursor.fetchone()[0]
    if row_count == 0:
        cursor.execute(query, args)
    else:
        print('The record for %s already exists.' % student[1])

    # Tidy up.
    conn.commit()
    cursor.close()
    conn.close()


def insert_enrollment():
    # Get the database values from config control
    vals = get_config_vals()
    usr = vals[1]
    pwd = vals[0]
    dbs = vals[2]

    # Define the general MySQL Command String and define args
    query = 'INSERT INTO enrollments (studentid,courseid) VALUES(%s,%s)'
    args = (course[0],course[0])

    conn = mysql.connector.connect(user=usr ,password=pwd ,database=dbs)
    cursor = conn.cursor()

    # cursor.execute(query, args)
    cursor.execute("SELECT id FROM  WHERE courseid = %s", (course[1],))

    row_count = cursor.fetchone()[0]
    if row_count == 0:
        cursor.execute(query, args)
    else:
        print('The record for %s already exists.' % student[1])

    # Tidy up.
    conn.commit()
    cursor.close()
    conn.close()


def insert_student(student, vals):
    # Get the database values from config control
    usr = vals[1]
    pwd = vals[0]
    dbs = vals[2]

    # Define the general MySQL Command String and define args
    # Added where clause to prevent duplicates on email
    query = 'INSERT INTO students(s_id,name,email) VALUES(%s,%s,%s)'
    args = (student[0],student[1],student[2])

    # Create a new connector and intialize a cursor to deliver query
    conn = mysql.connector.connect(user=usr, password=pwd, database=dbs)
    cursor = conn.cursor()

    # cursor.execute(query, args)
    cursor.execute("SELECT COUNT(*) FROM students WHERE email = %s", (student[2],))

    row_count = cursor.fetchone()[0]
    if row_count == 0:
        cursor.execute(query, args)
    else:
        print('The record for %s already exists.' % student[1])

    '''
    if cursor.lastrowid:
        print('last insert id', cursor.lastrowid)
    else:
        print('last insert id not found')
    '''

    conn.commit()
    cursor.close()
    conn.close()


def main():
    get_student_id(...)


if __name__ == '__main__':
    main()
