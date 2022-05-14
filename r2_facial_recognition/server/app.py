from flask import Flask
from flask_login import LoginManager
from gamlogger import get_default_logger
import cv2
import os

from .models import db, People
from .views.facial_recognition import face_recognition_bp
from .views.admin import admin_bp
from .config import LOG_LEVEL
from .recognition import prepare
from .loader import load


logger = get_default_logger(__name__)
logger.setLevel(LOG_LEVEL)


def create_app():
    logger.info('Serving the Facial Recognition app.')
    app = Flask(__name__)
    # Dual config setup, from config.py for defaults, from file specified by
    #  C1C0_FACEREC_CONFIG for secrets
    logger.debug('Loading config.')
    app.config.from_pyfile('config.py')
    app.config.from_envvar('C1C0_FACEREC_CONFIG', silent=True)
    logger.debug('Initializing database.')
    db.init_app(app)

    logger.debug('Setting up authentication.')
    # Login handling for serverside changes and management
    login_manager = LoginManager()
    login_manager.login_view = 'admin_bp.signin'
    login_manager.init_app(app)

    logger.debug('Initializing tables in database')
    # Initialize database
    with app.app_context():
        db.create_all()

    logger.debug('Registering blueprints.')
    app.register_blueprint(face_recognition_bp, url_prefix='/face_recognition')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Tells login_manager how to load user with active session
    @login_manager.user_loader
    def load_user(user_id):
        return People.query.get(username=user_id)

    # Scrape users if in allow-list.
    loaded = load(app.config.get('CORNELL_CUP_WEBSITE'),
                  loader=app.config.get('LOADER'),
                  allow_list=app.config.get('ALLOW_LIST')['allowed'])
    for name, (img, _) in loaded.items():
        print(f'Writing {name} to uploads folder.')
        cv2.imwrite(os.path.join(app.config.get('UPLOADS_FOLDER'),
                                 f'{name}.jpeg'), img)
    with app.app_context():
        prepare(app.config.get('UPLOADS_FOLDER'))

    logger.info('Facial Recognition app created.')
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
