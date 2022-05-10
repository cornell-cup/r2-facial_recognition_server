import os
import cv2
from flask import Blueprint, request, current_app
import numpy as np
from gamlogger import get_default_logger

from ..recognition import prepare, compare_faces
from ..loader import load

logger = get_default_logger(__name__)

face_recognition_bp = Blueprint('face_recognition_bp', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           current_app.config['ALLOWED_EXTENSIONS']


@face_recognition_bp.before_app_first_request
def start_up():
    logger.setLevel(current_app.config.get('LOG_LEVEL'))
    loaded = load(current_app.config.get('CORNELL_CUP_WEBSITE'),
                  loader=current_app.config.get('LOADER'),
                  allow_list=current_app.config.get('ALLOW_LIST')['allowed'])
    for name, (img, _) in loaded.items():
        print(f'Writing {name} to uploads folder.')
        cv2.imwrite(os.path.join(current_app.config.get('UPLOADS_FOLDER'),
                                 f'{name}.jpeg'), img)

    prepare(current_app.config.get('UPLOADS_FOLDER'))
    logger.info('Facial Recognition Server completed startup operation.')


@face_recognition_bp.route('/', methods=['GET'])
def index():
    return 'C1C0 Facial Recognition Server is listening.'


@face_recognition_bp.route('/detect', methods=['GET', 'POST'])
def detect():
    logger.info('Request to detect face received.')
    if request.method == 'POST':
        try:
            shape = request.form.get('shape')
            if shape is None:
                return 'Please include the shape of the image.', 400
            logger.debug('Shape: (%s)', shape)
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
            logger.info('%s identities found!', len(identities))
            matches = list(zip(identities, face_locations))
            logger.debug('Matches found: %s', matches)
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
