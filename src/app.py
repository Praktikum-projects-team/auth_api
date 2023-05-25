from flask import Flask

from api.v1.models.marshmallow_init import init_marshmallow
from api.v1.role import roles
from api.v1.auth import auth_bp
from core.config import app_config
from db.pg_db import init_db, db
from services.auth.jwt_init import init_jwt


def register_blueprints(app):
    API_V1_PATH = '/api/v1'
    app.register_blueprint(auth_bp, url_prefix=API_V1_PATH + '/auth')
    app.register_blueprint(roles, url_prefix="/admin/roles")


def init_extensions(app):
    init_jwt(app=app)
    init_db(app=app)
    init_marshmallow(app=app)


def create_app():
    app = Flask(__name__)

    app.config.from_object(app_config)
    init_extensions(app)
    register_blueprints(app)

    with app.app_context():
        from db import models
        db.create_all()

    return app



