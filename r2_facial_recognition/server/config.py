import os
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

LOG_LEVEL = INFO

if os.path.exists(SECRET_FILENAME):
    with open('.secret', 'r') as f:
        SECRET_KEY = f.read()
else:
    SECRET_KEY = os.urandom(256).hex()
    with open('.secret', 'w') as f:
        f.write(SECRET_KEY)
