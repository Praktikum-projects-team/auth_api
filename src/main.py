from flask import Flask

from core import config
from db.pg_db import init_db, db
from dotenv import load_dotenv

from api.v1.users import users

load_dotenv()

app_config = config.AppConfig()
postgres_config = config.PostgresConfig()
redis_config = config.RedisConfig()

app = Flask(__name__)
init_db(app=app)

with app.app_context():
    from db import models

    db.create_all()

app.register_blueprint(users, url_prefix='/api/v1/user')


@app.route('/api/hello-world')
def hello_world():
    from db.models import User
    admin = User(login='admin', password='password')
    db.session.add(admin)
    db.session.commit()
    user = User.query.filter_by(login='admin').first()
    return str(user.id)


# @app.route('/api/user/profile')
# def get_user_info():
#     return f"User"


if __name__ == '__main__':
    app.run()
