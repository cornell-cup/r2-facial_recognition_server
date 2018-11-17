# r2-facial_recognition_server buffer program
Authors: Rong Tan, Stanley Lin
This program is part of the R2 facial recognition server code.

### General info
Language: Python

Input: JSON

Output: JSON

Libraries: `google-auth` `google-auth-oauthlib`

Install neccessary libraries with `pip`

### Description
This program will act as an API server. It will listen for HTTP requests sent to it via the client and process the image file to be sent to the facial recognition program. The result from that program will be returned to the client.

### Input
This program will utilize flask as the webserver.
JSON data from the client, formatted as follows:
```
{
	"image": <base64 encoded string>
}
```

### Output
The JSON output from the facial recognition program will be returned to the client, unmodified.

#r2-facial_recognition_server_util_sheets
###General Description

Language: Python

API: Google sheet API

###Description
This program is to record people's sign-in status in a google doc.

Input: JSON

Output: Google doc with people's sign-in status

#r2-facial_recognition_server_util_facerec

###General Info
Language: Python

Input: None

Output: checkin result for people in JSON format

###Description
This program first import all headshots and then return the JSON which contains the information of checkin status for people.