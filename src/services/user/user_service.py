from db.queries.user import get_user_by_login, add_login_history_record
from db.queries.user import create_new_user, get_login_history, does_user_exist
from db.pg_db import db


class LoginAlreadyExists(Exception):
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
