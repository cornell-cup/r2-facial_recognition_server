import os
import json
from logging import INFO

UPLOADS_FOLDER = 'uploads'

# sqlite in memory, for now.
SQLALCHEMY_DATABASE_URI = 'sqlite:///facial_recognition.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_EXTENSIONS = [
    'jpg', 'jpeg', 'png'
]

PROCESSORS = 12

SECRET_FILENAME = '.secret'

ALLOW_LIST_FILENAME = '.allowlist.json'

LOG_LEVEL = INFO

CORNELL_CUP_WEBSITE = 'https://cornellcuprobotics.com/members.html'
LOADER = 'cornellcup_loader'


def __init_file(filename, global_val, data, read_fun=lambda x: x):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            globals()[global_val] = read_fun(f.read())
    else:
        globals()[global_val] = str(data())
        with open(filename, 'w') as f:
            f.write(globals()[global_val])


__init_file(SECRET_FILENAME, 'SECRET_KEY', lambda: os.urandom(256).hex())

__init_file(ALLOW_LIST_FILENAME, 'ALLOW_LIST', lambda: json.dumps({'allowed': []},
                                                              sort_keys=True,
                                                              indent=4),
            read_fun=json.loads)


del __init_file
del os
del json
del INFO
