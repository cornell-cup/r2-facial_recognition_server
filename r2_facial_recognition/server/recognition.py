import os
from typing import Optional, List, Tuple
from face_recognition import (
    load_image_file, face_encodings, face_locations,
    compare_faces as compare_faces_, face_distance
)
import numpy as np
from gamlogger import get_default_logger

try:
    from .models import db, People
    from .utils import img_from_bytes

except ImportError:
    from models import db, People
    from utils import img_from_bytes

logger = get_default_logger(__name__)

FILE_FOLDER = ''
IMG_EXTs = ['jpg', 'jpeg', 'png']


def prepare(folder: Optional[str] = None, force_reload: bool = False):
    logger.info('Preparing recognition API.')
    if folder is None:
        folder = FILE_FOLDER
    os.makedirs(folder, exist_ok=True)
    if os.path.isdir(folder):
        for _, _, files in os.walk(folder):
            for file in files:
                logger.debug('Processing %s.', file)
                ext_idx = file.rindex('.')
                ext = file[ext_idx + 1:]
                if ext in IMG_EXTs:
                    filename = file[:file.rindex('.')]
                    first_name, last_name = filename.split('_')
                    people = People.query.filter_by(first_name=first_name,
                                                    last_name=last_name).all()
                    if len(people) == 0:
                        # Image should be of a single person, preferably a
                        #  headshot.
                        encodings = face_encodings(load_image_file(
                            os.path.join(folder, file)))[0]
                        person = People(first_name=first_name,
                                        last_name=last_name,
                                        facial_encoding=encodings.tobytes(),
                                        admin=False)
                        db.session.add(person)
                    elif len(people) == 1:
                        # One person, replace
                        person = people[0]
                        if person.facial_encoding is None or force_reload:
                            # Image should be of a single person, preferably a
                            #  headshot.
                            encodings = face_encodings(load_image_file(
                                os.path.join(folder, file)))[0]
                            person.facial_encoding = encodings
                    else:
                        # unexpected case, duplicate exists. Not possible
                        print(f'Multiple people named {first_name} {last_name}'
                              f'! What happened here?')
        db.session.commit()
    logger.info('Recognition API prepared.')


def compare_faces(img: Optional[np.ndarray] = None,
                  encodings: Optional[List[np.ndarray]] = None,
                  gen_face_locations: bool = False):
    logger.info('Comparing face.')
    all_people = People.query.order_by(People.id.desc()).all()
    print([person.first_name for person in all_people])
    # assoc list
    known_encodings_map = [
        (person.id, person.facial_encoding) for person in all_people
    ]
    # Needs to be list anyway
    known_encodings = [np.frombuffer(encoding) for _, encoding in
                       known_encodings_map]

    unknown_face_locations = []
    if encodings is None or gen_face_locations:
        try:
            unknown_face_locations = face_locations(img)
        except TypeError as exc:
            raise ValueError('did not pass encodings or an image.') from exc
    if encodings is None:
        encodings = face_encodings(img, unknown_face_locations)

    identities = []

    for unknown_face in encodings:
        matches = compare_faces_(known_encodings, unknown_face)
        face_distances = face_distance(known_encodings, unknown_face)
        closest_idx = np.argmin(face_distances)
        # distance = face_distances[closest_idx]
        if matches[closest_idx]:
            # Cross-referencing the index is necessary in case the primary
            #  key gets out of sync, for example, by deleting an element.
            person_id = known_encodings_map[closest_idx][0]
            person = People.query.get(person_id)
            identities.append(f'{person.first_name}_{person.last_name}')
        else:
            identities.append('Unknown')
    return identities, encodings, unknown_face_locations


def full_identification(img: Optional[np.ndarray] = None,
                        encodings: Optional[List[np.ndarray]] = None,
                        locations: Optional[List[np.ndarray]] = None) -> \
        List[Tuple[Tuple[str, str], Optional[np.ndarray], Optional[np.ndarray],
                   Optional[Tuple[int, int, int, int]]]]:

    all_people = People.query.order_by(People.id).all()
    # assoc list
    known_encodings_map = [
        (person.id, person.facial_encoding) for person in all_people
    ]
    # Needs to be list anyway
    known_encodings = [encoding for _, encoding in known_encodings_map]

    if locations is None:
        locations = face_locations(img)
    if encodings is None:
        encodings = face_encodings(img, locations)

    identities = []
    for unknown_face in encodings:
        matches = compare_faces_(known_encodings, unknown_face)
        face_distances = face_distance(known_encodings, unknown_face)
        closest_idx = np.argmin(face_distances)
        distance = face_distances[closest_idx]
        if matches[closest_idx]:
            # Cross-referencing the index is necessary in case the primary
            #  key gets out of sync, for example, by deleting an element.
            person_id = known_encodings_map[closest_idx][0]
            person = People.query.get(person_id)
            identities.append(((person.first_name, person.last_name),
                               encodings[closest_idx],
                               face_distances[closest_idx],
                               locations[closest_idx]))
        else:
            identities.append((('Unknown', ''), None, None, None))

    return identities

