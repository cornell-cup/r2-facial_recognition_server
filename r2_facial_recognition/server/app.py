from flask import Flask
from flask_login import LoginManager

try:
    from .models import db, People
    from .views.facial_recognition import face_recognition_bp
    from .views.admin import admin_bp
except ImportError:
    from models import db, People
    from views.facial_recognition import \
        face_recognition_bp
    from views.admin import admin_bp


def create_app():
    app = Flask(__name__)
    # Dual config setup, from config.py for defaults, from file specified by
    #  C1C0_FACEREC_CONFIG for secrets
    app.config.from_pyfile('config.py')
    app.config.from_envvar('C1C0_FACEREC_CONFIG', silent=True)
    db.init_app(app)

    # Login handling for serverside changes and management
    login_manager = LoginManager()
    login_manager.login_view = 'admin_bp.signin'
    login_manager.init_app(app)

    # Initialize database
    with app.app_context():
        db.create_all()

    app.register_blueprint(face_recognition_bp, url_prefix='/face_recognition')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Tells login_manager how to load user with active session
    @login_manager.user_loader
    def load_user(user_id):
        return People.query.get(username=user_id)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
