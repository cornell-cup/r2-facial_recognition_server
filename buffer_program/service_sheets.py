from pprint import pprint
from googleapiclient import discovery
from google.oauth2 import service_account
import google.auth

#this uses service accounts

#aka the auth url
SCOPE = 'https://www.googleapis.com/auth/spreadsheets'

try:
    #get application default credentials if they exist
    credentials, project = google.auth.default(
        scopes=[SCOPE])
except google.auth.exceptions.DefaultCredentialsError:
    print("default credentials not found, obtaining from json file")

    #create a new Credentials from file
    credentials = service_account.Credentials.from_service_account_file(
        "creds/sheets-test-secret.json")

    #get a new copy of Credentials, but with proper scope
    scoped_credentials = credentials.with_scopes([SCOPE])

#using service account
service = discovery.build("sheets", "v4", credentials=scoped_credentials)


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

