import cv2
from flask import Blueprint, request, current_app
import numpy as np

try:
    from ..recognition import prepare, compare_faces
except ImportError:
    from r2_facial_recognition.server.recognition import prepare, compare_faces


face_recognition_bp = Blueprint('face_recognition_bp', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           current_app.config['ALLOWED_EXTENSIONS']


@face_recognition_bp.before_app_first_request
def start_up():
    print(current_app.config.get('UPLOADS_FOLDER'))
    prepare(current_app.config.get('UPLOADS_FOLDER'))
    print('Facial Recognition Server completed startup operation.')


@face_recognition_bp.route('/', methods=['GET'])
def index():
    return 'C1C0 Facial Recognition Server is listening.'


@face_recognition_bp.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        try:
            # print(request.files)
            shape = eval(request.form.get('shape'))
            filenames = list(request.files.keys())
            # print(list(filenames))
            # print(dir(request.files['image']))
            data = np.frombuffer(request.files['image'].stream.read(),
                                 dtype=np.uint8)

            print(f'type(data)={type(data)}')
            print(f'data={data}')
            print(f'data.shape={data.shape}')
            print(f'shape={shape}')
            unknown_img = np.reshape(data, tuple(shape)) if 'image' in filenames else None
            unknown_img = cv2.cvtColor(unknown_img, cv2.COLOR_RGB2BGR)
            cv2.imwrite('test.jpeg', unknown_img)
            unknown_encodings = np.frombuffer(request.files['encoding']) \
                if 'encoding' in filenames else None
            # print(unknown_img)
            # print(unknown_encodings)
            compare_faces(unknown_img, unknown_encodings)
        except ValueError as exc:
            if current_app.config['DEBUG']:
                raise exc
            return '400 - Bad request', 400

    elif request.method == 'GET':
        # TODO: Implement me, check args and grab base64
        return '405 - Method Not Allowed', 405
