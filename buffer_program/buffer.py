import socket
import sys
import json
import datetime
import requests

# defining the api-endpoint
API_ENDPOINT_Name = ""
API_ENDPOINT_CheckInData = ""

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

#Copy images to fr_program dir: need to change after figuring out the address

def changeDir():
	src_dir = "source_directory"
	dst_dir = "destination_directory"
	for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
    	shutil.copy(jpgfile, dst_dir)

#remove unwanted images from the buffer_program dir
def removeIm():
	for i in glob.glob("*.jpg"):
    	os.remove(i)



#Check the attendance of person with the name and return a complete check in status in json format
def checkAttendance(inputNameJson):

    text = json.loads(inputNameJson)

    #Name
    face_name = text[name]
    status_request = text[status]

    #timeCheck
    nowTime = datetime.datetime.now()
    today12pm = datetime.time(hour=12)

    #Status(need to update)
    statusOnTime = nowTime <= today12pm

    #MeetingType(need to update)
    meetingType = 1

    status = 0

    # check already checked in or not
    if (checkIfCheckedIn(face_name)):
        status = 3
    else:  # check this person in
        if status_request == "success":  # input statues
            if statusOnTime:
                status = 1  # success
            else:
                status = 4  # late
        else:
            status = 2  # fail

    return parseToJson(face_name, status, meetingType)

#check if the person has check in
def checkIfCheckedIn(name):
    return True

#Parse the Check in result to json
def parseToJson(face_name, checkInStatus, meetingType):
   CheckInData = {
        'name': face_name,
        'checkInStatus': checkInStatus,
        'meetingType': meetingType
    }

    jsonCheckInData = json.dumps(CheckInData)

    return jsonCheckInData

def get_request_name():
    try:
        r = requests.get(API_ENDPOINT_Name)
        data_name = r.json()
        r.raise_for_status()
        return data_name
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)



def send_request_checkInData(checkIndata):
    try:
        r = requests.post(url=API_ENDPOINT_CheckInData, json=checkIndata)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)



def main():
    getImage()

    #get the name from API_ENDPOINT_Name
    name = get_request_name()

    #send the checkInData to API_ENDPOINT_CheckInData
    CheckInData = checkAttendance(name)
    send_request_checkInData(CheckInData)

