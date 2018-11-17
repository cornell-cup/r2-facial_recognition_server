import face_recognition
import glob
import pickle
import json
import datetime

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
    fw = open('face_encoding_set.data', 'wb')
    pickle.dump(face_encoding_set, fw)
    fw.close()


"""
This function take in the images from path, match to the existing face set, and return the name.
Input: path | the path of test image 
Output: face_name | the person's name of the input image
"""
def recognize_face(path):
    # read back the data in face_encoding_set
    fd = open('face_encoding_set.data', 'rb')
    image_file = open(path, 'rb')
    face_encoding_set = pickle.load(fd)

    test_image = face_recognition.load_image_file(image_file.name)
    test_face_encoding = face_recognition.face_encodings(test_image)[0]
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(face_encoding_set, test_face_encoding)
    print("Is this a new face? {}".format(not True in results))
    for i in range(len(results)):
        if results[i]:
            print("The test is same as person")
            count = 0
            # find the file name with face name on it
            for image_name in glob.glob('face_set/*.jpg'):
                if count == i:
                    face_name = image_name.replace("face_set/", "").replace(".jpg", "")
                    return face_name
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
"""
def checkAttendance(face_name):
    # define a empty input name exception for null input
    # Name
    status_request = "";

    if(face_name):
        status_request == "fail"
    else:
        status_request == "success"

    # timeCheck
    now_time = datetime.datetime.now()
    today12pm = datetime.time(hour=12)

    # Status(need to update)
    # status_on_time = now_time <= today12pm
    status_on_time = True

    # MeetingType(need to update)
    meeting_type = 1

    # check already checked in or not
    if checkIfCheckedIn(face_name):
        status = 3
    else:  # check this person in
        if status_request == "success":  # input statues
            if status_on_time:
                status = 1  # success
            else:
                status = 4  # late
        else:
            status = 2  # fail

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


