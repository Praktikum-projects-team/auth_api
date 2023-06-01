from db.queries.user import (
    get_user_by_login,
    add_login_history_record,
    create_new_user,
    get_login_history,
    does_user_exist,
    user_admin_all,
    get_user_by_id,
    admin_update_user,
    admin_update_user_roles
)
from db.pg_db import db
from services.role.role_service import get_role_by_name, RoleNotFound
from uuid import UUID
from sqlalchemy.exc import DataError


class LoginAlreadyExists(Exception):
    ...


class UserNotFound(Exception):
    ...


def user_get_data(login: str):
    return get_user_by_login(login)


def user_login_history(login: str, page: int, page_size: int):
    user_id = get_user_by_login(login).id
    return get_login_history(user_id, page, page_size)


def user_update(login: str, new_data: dict):
    user = get_user_by_login(login)
    user.name = new_data['name']
    db.session.commit()


def user_change_login(login: str, new_data: dict):
    user = get_user_by_login(login)
    login_exists = does_user_exist(new_data['new_login'])
    if login_exists:
        raise LoginAlreadyExists("Login already exist")
    user.login = new_data['new_login']
    db.session.commit()


def get_user_admin_info():
    return user_admin_all()


def get_user_info(user_id: UUID):
    user = get_user_by_id(user_id)
    if not user:
        raise UserNotFound("User not found")
    return user


def update_user_admin(user_id: UUID, body: dict):
    try:
        user = get_user_info(user_id)
    except (UserNotFound, ValueError, DataError):
        raise
    user = admin_update_user(user, body['is_superuser'])
    for role_name in body['roles']:
        try:
            role = get_role_by_name(role_name)
        except RoleNotFound:
            raise
        admin_update_user_roles(user, role)
    db.session.commit()


