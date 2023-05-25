from flask_jwt_extended import JWTManager
from main import app


jwt = JWTManager(app)


def init_jwt(app):
    jwt.init_app(app)
