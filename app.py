import os, sys
from flask import Flask, request

from util import facerec
from util import sheets

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"

@app.route("/locate-face", methods=["POST"])
def locate_face():
    return "hi"

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
sheets.init()
print("Server ready")

