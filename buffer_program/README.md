# r2-facial_recognition_server buffer program
Authors: Rong Tan, Stanley Lin
This program is part of the R2 facial recognition server code.

### General info
Language: Python

Input: JSON

Output: JSON

Libraries: `flask`

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

