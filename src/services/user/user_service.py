from flask import current_app
from flask_sqlalchemy.pagination import Pagination

from db.queries.user import (
    get_user_by_login,
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
    history = get_login_history(user_id, page, page_size)
    return get_paginated(history)


def get_paginated(paginated_obj: Pagination):
    return {
        'results': paginated_obj.items,
        'pagination': {
            'page': paginated_obj.page,
            'per_page': paginated_obj.per_page,
            'pages_total': paginated_obj.pages
        }
    }


def user_update(login: str, new_data: dict):
    user = get_user_by_login(login)
    user.name = new_data['name']

    db.session.commit()
    current_app.logger.info('User in db %s updated successfully', login)


def user_change_login(login: str, new_data: dict):
    user = get_user_by_login(login)
    login_exists = does_user_exist(new_data['new_login'])
    if login_exists:
        raise LoginAlreadyExists('Login already exist')
    user.login = new_data['new_login']

    db.session.commit()
    current_app.logger.info('User login in db %s updated successfully', login)


def get_user_admin_info():
    return user_admin_all()


def get_user_info(user_id: UUID):
    user = get_user_by_id(user_id)
    if not user:
        raise UserNotFound('User not found')
    current_app.logger.info('User in db %s found', user_id)

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
    logging.info('User in db %s updated successfully', user_id)
