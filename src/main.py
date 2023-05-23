from flask import Flask

from core import config
from create_superuser import createsuperuser
from db.pg_db import init_db, db

app_config = config.AppConfig()
postgres_config = config.PostgresConfig()
redis_config = config.RedisConfig()


app = Flask(__name__)
init_db(app=app)

with app.app_context():
    from db import models
    db.create_all()

with app.app_context():
    createsuperuser()


@app.route('/api/hello-world')
def hello_world():
    from db.models import User
    admin = User(login='admin', password='password')
    db.session.add(admin)
    db.session.commit()
    user = User.query.filter_by(login='admin').first()
    return str(user.id)


if __name__ == '__main__':
    app.run()
