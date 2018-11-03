import face_recognition
import glob
import pickle
import json

face_encoding_set = []

# import all the images of the headshot
def import_headshot_set():
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


# this function can read the image named test.jpg and match to the existing face set
def recognize_face():
    # read back the data in face_encoding_set
    fd = open('face_encoding_set.data', 'rb')
    face_encoding_set = pickle.load(fd)

    test_image = face_recognition.load_image_file("test.jpg")
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
                    temp_json = parse_json(face_name)
                    break;
                count += 1
            break

#define a empty input name exception for null input
class EmptyInputError(Exception):
    """no value for the face_name"""
    pass

#parse the face_name into json and send it to buffer program with exception handing for empty input
def parse_json(face_name):
    try:
        if(face_name):
            raise EmptyInputError
        data = {
            'name': face_name,
        }
        inputNameJson = json.dumps(data)
        return inputNameJson
    except EmptyInputError:
        print("Error! This person is in Cornell Cup.")
        data = {}
        return json.dumps(data)



import_headshot_set()
recognize_face()