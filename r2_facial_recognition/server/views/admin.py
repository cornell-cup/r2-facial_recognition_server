from flask import Blueprint, request
from flask_login import login_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import escape
import numpy as np
from gamlogger import get_default_logger

from ..models import People, db
from ..config import LOG_LEVEL

logger = get_default_logger(__name__)
logger.setLevel(LOG_LEVEL)

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/')
def index():
    return ''


@admin_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = escape(request.form.get('username'))
        password = escape(request.form.get('password'))
        logger.debug('Got a request to signin user. (%s)', username)
        remember = True if request.form.get('remember') else False
        person = People.query.filter_by(
            username=username).first()
        pass_hash_check = check_password_hash(person.password, password)
        if not person or not pass_hash_check:
            logger.debug('User not found or credentials didn\'t match. Bools: '
                         '%s, %s', not person, pass_hash_check)
            return 'Your credentials do not match. Please contact the ' \
                   'admins.', 401
        login_user(person, remember=remember)
        logger.debug('%s successfully logged in.', username)
        return 'Login successful.'
    else:
        # Later make HTML page for login maybe
        logger.error('Got a GET request- not yet implemented.')
        return 'Unsupported', 405


@admin_bp.route('/signup', methods=['GET', 'POST'])
# @login_required
def signup():
    if request.method == 'POST':
        if not current_user.admin:
            return 'You do not have permission to create new users.', 405
        username = escape(request.form.get('username'))
        password = generate_password_hash(escape(request.form.get('password')))
        logger.debug('Got a request to signup user. (%s)', username)
        first_name = escape(request.form.get('first_name'))
        last_name = escape(request.form.get('last_name'))
        facial_encoding = request.files.get('facial_encoding')
        if facial_encoding is not None:
            logger.debug('Decoding buffer.')
            facial_encoding = np.frombuffer(facial_encoding.stream.read(),
                                            dtype=np.uint8)
            logger.debug('Buffer decoded.')
        admin = bool(escape(request.form.get('admin')).lower())
        person = People.query.filter_by(username=username).first()
        if person is None:
            logger.info('%s does not exist, creating new user.', username)
            person = People(first_name=first_name, last_name=last_name,
                            facial_encoding=facial_encoding, username=username,
                            password=password, admin=admin)
            db.session.add(person)
            logger.info('%s successfully created.', username)

        person.username = username if username is not None else person.username
        person.password = password if password is not None else person.password
        person.first_name = first_name if first_name is not None else \
            person.first_name
        person.last_name = last_name if last_name is not None else \
            person.last_name
        person.facial_encoding = facial_encoding if \
            facial_encoding is not None else person.facial_encoding
        db.session.commit()
        logger.debug('Changes for %s committed.', person.username)
        return 'User created.'
    else:
        return 'GET version of signup not set up set.', 501
