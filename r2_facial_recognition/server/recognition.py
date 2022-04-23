import os
from typing import Optional, List, Tuple
from face_recognition import (
    load_image_file, face_encodings, face_locations,
    compare_faces as compare_faces_, face_distance
)
import numpy as np

try:
    from .models import db, People

except ImportError:
    from models import db, People

FILE_FOLDER = ''
IMG_EXTs = ['jpg', 'jpeg', 'png']


def prepare(folder: Optional[str] = None, force_reload: bool = False):
    if folder is None:
        folder = FILE_FOLDER
    os.makedirs(folder, exist_ok=True)
    if os.path.isdir(folder):
        for _, _, files in os.walk(folder):
            for file in files:
                print(f'Analyzing file: {file}.')
                ext_idx = file.rindex('.')
                ext = file[ext_idx + 1:]
                if ext in IMG_EXTs:
                    print(f'Image extension matches: {ext}')
                    print(f'{file} was loaded in as a recognized face.')
                    filename = file[:file.rindex('.')]
                    # check_and_add(path, file)
                    first_name, last_name = filename.split('_')
                    people = People.query.filter_by(first_name=first_name,
                                                    last_name=last_name).all()
                    if len(people) == 0:
                        encodings = face_encodings(load_image_file(file))
                        person = People(first_name, last_name, encodings,
                                        admin=False)
                        db.session.add(person)
                    elif len(people) == 1:
                        # One person, replace
                        person = people[0]
                        if person.facial_encoding is None or force_reload:
                            encodings = face_encodings(load_image_file(file))
                            person.facial_encoding = encodings
                    else:
                        # unexpected case, duplicate exists. Not possible
                        print(f'Multiple people named {first_name} {last_name}'
                              f'! What happened here?')
        db.session.commit()


def compare_faces(img: Optional[np.ndarray] = None,
                  encodings: Optional[List[np.ndarray]] = None):
    query = People.query
    print('\n\nPrinting query info:')
    print(query)
    ordered_query = query.order_by(People.id)
    print(ordered_query)
    # all_people = People.query.order_by(People.id.desc()).all()
    all_people = ordered_query
    print(all_people)
    # assoc list
    known_encodings_map = [
        (person.id, person.facial_encoding) for person in all_people
    ]
    # Needs to be list anyway
    known_encodings = [encoding for _, encoding in known_encodings_map]
    if encodings is None:

        try:
            unknown_face_locations = face_locations(img)
        except TypeError as exc:
            raise ValueError('did not pass encodings or an image.') from exc

        encodings = face_encodings(img, unknown_face_locations)
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
            print(f'Face was {distance} away from {person.first_name} '
                  f'{person.last_name}.')
            identities.append(f'{person.first_name}_{person.last_name}')
        else:
            print(f'Unknown face detected! Distance: {distance}')
            identities.append('Unknown')

    return identities, encodings


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
            print(f'Face was {distance} away from {person.first_name} '
                  f'{person.last_name}.')
            identities.append(((person.first_name, person.last_name),
                               encodings[closest_idx],
                               face_distances[closest_idx],
                               locations[closest_idx]))
        else:
            print(f'Unknown face detected! Distance: {distance}')
            identities.append((('Unknown', ''), None, None, None))

    return identities

