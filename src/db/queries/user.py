from uuid import UUID

from constants import RoleName
from db.models import Role, User, LoginHistory, UserRole
from db.pg_db import db


def get_user_by_login(login: str):
    return User.query.filter_by(login=login).first()


def does_user_exist(login: str):
    return db.session.query(User.query.filter_by(login=login).exists()).scalar()


def create_new_user(user):
    # Вносим пользователя в базу
    new_user = User(**user)
    db.session.add(new_user)

    # Создаем роль, если она не существует
    role_exist = db.session.query(Role).filter(Role.name == RoleName.USER).first()
    if not role_exist:
        new_role = Role(name=RoleName.USER)
        db.session.add(new_role)

    # Получаем id роли
    role_data = db.session.query(Role).filter(Role.name == RoleName.USER).first()
    role_id = role_data.id

    # Получаем id пользователя
    user_data = User.query.filter_by(login=user["login"]).first()
    user_id = user_data.id

    # Привязываем пользователю роль
    new_user_role = UserRole(user_id=user_id, role_id=role_id)
    db.session.add(new_user_role)

    db.session.commit()


def add_login_history_record(user_id: UUID, user_agent: str):
    record = LoginHistory(user_id=user_id, user_agent=user_agent)
    db.session.add(record)
    db.session.commit()
