import os, sys
from flask import Flask, request, make_response

from util import facerec
from util import sheets
from util import learnface

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["UPLOAD_FILENAME"] = "test.png"
app.config["SAVE_TEST_DIR"] = "test_friends"
app.config["FACE_SET_DIR"] = "face_set"

@app.route("/locate-face", methods=["POST"])
def locate_face():
    return "hi"

@app.route("/save-face", methods=["POST"])
def save_face():
    '''
    Takes picture of face and saves as image file
    named after the person

    will need to send over the person's name
    '''
    file = request.files["image"]
    name = request.form["name"]

    file.save(os.path.join(
        app.config["UPLOAD_FOLDER"],
        app.config["UPLOAD_FILENAME"]))
    
    '''
    https://stackoverflow.com/questions/16133923/
    400-vs-422-response-to-post-of-data
    '''
    if learnface.face_exists(
            app.config["UPLOAD_FOLDER"],
            app.config["UPLOAD_FILENAME"]):
        return make_response(("Face exists", 422))

    #get hash of the image, to differentiate
    #between people with the same name
    hexed = learnface.hexify(
            app.config["UPLOAD_FOLDER"],
            app.config["UPLOAD_FILENAME"])
    
    f = open(os.path.join(app.config["UPLOAD_FOLDER"],
        app.config["UPLOAD_FILENAME"]), "rb")
    
    newfilename = "%s%s.jpg"%(hexed, name)
    #save the new face
    newfile = open(os.path.join(
        app.config["FACE_SET_DIR"],
        newfilename),
        "wb")
    newfile.write(f.read())

    facerec.import_headshot(
            os.path.join(
                app.config["FACE_SET_DIR"],
                newfilename),
            True)
    
    newfile.close()
    f.close()
    
    return make_response(("OK", 200))

#call the facial recognition library code
@app.route("/identify-face", methods=["POST"])
def identify_face():
    '''
    Calls the facial recognition library code and
    checks in the person if recognized
    '''
    file = request.files["image"]

    file.save(os.path.join(
        app.config["UPLOAD_FOLDER"],
        app.config["UPLOAD_FILENAME"]))
    
    name = facerec.recognize_face(os.path.join(
        app.config["UPLOAD_FOLDER"],
        app.config["UPLOAD_FILENAME"]))
    
    return facerec.checkAttendance(name)

@app.route("/")
def root():
    return "hello"

print("Server initializing...")
facerec.import_headshot_set()
sheets.init()
print("Server ready")

