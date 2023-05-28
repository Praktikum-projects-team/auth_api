import logging
from http import HTTPStatus
from typing import Any

import requests
from psycopg2 import DataError
from pydantic import BaseModel

from tests.functional.testdata.user import get_user_data
from tests.functional.utils.routes import AUTH_URL, ROLES_URL


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


class ApiResponse(BaseModel):
    status: HTTPStatus
    body: Any


def make_request(method: str, url: str, url_params: dict = None, body: dict = None) -> ApiResponse:
    resp = getattr(requests, method)(url, params=url_params, json=body)

    return ApiResponse(status=resp.status_code, body=resp.json())


def make_get_request(url: str, url_params: dict = None):
    return make_request(method="get", url=url, url_params=url_params)


def make_post_request(url: str, url_params: dict = None, body: dict = None):
    return make_request(method="post", url=url, url_params=url_params, body=body)


def make_put_request(url: str, url_params: dict = None, body: dict = None):
    return make_request(method="put", url=url, url_params=url_params, body=body)


def make_delete_request(url: str, url_params: dict = None):
    return make_request(method="delete", url=url, url_params=url_params)


def create_user():
    user_data = get_user_data()
    make_post_request(AUTH_URL, body={
        'login': user_data['login'],
        'name': user_data['name'],
        'password': user_data['password']
    })

    return user_data


def create_role(role_name: str):
    role_exists = make_get_request(ROLES_URL)
    if role_name not in role_exists.body:
        make_post_request(ROLES_URL, body={'name': role_name})
