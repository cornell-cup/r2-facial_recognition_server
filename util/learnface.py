import hashlib
from util import facerec

import os

def hexify(dirname, filename):
    '''
    Generates a hash from the given image
    '''
    hash_func = hashlib.sha256()
    with open(os.path.join(dirname, filename), "rb") as f:
        hash_func.update(f.read())
    return hash_func.hexdigest()

def face_exists(upload_dir, upload_file):
    '''
    Check if an image with the passed in name exists
    '''
    name = facerec.recognize_face(os.path.join(
        upload_dir,
        upload_file))
    return not(name == None or name == "None")

