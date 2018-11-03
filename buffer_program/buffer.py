import socket
import sys
<<<<<<< HEAD
#added
import glob
import shutil
import os

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print('Failed to create socket')
	sys.exit()
print('Socket Created')

host = '192.168.4.148'
port = 6000

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
	print('Hostname could not be resolved. Exiting')
	sys.exit()

#Connect to remote server
s.connect((remote_ip , port))
print('Socket Connected to ' + host + ' on ip ' + remote_ip)

filename = open('camerashot.jpg', 'wb')
while True:
    strng = s.recv(1024)
    if not strng:
        break
    filename.write(strng)
filename.close()
print('received, yay!')
s.close()
=======
import json
import datetime
from buffer_program.facial_recognition import parse_json

#get image from the Rasberry Pi via socket
def getImage():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()
    print('Socket Created')

    host = '192.168.4.148'
    port = 6000

    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    #Connect to remote server
    s.connect((remote_ip , port))
    print('Socket Connected to ' + host + ' on ip ' + remote_ip)


    filename = open('camerashot.jpg', 'wb')
    while True:
        strng = s.recv(1024)
        if not strng:
            break
        filename.write(strng)

    filename.close()
    print('received, yay!')

    s.close()

#Check the attendance of person with the name and return a complete check in status in json format
def checkAttendance(inputNameJson):

    text = json.loads(inputNameJson)

    #Name
    face_name = text[name]

    #timeCheck
    nowTime = datetime.datetime.now()
    today12pm = datetime.time(hour=12)

    #Status(need to update)
    statusOnTime = nowTime <= today12pm

    #MeetingType(need to update)
    meetingType = "Saturday Work Meeting"

    return parseToJson(face_name, nowTime, statusOnTime, meetingType)

#Parse the Check in result to json
def parseToJson(face_name, nowTime, statusOnTime, meetingType):
    statusInString = ""
    if statusOnTime:
        status = "OnTime"
    else:
        status = "Late"

        CheckInData = {
        'name': face_name,
        'CurrentTime': nowTime,
        'Status': status,
        'MeetingType': meetingType
    }

    jsonCheckInData = json.dumps(CheckInData)

    return jsonCheckInData


>>>>>>> 4cd7d95de5392d1b7c61776cbb97208970b74828
