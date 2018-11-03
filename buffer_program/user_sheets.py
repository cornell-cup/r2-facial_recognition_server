from pprint import pprint
from googleapiclient import discovery
from google_auth_oauthlib.flow import Flow, InstalledAppFlow

#this uses user accounts

#useful: https://developers.google.com/api-client-library/python/guide/aaa_oauth

#aka the auth url
SCOPE = 'https://www.googleapis.com/auth/spreadsheets'

#A flow object has functionality to help gain user credentials

#the following code uses a generalized flow, which allows manual handling of the authorization code
'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#create a new flow object from a client secrets file, which stores parameters for oauth2
flow = Flow.from_client_secrets_file(
        "creds/client_secret.json",
        scopes=[SCOPE],
        redirect_uri="urn:ietf:wg:oauth:2.0:oob")

#now, user must navigate to a url to provide consent
auth_url, state = flow.authorization_url()
print("Go here: {}".format(auth_url))

#user will get an authorization code, which is used to get access token
code = input("Enter code: ")

#final step, get the access token
flow.fetch_token(code=code)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#the following code uses an InstalledAppFlow, making the acquisition of the authorization code easier

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
flow = InstalledAppFlow.from_client_secrets_file(
        "creds/client_secret.json",
        scopes=[SCOPE])

#this will create a temporary local server that attempts to redirect the browser to the auth url. It listens for the authorization code in the response. Once it gets it, it will shut down. It will also acquire the access token
flow.run_local_server()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#get the credentials
credentials = flow.credentials

service = discovery.build("sheets", "v4", credentials=credentials)

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

