'''
A function to help simplify the creation of the html template needed for the
html email body text needed in the Mimetext payload.
'''
from create_pr import pr
from send_pr import send_msg

c_id = '24471685026'
master_record = pr(c_id)

def create_main(std_record):
    msg_text = str('<p>' + std_record[0] + ',</p>'
                +'<p>Below is the progress report for the course: <b>'
                + std_record[-1] + '</b>'
                + '<p>As a reminder, you can access all of your completion certificates'
                + ' from the shared Google Drive folder under your GCE training account.</p>'
                + '<p>Course Completion Status: <b>' + std_record[-2] + '</b></p>'
                + '<table cell-spacing="0" cell-padding="0" style="border:none; text-align:center;">'
                + '<tbody><tr>'
                + '<td width="220" style="background:#880e4f; color:white;">Assignment Title</td>'
                + '<td width="220" style="background:#880e4f; color:white;">Link to Assignment</td>'
                + '<td width="220" style="background:#880e4f; color:white;">Status</td></tr>')
    offset = 0
    while True:
        place = (2 + 3*offset)
        if std_record[place] != std_record[-2]:
            msg_text = str(msg_text
                + '<tr><td width="220" style="background:#fde3ec; color:black;">'
                + str(std_record[place]) + '</td>'
                + '<td width="220" style="background:#fde3ec; color:black;">'
                + '<a href="' +str(std_record[place+1]) + '">Assignment</a></td>'
                + '<td width="220" style="background:#fde3ec; color:black;">'
                + str(std_record[place+2]) + '</td></tr>')
            offset += 1
        else:
            msg_text = str(msg_text + '</tbody></table><br />'
                + '<pr>As always, if you have any questions or concerns about this'
                + ' course, then please do not hesitate to contact us.</pr>'
                + '<p>Your Friendy Neighborhood Instructors,<br />'
                + 'Lynnice and David')
            break
    return msg_text

if __name__ == '__main__':
    for record in master_record:
        rec_adr = record[1]
        subj = 'Progress Report: ' + str(record[-1])
        send_msg(create_main(record), rec_adr, subj)
