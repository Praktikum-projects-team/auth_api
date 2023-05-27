from flask import Flask

from dotenv import load_dotenv

from api.v1.users import users_bp
from api.v1.auth import auth_bp
from core.config import app_config
from db.pg_db import init_db, db
from services.auth.jwt_init import init_jwt

app = Flask(__name__)
app.config.from_object(app_config)

init_jwt(app=app)
init_db(app=app)

API_V1_PATH = '/api/v1'
app.register_blueprint(auth_bp, url_prefix=API_V1_PATH + '/auth')
app.register_blueprint(users_bp, url_prefix=API_V1_PATH + '/user')

with app.app_context():
    from db import models

    db.create_all()

if __name__ == '__main__':
    app.run()
