# Facial Recognition Program

### General Info
Language: Python

Input: Preprocessed image data

Output: JSON

Libraries: face_recognition

Must be manually called

### Description
This program will receive preprocessed image data from the buffer program. It will execute the neccessary facial recognition related algorithms and output a result, stored in JSON format. This will make a call to a database containing image data for all Cornell Cup team members. This program will be manually called.

JSON data is formatted as follows:
```
{
	name: <string>,
	checkInStatus: <int>,
	meetingType: <MeetingTypeId>
}
```
`checkInStatus` is an integer value indicating the outcome of the check in operation. Possible values:
* `1`: success
* `2`: failed
* `3`: already checked in
* `4`: late

`MeetingtypeId` is an integer value indicating the type of the meeting. Possible values:
* `1`: Saturday work meeting
* `2`: R2 Dave meeting
* `3`: R2 weekly work meeting
* `4`: Labo Dave meeting
* `5`: Labo weekly work meeting

Note that there is no support at the moment for meeting types other than the ones listed.

### Algorithms Used
\<pending\>

