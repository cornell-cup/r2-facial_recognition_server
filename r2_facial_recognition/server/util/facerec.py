import face_recognition
import glob
import pickle
import json
from r2_facial_recognition.server.util import meeting

"""
How to use this module:

Step1: import all the headshot set 
import_headshot_set()

Step2: get the check-in result for this person in json format
checkInResult(path)
"""


def import_headshot_set():
    """
    This function import all the images of the headshot
    Input: none
    Output: none
    """
    face_encoding_set = {}
    print("Importing headshot...")
    for image_name in glob.glob('face_set/*.jpg'):
        import_headshot(image_name, False, face_encoding_set)
    print("Headshot imported!")
    # save the face_encoding_set to local text file
    fw = open('data/face_encoding_set.data', 'wb')
    pickle.dump(face_encoding_set, fw)
    fw.close()


def import_headshot(image_name, dump_set, face_encoding_set=None):
    if face_encoding_set is None:
        fd = open('data/face_encoding_set.data', 'rb')
        face_encoding_set = pickle.load(fd)
        fd.close()
    
    try:
        temp_image = face_recognition.load_image_file(image_name)
        temp_encoding = face_recognition.face_encodings(temp_image)[0]
        
        # truncate filename
        face_name = image_name.replace("face_set/", "").replace(".jpg", "")
        face_encoding_set[face_name[64:]] = temp_encoding
    except IndexError:
        print("I wasn't able to locate any faces in " + image_name +
              ". Check the image files. Aborting...")

    if dump_set:
        fw = open('data/face_encoding_set.data', 'wb')
        pickle.dump(face_encoding_set, fw)
        fw.close()
    print("import_headshot: saving headshot data")


def recognize_face(path):
    """
    This function take in the images from path, match to the existing face set,
     and return the name.
    Input: path | the path of test image
    Output: face_name | the person's name of the input image
            returns "None" if no person is found
    """
    # read back the data in face_encoding_set
    fd = open('data/face_encoding_set.data', 'rb')
    image_file = open(path, 'rb')
    face_encoding_set = pickle.load(fd)
    print(len(face_encoding_set))
    test_image = face_recognition.load_image_file(image_file.name)
    
    if len(face_recognition.face_encodings(test_image)) == 0:
        return "None" 
    
    test_face_encoding = face_recognition.face_encodings(test_image)[0]
    
    for key_name, encoding in face_encoding_set.items():
        if face_recognition.compare_faces(
                [encoding], test_face_encoding, tolerance=0.4)[0]:
            print("The test is same as person %s" % key_name)
            return key_name
            
    print("nothing found")
    return None


def get_new_image():
    return ""


class EmptyInputError(Exception):
    """no value for the face_name"""
    pass


def check_attendance(face_name):
    """
    This function check the attendance of person with the name and return a
    complete check in status in json
    Input: face_name | a person's name
    Output: a json | the person's check-in data in json format
            if face_name == "None", the fields in the output are undefined
    """
    # define a empty input name exception for null input
    # Name
    print("checkAttendance checking:")
    meeting_type = 0
    meeting_name = ""
    late = 0
    if face_name == "None":
        return parse_json(face_name, "fail", 999)

    if face_name:
        (name, m, l) = meeting.person_late(face_name)
        meeting_name = m
        late = l

    if meeting_name == "SaturdayMeeting":
        meeting_type = 1
    if meeting_name == "R2 Dave meeting":
        meeting_type = 2
    if meeting_name == "R2 Weekly work meeting":
        meeting_type = 3
    if meeting_name == "Minibot Dave meeting":
        meeting_type = 4
    if meeting_name == "Minibot Weekly work meeting":
        meeting_type = 5
    if meeting_name == "Communication Dave meeting":
        meeting_type = 6
    if meeting_name == "Communication Weekly work meeting":
        meeting_type = 7

    # check already checked in or not
    status = 1  # success
    if is_checked_in(face_name):
        status = 3  # Already checked in
    if late:
        status = 4  # late
    if not face_name:
        status = 2  # fail

    # FIXME: If this was what was done for NASA event, was it ever working?
    # status = 1  # for NASA event purpose
    # meeting_type = 1  # default
    
    print("this person is :", face_name, "   status:", status,
          "   meeting_type", meeting_type)
    return parse_json(face_name, status, meeting_type)


# check if the person has check in
# FIXME: Make this do something.
def is_checked_in(name):
    return True


def parse_json(face_name, check_in_status, meeting_type):
    """
    This function parse the check-in result to json
    Input: face_name      | name of the person
           checkInStatus  | check in status
           meetingType    | type of meeting
    Output: a json | the person's checkIn data in json format
    """
    check_in_data = {
        'name': face_name,
        'checkInStatus': check_in_status,
        'meetingType': meeting_type
        }
    check_in_result_json = json.dumps(check_in_data)

    return check_in_result_json


def get_check_in_result(path):
    """
    This function combines the recognize_face and checkAttendance, returns the
    check-in json.
    Input: path | the path of test image
    Output: a json | the person's checkIn data in json format
    """
    face_name = recognize_face(path)
    check_in_result = check_attendance(face_name)
    return check_in_result


