import cv2
from flask import Blueprint, request, current_app
import numpy as np
from gamlogger import get_default_logger

from ..recognition import prepare, compare_faces

logger = get_default_logger(__name__)

face_recognition_bp = Blueprint('face_recognition_bp', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           current_app.config['ALLOWED_EXTENSIONS']


@face_recognition_bp.before_app_first_request
def start_up():
    prepare(current_app.config.get('UPLOADS_FOLDER'))
    logger.info('Facial Recognition Server completed startup operation.')


@face_recognition_bp.route('/', methods=['GET'])
def index():
    return 'C1C0 Facial Recognition Server is listening.'


@face_recognition_bp.route('/detect', methods=['GET', 'POST'])
def detect():
    logger.debug('Request to detect face received.')
    if request.method == 'POST':
        try:
            shape = request.form.get('shape')
            if shape is None:
                return 'Please include the shape of the image.', 400
            print(shape)
            shape = eval(shape)
            filenames = list(request.files.keys())
            # Image in BGR format
            data = np.frombuffer(request.files['image'].stream.read(),
                                 dtype=np.uint8)
            unknown_img = np.reshape(data, tuple(shape)) if 'image' in \
                                                            filenames else None
            unknown_encodings = np.frombuffer(request.files['encoding']) \
                if 'encoding' in filenames else None
            identities, encodings, face_locations = compare_faces(
                unknown_img, unknown_encodings)
            logger.debug('%s identities found!', len(identities))
            matches = list(zip(identities, face_locations))
            print(matches)
            return {
                'matches': matches,
                'face_locations': []
            }
        except ValueError as exc:
            logger.debug('Got a ValueError: %s', exc.args)
            if current_app.config['DEBUG']:
                raise exc
            return '400 - Bad request', 400

    elif request.method == 'GET':
        # TODO: Implement me, check args and grab base64
        return '405 - Method Not Allowed', 405
