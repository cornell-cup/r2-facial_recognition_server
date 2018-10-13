# Facial Recognition Program

### General Info
Language: Java

Input: Preprocessed image data

Output: JSON

Libraries: OpenCV

Must be manually called

If you aren't running Windows, then it is **required** to build OpenCV from source. Visit [this](https://docs.opencv.org/3.4.3/d9/d52/tutorial_java_dev_intro.html) page for instructions. Note the location of the jar and library output and either move it to a more suitable location, or ensure that your build tools point to the output location.

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

