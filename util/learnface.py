import hashlib
import facerec

import os

def hexify(f):
    '''
    Generates a hash from the given image
    '''
    hash_func = hashlib.sha256()
    hash_func.update(f.read())
    return hash_func.digest()

def face_exists(name, upload_dir):
    '''
    Check if an image with the passed in name exists
    '''
    name = facerec.recognize_face(os.path.join(
        upload_dir,
        "test.png"))
    return not(name == None or name == "None")

