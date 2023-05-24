from flask import Flask
from flask_marshmallow import Marshmallow

from api.v1.role import roles
from db.pg_db import db, init_db


def create_app():
    app = Flask(__name__)
    init_db(app=app)
    ma = Marshmallow(app)

    app.register_blueprint(roles, url_prefix="/api/v1/admin/roles")

    with app.app_context():
        db.create_all()

    return app
