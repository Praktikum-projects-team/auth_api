from flask import Flask
from flask_jwt_extended import JWTManager


from api.v1.auth import auth_bp
from core import config
from db.pg_db import init_db, db

app_config = config.AppConfig()
postgres_config = config.PostgresConfig()
redis_config = config.RedisConfig()


app = Flask(__name__)
app.config.from_object(app_config)
jwt = JWTManager(app)

init_db(app=app)

API_V1_PATH = '/api/v1'
app.register_blueprint(auth_bp, url_prefix=API_V1_PATH + '/auth')


with app.app_context():
    from db import models
    db.create_all()


@app.route('/api/hello-world')
def hello_world():
    from db.models import User
    admin = User(login='admin1', password=hash_password('password'))
    db.session.add(admin)
    db.session.commit()
    user = User.query.filter_by(login='admin').first()
    return str(user.id)


if __name__ == '__main__':
    app.run()
