from pprint import pprint
from googleapiclient import discovery
import creds

service = None
spreadsheet_id = "1oXC40VF9RC2bvzystQ9iaO_2K0kzOqekAB2MZowdd2o"

def init():
    '''
        Obtains credentials and sets up the sheets service
    '''
    global service
    
    credentials = creds.get_user_credentials("creds/user-secret.json")
    #credentials = creds.get_service_credentials("creds/sheets-test-secret.json")
    service = discovery.build("sheets", "v4", credentials=credentials)

def create_spreadsheet():
    '''
        Create a new test spreadsheet and print out the response
    '''
    test_spreadsheet = {
        "properties": {
            "title": "Hello test",
            "locale": "en",
            "timeZone": "America/New_York"
        },
        "sheets": [
            {
                "properties": {
                    "sheetId": 0,
                    "title": "First sheet",
                    "tabColor": {
                        "green": 1
                    }
                }
            }
        ]
    }

    request = service.spreadsheets().create(body=test_spreadsheet)

    new_sheet = request.execute()
    pprint(new_sheet)

def add_data():
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

def add_row(values):
    '''
    Adds the data in the array "values" to the spreadsheet
    values formatted as follows:
    [
        ["Row", "of", "data"],
        ["row", 2]
    ]
    '''

    #search through whole sheet
    input_range = "First sheet"
    
    value_input_option = "USER_ENTERED"
    request_body = {
        "range": input_range,
        "majorDimension": "ROWS",
        "values": [
            ["new", "line"],
        ]
    }
    
    request = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=input_range,
            body=request_body,
            valueInputOption=value_input_option
        )
    response = request.execute()
    pprint(response)

init()
#create_spreadsheet()
add_row()


