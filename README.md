# r2-facial_recognition_server buffer program
Authors: Rong Tan, Stanley Lin
This program is part of the R2 facial recognition server code.

### General info
Language: Python

Input: JSON

Output: JSON

Libraries: `google-auth` `google-auth-oauthlib` `flask` `face_recognition`

Install neccessary libraries with `pip`

### Running the program
Set the environment variable `FLASK_ENV=development`. Then call `flask run --no-reload` (due to how the program handles oauth for the Sheets API, running with reload enabled will cause problems). To change the host and port, consult `flask run --help`.

### Description
This program will act as an API server. It will listen for HTTP requests sent to it via the client and process the image file to be sent to the facial recognition program. The result from that program will be returned to the client.

### Input
This program will utilize flask as the webserver.
The client will send a POST request encoded with `multipart/form-data`. The server will expect the following format:
```
{
	"image": <raw image file>
}
```

### Output
The JSON output from the facial recognition program will be returned to the client, unmodified.


### Modules

#### sheets
Uses Google Sheets API

Uploads the check in status of a person to a Google spreadsheet

Input: JSON

Output: None

#### facerec
Uses `face_recognition` python library

This program first imports all headshots and then returns the JSON which contains the check in status of person. If no person was identified, the fields in the output are undefined.

Input: location of image file (string) 

Output: check in status in JSON format
```
{
	"name": <string>,
	"checkInStatus": <string>,
	"meetingType": <number>
}
```

