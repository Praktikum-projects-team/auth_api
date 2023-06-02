from uuid import UUID

from constants import RoleName
from db.models import Role, User, LoginHistory, UserRole
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


def get_login_history(user_id: UUID, page: int, page_size: int):
    user_login_history = LoginHistory.query.filter_by(user_id=user_id).paginate(page=page, per_page=page_size)
    return user_login_history


def user_admin_all():
    return User.query.all()


def get_user_by_id(user_id: UUID):
    return User.query.filter_by(id=user_id).first()


def admin_update_user(user, is_superuser: bool):
    user.is_superuser = is_superuser
    user.roles = []
    return user


def admin_update_user_roles(user, role):
    user_role = UserRole(user_id=user.id, role_id=role.id)
    db.session.add(user_role)
