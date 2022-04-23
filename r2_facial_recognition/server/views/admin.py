from flask import Blueprint, request
from flask_login import login_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import escape
import numpy as np
from ..models import People, db

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/')
def index():
    return ''


@admin_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = escape(request.form.get('username'))
        password = escape(request.form.get('password'))
        remember = True if request.form.get('remember') else False
        person = People.query.filter_by(
            username=username).first()
        if not person or not check_password_hash(person.password, password):
            return 'Your credentials do not match. Please contact the ' \
                   'admins.', 401
        login_user(person, remember=remember)
        return 'Login successful.'
    else:
        # Later make HTML page for login maybe
        return 'Unsupported', 405


@admin_bp.route('/signup', methods=['GET', 'POST'])
# @login_required
def signup():
    if request.method == 'POST':
        # if not current_user.admin:
        #     return 'You do not have permission to create new users.', 405
        username = escape(request.form.get('username'))
        password = generate_password_hash(escape(request.form.get('password')))
        first_name = escape(request.form.get('first_name'))
        last_name = escape(request.form.get('last_name'))
        facial_encoding = request.files.get('facial_encoding')
        if facial_encoding is not None:
            facial_encoding = np.frombuffer(facial_encoding.stream.read(),
                                            dtype=np.uint8)
        # admin = bool(escape(request.form.get('admin')).lower())
        admin = True
        person = People.query.filter_by(username=username).first()
        if person is None:
            person = People(first_name=first_name, last_name=last_name,
                            facial_encoding=facial_encoding, username=username,
                            password=password, admin=admin)
            db.session.add(person)

        person.username = username if username is not None else person.username
        person.password = password if password is not None else person.password
        person.first_name = first_name if first_name is not None else \
            person.first_name
        person.last_name = last_name if last_name is not None else \
            person.last_name
        person.facial_encoding = facial_encoding if \
            facial_encoding is not None else person.facial_encoding
        db.session.commit()
        return 'User created.'
    else:
        return 'GET version of signup not set up set.', 501
