import logging
import uuid
from datetime import datetime
from http import HTTPStatus

import pytest
import requests
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from tests.functional.utils.constants import AdminData, RoleName, UserData
from tests.functional.utils.helpers import create_user
from tests.functional.utils.routes import AUTH_URL_LOGIN, AUTH_URL_SIGN_UP


@pytest.fixture(scope="session", autouse=True)
def create_admin_default(pg_conn):
    user_id = str(uuid.uuid4())
    hashed_password = pbkdf2_sha256.hash(AdminData.PASSWORD)

    with pg_conn.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE login = %s)", (AdminData.LOGIN,))
        user = cursor.fetchone()[0]
    if user:
        logging.warning("Admin already exist")
        return

    # Создаем админа для тесовой сессии, если он не был создан
    with pg_conn.cursor() as cursor:
        created_at = datetime.utcnow()
        cursor.execute(
            "INSERT INTO users (id, login, password, is_superuser, created_at)"
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, AdminData.LOGIN, hashed_password, True, created_at)
        )
        pg_conn.commit()

    # Получаем id роли администратора
    with pg_conn.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM roles WHERE name = %s", (RoleName.ADMIN,)
        )
        role_id = cursor.fetchone()

    # Привязываем роль администратора к созданному админу
    with pg_conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_roles (user_id, role_id, given_at)"
            "VALUES (%s, %s, %s)",
            (user_id, role_id, datetime.utcnow())
        )
        pg_conn.commit()

    pg_conn.close()

    logging.info("Admin successfully created")


@pytest.fixture(scope="session", autouse=True)
def create_user_default():
    requests.post(AUTH_URL_SIGN_UP, json={
        'login': UserData.LOGIN,
        'password': UserData.PASSWORD,
        'name': UserData.NAME
    })
    logging.info("User successfully created")


@pytest.fixture(scope="session")
def access_token_admin():
    resp = requests.post(AUTH_URL_LOGIN, json={
        'login': AdminData.LOGIN,
        'password': AdminData.PASSWORD
    })
    resp_data = resp.json()
    if resp.status_code != HTTPStatus.OK:
        raise Exception(resp_data['message'])

    return resp_data['access_token']


@pytest.fixture(scope="session")
def access_token_user():
    resp = requests.post(AUTH_URL_LOGIN, json={
        'login': UserData.LOGIN,
        'password': UserData.PASSWORD
    })
    resp_data = resp.json()
    if resp.status_code != HTTPStatus.OK:
        raise Exception(resp_data['message'])

    return resp_data['access_token']


@pytest.fixture()
def user_data_with_access_token():
    user_data = create_user()
    resp = requests.post(AUTH_URL_LOGIN, json={'login': user_data['login'], 'password': user_data['password']})
    resp_data = resp.json()
    if resp.status_code != HTTPStatus.OK:
        raise Exception(resp_data['message'])

    return {'access_token': resp_data['access_token'], 'user_data': user_data}
