import argparse

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from constants import RoleName
from core.config import PostgresConfig
from db.models import Role, User, UserRole

parser = argparse.ArgumentParser(description='Create superuser')
parser.add_argument('login', type=str, help='Superuser login')
parser.add_argument('password', type=str, help='Superuser password')

args = parser.parse_args()

db = SQLAlchemy()
pg_conf = PostgresConfig()
pg_dsn = f'postgresql://{pg_conf.user}:{pg_conf.password}@{pg_conf.host_local}:{pg_conf.port}/{pg_conf.database}'


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = pg_dsn
    db.init_app(app)


app = Flask(__name__)
init_db(app=app)


def createsuperuser(login, password):
    user_exist = db.session.query(User).filter(User.login == login).first()
    if user_exist:
        return "Superuser already exist"

    superuser = User(login=login, password=password, is_superuser=True)
    db.session.add(superuser)
    db.session.commit()

    role_exist = db.session.query(Role).filter(Role.name == RoleName.ADMIN).first()
    if not role_exist:
        role = Role(name=RoleName.ADMIN)
        db.session.add(role)
        db.session.commit()

    role_id = db.session.query(Role.id).filter_by(name=RoleName.ADMIN).scalar()

    user_role = UserRole(user_id=superuser.id, role_id=role_id)
    db.session.add(user_role)
    db.session.commit()
    return "Superuser successfully created"


if __name__ == '__main__':
    with app.app_context():
        createsuperuser(args.login, args.password)
