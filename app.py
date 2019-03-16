import os, sys
from flask import Flask, request

from util import facerec
from util import sheets
from util import learnface

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SAVE_TEST_FOLDER"] = "test_friends"

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
    #name = "bob"

    file.save(os.path.join(
        app.config["UPLOAD_FOLDER"],
        "temp.png"))
    
    if face_exists(name):
        print("exists")
        #return "exists"
        return make_response(300)

    f = open("%s%s"%(app.config["UPLOAD_FOLDER"], "temp.png"), "rb")
    
    hexed = hexify(file)

    file.save(os.path.join(
        app.config["SAVE_TEST_FOLDER"],
        "%s%s.JPG"%(hexed, name)))
    
    return make_response(200)

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
        "test.png"))
    
    name = facerec.recognize_face(os.path.join(
        app.config["UPLOAD_FOLDER"],
        "test.png"))
    
    return facerec.checkAttendance(name)

@app.route("/")
def root():
    return "hello"

print("Server initializing...")
facerec.import_headshot_set()
#sheets.init()
print("Server ready")

