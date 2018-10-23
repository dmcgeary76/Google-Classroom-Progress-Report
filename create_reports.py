from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from get_grade_data import get_progress_list
from get_assignment_list import get_assignments
from get_student_list import get_students

course_id = '16954164213'
assignment_key = get_assignments(course_id)
student_key = get_students(course_id)

progress_list = get_progress_list(assignment_key, course_id)
print(progress_list[0][0])

# If modifying these scopes, delete the file gs_token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
spreadsheet_id = '1uS-4WDfkEwrj-BlsbCyWi-JEVhK84A4cJW4qCQAs4Cc'
sheet_id = 0   # The int id of the sheet containing the template

def new_pr_sheet(temp_spreadsheet_id, temp_sheet_id):
    """
    Make a copy of a progress report template and copy that sheet into a new spreadsheet document.
    """
    store = file.Storage('gs_token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials2.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    spreadsheet = {
        'destination_spreadsheet_id': '1MNsq1-C0D5vbm-d-D1EmSN35RVTxIbWwJpMN2OD2R7g',
    }

    request = service.spreadsheets().sheets().copyTo(spreadsheetId=temp_spreadsheet_id,
                                                          sheetId=temp_sheet_id, body=spreadsheet)
    response = request.execute()
    return response

if __name__ == '__main__':
    store = file.Storage('gs2_token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials2.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    count = 0
    for student in student_key:
        body_info = {
            "majorDimension": "ROWS",
            "range": "D1",
            "values": [
                [
                    "David"
                ]
            ]
        }
        count += 1
        print(student)
        new_pr_sheet(spreadsheet_id, sheet_id)
        request = service.spreadsheets().values().append(spreadsheetId='1MNsq1-C0D5vbm-d-D1EmSN35RVTxIbWwJpMN2OD2R7g',
                                                         range='D1',
                                                         valueInputOption='RAW',
                                                         insertDataOption='OVERWRITE', body=body_info)
        response = request.execute()
