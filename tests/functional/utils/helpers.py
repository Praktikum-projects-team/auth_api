import logging
from http import HTTPStatus
from typing import Any

import requests
from psycopg2 import DataError
from pydantic import BaseModel
from tests.functional.utils.routes import AUTH_URL_LOGIN, AUTH_URL_SIGN_UP
from tests.functional.utils.constants import UserData
from tests.functional.testdata.user import get_user_sign_up_data, get_user_login_data


def insert_data(postgres_conn, table_name, data):
    cursor = postgres_conn.cursor()
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

    try:
        cursor.execute(query, tuple(data.values()))
        postgres_conn.commit()
        logging.info(f"Success to insert data into {table_name}")
    except DataError as e:
        postgres_conn.rollback()
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


def get_user_token():
    return get_access_token(UserData.LOGIN, UserData.PASSWORD)


class ApiResponse(BaseModel):
    status: HTTPStatus
    body: Any


def make_request(method: str, url: str, url_params: dict = None, body: dict = None,
                 access_token: str = None) -> ApiResponse:

    headers = {'Authorization': f'Bearer {access_token}'}
    resp = getattr(requests, method)(url, params=url_params, json=body, headers=headers)
    return ApiResponse(status=resp.status_code, body=resp.json())


def make_get_request(url: str, url_params: dict = None, access_token: str = None):
    return make_request(method="get", url=url, url_params=url_params, access_token=access_token)


def make_post_request(url: str, url_params: dict = None, body: dict = None, access_token: str = None):
    return make_request(method="post", url=url, url_params=url_params, body=body, access_token=access_token)


def make_put_request(url: str, url_params: dict = None, body: dict = None, access_token: str = None):
    return make_request(method="put", url=url, url_params=url_params, body=body, access_token=access_token)


def make_delete_request(url: str, url_params: dict = None, access_token: str = None):
    return make_request(method="delete", url=url, url_params=url_params, access_token=access_token)


def sign_up_user():
    user_data = get_user_sign_up_data()
    make_post_request(AUTH_URL_SIGN_UP, body={
        'login': user_data['login'],
        'name': user_data['name'],
        'password': user_data['password']
    })