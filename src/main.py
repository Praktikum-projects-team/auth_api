from flask import Flask

from api.v1.role import roles
from core import config
from db.pg_db import db, init_db

app_config = config.AppConfig()
postgres_config = config.PostgresConfig()
redis_config = config.RedisConfig()


app = Flask(__name__)
app.register_blueprint(roles, url_prefix="/api/v1/admin/roles")
init_db(app=app)

with app.app_context():
    db.create_all()


@app.route('/api/hello-world')
def hello_world():
    # from db.models import User
    # admin = User(login='admin', password='password')
    # db.session.add(admin)
    # db.session.commit()
    # user = User.query.filter_by(login='admin').first()
    # return str(user.id)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
