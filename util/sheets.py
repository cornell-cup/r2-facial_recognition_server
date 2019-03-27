import datetime

from pprint import pprint
from googleapiclient import discovery

#from . import creds
import creds

service = None
'''
meeting:
time, day of week (dow), groups allowed

people:
group

day of week 0-6
'''
CHECK_IN_STATUSES = {
    1: "Success",
    2: "Failed",
    3: "Already checked in",
    4: "Late"
}

MEETING_TYPES = {
    1: "Saturday work meeting",
    2: "R2 Dave meeting",
    3: "R2 weekly work meeting",
    4: "Minibot Dave meeting",
    5: "Minibot weekly work meeting",
    6: "Communication Dave meeting",
    7: "Communication Weekly work meeting"
}

def init():
    '''
        Obtains credentials and sets up the sheets service
    '''
    global service
    print("Initalizing Sheets API...")
    
    credentials = creds.get_user_credentials("creds/user-secret.json")
    #credentials = creds.get_service_credentials("creds/sheets-test-secret.json")
    service = discovery.build("sheets", "v4", credentials=credentials)

def create_spreadsheet(spreadsheet_name, sheet_name):
    '''
        Create a new attendance spreadsheet with name spreadsheet_name
        The first sheet is named sheet_name

        Returns the created spreadsheet's id
    '''
    new_spreadsheet = {
        "properties": {
            "title": spreadsheet_name,
            "locale": "en",
            "timeZone": "America/New_York"
        },
        "sheets": [
            {
                "properties": {
                    "sheetId": 0,
                    "title": sheet_name,
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                },
                "data": {
                    "startRow": 0,
                    "startColumn": 0,
                    "rowData": {
                        "values": [
                            {
                                "userEnteredValue": {"stringValue": "Name"}
                            },
                            {
                                "userEnteredValue": {"stringValue": "Meeting Type"}
                            },
                            {
                                "userEnteredValue": {"stringValue": "Time"}
                            },
                            {
                                "userEnteredValue": {"stringValue": "Check-in Status"}
                            },
                        ]
                    }
                }
            }
        ]
    }
    '''
    ,
        "developerMetadata": [
            {
                "metadataKey": "signedInMembers",
                "metadataValue": "",
                "location": {
                    "spreadsheet": ,
                    
                },
                "visibility": "PROJECT"
            }
        ]
    '''

    request = service.spreadsheets().create(body=new_spreadsheet)

    new_sheet = request.execute()
    return new_sheet["spreadsheetId"]

def add_test_data():
    '''
    Adds test data
    '''
    spreadsheet_id = "1oXC40VF9RC2bvzystQ9iaO_2K0kzOqekAB2MZowdd2o"
    input_range = "First sheet!A1:B2"
    value_input_option = "USER_ENTERED"
    request_body = {
        "majorDimension": "ROWS",
        "values": [
            ["Hey", "this"],
            ["is", "123"]
        ]
    }
    
    request = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=input_range,
            body=request_body,
            valueInputOption=value_input_option)
    response = request.execute()
    pprint(response)

def add_sheet(spreadsheet_id, sheet_name):
    '''
    Adds a new sheet
    '''
    body = {
        "requests": [ 
            {
                "addSheet": {
                    "properties": {
                        "title": sheet_name,
                        "gridProperties": {
                            "frozenRowCount": 1
                        }
                    }
                }
            }
        ]
    }
    request = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    )

    response = request.execute()
    pprint(response)

    #now set up header row
    add_row([["Name", "Meeting Type", "Time", "Check-in Status"]],
            spreadsheet_id, sheet_name)

def add_row(values, spreadsheet_id, sheet_name="Sheet1"):
    '''
    Adds the data in the array "values" to the specified
    sheet in the spreadsheet
    
    values formatted as follows:
    [
        ["Row", "of", "data"],
        ["row", 2]
    ]
    
    Default sheet name is "Sheet1"
    '''

    #search through whole sheet
    input_range = sheet_name
    
    value_input_option = "USER_ENTERED"
    request_body = {
        "range": input_range,
        "majorDimension": "ROWS",
        "values": values
    }
    
    request = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=input_range,
            body=request_body,
            valueInputOption=value_input_option
        )
    response = request.execute()
    pprint(response)

def add_attendance(json_data, spreadsheet_id, sheet_name="Sheet1"):
    '''
    json_data is the output of the facial_recognition program,
    formatted as a dictionary.
    spreadsheet_id is a string

    Default sheet_name is "Sheet1"
    '''
    
    values = [
        [
            json_data["name"],
            MEETING_TYPES[json_data["meetingType"]],
            str(datetime.datetime.now()),
            CHECK_IN_STATUSES[json_data["checkInStatus"]]
        ]
    ]
    add_row(values, spreadsheet_id)

def is_checked_in(name, spreadsheet_id, sheet_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="%s!A:A"%(sheet_name),
        majorDimension="COLUMNS"
    ).execute()
    
    return name in result["values"][0]
    
if __name__ == "__main__":
    init()
    #spread_id = create_spreadsheet("hi there")
    spread_id = "10knpZyzaytlyvhTeg3tshXjZ-j6E2nCRz3xBQikZGwQ"
    '''
    add_row([
        ["Billy Jones", "R2 Weekly", 1243215453, "Late"]
    ])
    '''
    '''
    add_attendance({
        "name": "Billy Jones",
        "meetingType": 1,
        "checkInStatus": 4
    }, spread_id)
    '''
    print(is_checked_in("Billy Jones", spread_id, "Sheet1"))
    #add_sheet(spread_id, "new sheet")


