import face_recognition
import glob
import pickle
import json
import datetime
from util import meeting

"""
How to use this module:

Step1: import all the headshot set 
import_headshot_set()

Step2: get the check-in result for this person in json format
checkInResult(path)
"""


"""
This function import all the images of the headshot
Input: none
Output: none
"""
def import_headshot_set():
    face_encoding_set = []
    print("Importing headshot...")
    for image_name in glob.glob('face_set/*.jpg'):
        try:
            temp_image = face_recognition.load_image_file(image_name)
            temp_encoding = face_recognition.face_encodings(temp_image)[0]
            face_encoding_set.append(temp_encoding)
        except IndexError:
            print("I wasn't able to locate any faces in " + image_name + ". Check the image files. Aborting...")
    print("Headshot imported!")
    # save the face_encoding_set to local text file
    fw = open('data/face_encoding_set.data', 'wb')
    pickle.dump(face_encoding_set, fw)
    fw.close()


"""
This function take in the images from path, match to the existing face set, and return the name.
Input: path | the path of test image 
Output: face_name | the person's name of the input image
        returns "None" if no person is found
"""
def recognize_face(path):
    # read back the data in face_encoding_set
    fd = open('data/face_encoding_set.data', 'rb')
    image_file = open(path, 'rb')
    face_encoding_set = pickle.load(fd)
    print(len(face_encoding_set))
    test_image = face_recognition.load_image_file(image_file.name)
    if len(face_recognition.face_encodings(test_image)) == 0:
        return "None" 
    test_face_encoding = face_recognition.face_encodings(test_image)[0]
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(face_encoding_set, test_face_encoding, tolerance=0.4)
    # print("Is this a new face? {}".format(not True in results))
    for i in range(len(results)):
        if results[i]:
            print("The test is same as person")
            count = 0
            # find the file name with face name on it
            for image_name in glob.glob('face_set/*.jpg'):
                if count == i:
                    face_name = image_name.replace("face_set/", "").replace(".jpg", "")
                    #return the name from 65th character to the end, truncating the hash
                    return face_name[64:]
                    break;
                count += 1
            break

def get_new_image():
    return ""

class EmptyInputError(Exception):
   """no value for the face_name"""
   pass


"""
This function check the attendance of person with the name and return a complete check in status in json
Input: face_name | a person's name 
Output: a json | the person's check-in data in json format
        if face_name == "None", the fields in the output are undefined
"""
def checkAttendance(face_name):
    # define a empty input name exception for null input
    # Name
    print("checkAttendance checking:")
    meeting_type = 0
    meetingName = ""
    late = 0
    if face_name == "None":
        return parseToJson(face_name, "fail", 999)

    if(face_name):
        (name, m, l) = meeting.PersonLate(face_name)
        meetingName = m
        late = l

    if meetingName == "SaturdayMeeting":
        meeting_type = 1
    if meetingName == "R2 Dave meeting":
        meeting_type = 2
    if meetingName == "R2 Weekly work meeting":
        meeting_type = 3
    if meetingName == "Minibot Dave meeting":
        meeting_type = 4
    if meetingName == "Minibot Weekly work meeting":
        meeting_type = 5
    if meetingName == "Communication Dave meeting":
        meeting_type = 6
    if meetingName == "Communication Weekly work meeting":
        meeting_type = 7

    # check already checked in or not
    status = 1 #success
    if checkIfCheckedIn(face_name):
        status = 3 #Already checked in
    if late:
        status = 4 #late
    if not face_name:
        status = 2 # fail
    print("this person is :", face_name, "   status:", status, "   meeting_type", meeting_type)
    return parseToJson(face_name, status, meeting_type)

# check if the person has check in
def checkIfCheckedIn(name):
    return True

"""
This function parse the check-in result to json
Input: face_name      | name of the person
       checkInStatus  | check in status
       meetingType    | type of meeting
Output: a json | the person's checkIn data in json format
"""
def parseToJson(face_name, checkInStatus, meetingType):
    check_in_data = {
        'name': face_name,
        'checkInStatus': checkInStatus,
        'meetingType': meetingType
        }
    checkInResult_json = json.dumps(check_in_data)

    return checkInResult_json

"""
This function combines the recognize_face and checkAttendance, returns the check-in json.
Input: path | the path of test image 
Output: a json | the person's checkIn data in json format
"""
def checkInResult(path):
    face_name = recognize_face()
    CheckInResult = checkAttendance(face_name)
    return CheckInResult


