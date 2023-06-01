from uuid import UUID

from constants import RoleName
from db.models import Role, User, LoginHistory
from db.pg_db import db


def get_user_by_login(login: str):
    return User.query.filter_by(login=login).first()


def does_user_exist(login: str):
    return db.session.query(User.query.filter_by(login=login).exists()).scalar()


def create_new_user(user):
    role = db.session.query(Role).filter(Role.name == RoleName.USER).first()
    new_user = User(**user, roles=[role])
    db.session.add(new_user)
    db.session.commit()


def add_login_history_record(user_id: UUID, user_agent: str):
    record = LoginHistory(user_id=user_id, user_agent=user_agent)
    db.session.add(record)
    db.session.commit()
