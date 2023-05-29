import logging
from http import HTTPStatus
from typing import Any

import requests
from psycopg2 import DataError
from pydantic import BaseModel

from tests.functional.testdata.user import get_user_data
from tests.functional.utils.constants import AdminData
from tests.functional.utils.routes import ADMIN_USER_URL, AUTH_URL_LOGIN, AUTH_URL_SIGN_UP, ROLES_URL


def insert_data(pg_conn, table_name, data):
    cursor = pg_conn.cursor()
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

    try:
        cursor.execute(query, tuple(data.values()))
        pg_conn.commit()
        logging.info(f"Success to insert data into {table_name}")
    except DataError as e:
        pg_conn.rollback()
        logging.error(f"Failed to insert data into {table_name}")
        raise e
    finally:
        cursor.close()


def get_access_token(login: str, password: str) -> str:
    resp = requests.post(AUTH_URL_LOGIN, json={
        'login': login,
        'password': password
    })
    resp_data = resp.json()
    if resp.status_code != HTTPStatus.OK:
        raise Exception(resp_data['message'])

    return resp_data['access_token']


ADMIN_ACCESS_TOKEN = get_access_token(AdminData.LOGIN, AdminData.PASSWORD)


class ApiResponse(BaseModel):
    status: HTTPStatus
    body: Any


def make_request(method: str, url: str, url_params: dict = None, body: dict = None) -> ApiResponse:
    headers = {'Authorization': f'Bearer {ADMIN_ACCESS_TOKEN}'}
    resp = getattr(requests, method)(url, params=url_params, json=body, headers=headers)

    return ApiResponse(status=resp.status_code, body=resp.json())


def make_get_request(url: str, url_params: dict = None):
    return make_request(method="get", url=url, url_params=url_params)


def make_post_request(url: str, url_params: dict = None, body: dict = None):
    return make_request(method="post", url=url, url_params=url_params, body=body)


def make_put_request(url: str, url_params: dict = None, body: dict = None):
    return make_request(method="put", url=url, url_params=url_params, body=body)


def make_delete_request(url: str, url_params: dict = None):
    return make_request(method="delete", url=url, url_params=url_params)


def get_user_id_by_login(login: str) -> int:
    users = make_get_request(ADMIN_USER_URL)
    for user in users.body:
        if user['login'] == login:
            return user['id']


def create_user():
    user_data = get_user_data()
    make_post_request(AUTH_URL_SIGN_UP, body={
        'login': user_data['login'],
        'name': user_data['name'],
        'password': user_data['password']
    })

    return user_data


def create_role(role_name: str):
    role = make_get_request(ROLES_URL)
    if role_name not in role.body:
        make_post_request(ROLES_URL, body={'name': role_name})
