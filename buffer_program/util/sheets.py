from googleapiclient import discovery

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
