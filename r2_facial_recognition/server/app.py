from flask import Flask

try:
    from .models import db
    from .views.facial_recognition import face_recognition_bp
except ImportError:
    from r2_facial_recognition.server.models import db
    from r2_facial_recognition.server.views.facial_recognition import \
        face_recognition_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.from_envvar('C1C0_FACEREC_CONFIG', silent=True)
    db.init_app(app)
    with app.app_context():
        # print(dir(db.metadata))
        print(list(db.metadata.tables.keys()))
        db.create_all()
        print(db.metadata.tables.values())
    app.register_blueprint(face_recognition_bp, url_prefix='/face_recognition')
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
