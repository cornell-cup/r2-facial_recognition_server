# Facial Recognition Program

### General Info
Language: Java

Input: Preprocessed image data

Output: JSON

Libraries: OpenCV

Must be manually called

### Description
This program will receive preprocessed image data from the buffer program. It will execute the neccessary facial recognition related algorithms and output a result, stored in JSON format. This will make a call to a database containing image data for all Cornell Cup team members. This program will be manually called.

JSON data is formatted as follows:
```
{
	name: <string>,
	checkInStatus: <int>,
	meetingTime: <MeetingId>
}
```
`checkInStatus` is a integer value indicating the outcome of the check in operation. Possible values:
* `1`: success
* `2`: failed
* `3`: already checked in
* `4`: late

`MeetingId` is an enum with values corresponding to different meeting types. Possible values:
\<TODO\>


### Algorithms Used
\<pending\>

