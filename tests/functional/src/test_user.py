from http import HTTPStatus

import pytest

from tests.functional.testdata.user import get_user_sign_up_data
from tests.functional.utils.helpers import (
    make_delete_request,
    make_get_request,
    make_post_request,
    make_put_request,
    sign_up_user,
    get_user_token
)
from tests.functional.utils.routes import USER_URL


class TestUser:

    def test_user_info(self, access_token_user):
        sign_up_user()
        resp = make_get_request(USER_URL, access_token=access_token_user)
        expected_fields = ['name', 'login', 'created_at']
        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in expected_fields:
            assert field in resp.body[0], f'No {field} in resp'

    def test_user_change_info(self, access_token_user):
        sign_up_user()
        resp_put = make_put_request(USER_URL, body={'name': "newname"}, access_token=access_token_user)
        resp = make_get_request(USER_URL, access_token=access_token_user)
        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['name'] == "newname", 'Incorrect name after changing'

    def test_user_login_history(self, access_token_user):
        sign_up_user()
        resp = make_get_request(f'{USER_URL}/login_history', access_token=access_token_user)
        expected_fields = ['user_id', 'user_agent', 'auth_datetime']
        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in expected_fields:
            assert field in resp.body[0], f'No {field} in resp'

    def test_user_change_login(self, access_token_user):
        sign_up_user()
        resp_put = make_put_request(USER_URL, body={'new_login': "newuserlogin@user.ru"}, access_token=access_token_user)
        resp = make_get_request(USER_URL, access_token=access_token_user)
        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'

    def test_user_change_password(self, access_token_user):
        sign_up_user()
        resp_put = make_put_request(USER_URL, body={'old_password': "123qwe", 'new_password': "122qwe"}, access_token=access_token_user)
        resp = make_get_request(USER_URL, access_token=access_token_user)
        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
