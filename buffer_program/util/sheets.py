from pprint import pprint
from googleapiclient import discovery
import creds

service = None

def init():
    '''
        Obtains credentials and sets up the sheets service
    '''
    #credentials = creds.get_user_credentials("creds/user-secret.json")
    credentials = creds.get_service_credentials("creds/sheets-test-secret.json")
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
