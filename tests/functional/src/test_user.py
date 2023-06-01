from http import HTTPStatus

from tests.functional.utils.helpers import (
    make_get_request,
    make_put_request,
    sign_up_user,
    access_token_user_after_login_changed,
    access_token_user_after_password_changed,
    create_user
)
from tests.functional.utils.routes import USER_URL
from tests.functional.utils.constants import UserData


class TestUser:

    def test_user_info(self, access_token_user):
        """Checking info about current user"""
        sign_up_user()
        resp = make_get_request(USER_URL, access_token=access_token_user)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['login'] == UserData.LOGIN, 'Wrong login'

    def test_user_change_info(self, access_token_user):
        """Checking updating info about current user"""
        sign_up_user()
        resp_put = make_put_request(USER_URL, body={'name': "newname"}, access_token=access_token_user)
        resp = make_get_request(USER_URL, access_token=access_token_user)

        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['name'] == "newname", 'Incorrect name after changing'

    def test_user_login_history(self, access_token_user):
        """Checking to get login history of current user"""
        sign_up_user()
        resp = make_get_request(f'{USER_URL}/login_history', access_token=access_token_user)
        expected_fields = ['id', 'user_agent', 'auth_datetime']

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in expected_fields:
            assert field in resp.body[0], f'No {field} in resp'

    def test_user_change_login(self, access_token_user):
        """Checking updating user login"""
        sign_up_user()
        resp_put = make_put_request(f'{USER_URL}/change_login', body={'new_login': UserData.NEW_LOGIN},
                                    access_token=access_token_user)
        resp = make_get_request(USER_URL, access_token=access_token_user_after_login_changed())

        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['login'] == UserData.NEW_LOGIN, 'Wrong login'

    def test_user_change_login_duplicate(self, access_token_user):
        """Checking updating user login to the one that already exists"""
        sign_up_user()
        resp = make_put_request(f'{USER_URL}/change_login', body={'new_login': create_user()['login']},
                                access_token=access_token_user)
        assert resp.status == HTTPStatus.CONFLICT, 'Wrong status code'
        assert resp.body['message'] == 'Login already exist', 'Wrong message'

    def test_user_change_password(self, access_token_user):
        """Checking updating user password"""
        sign_up_user()
        resp_put = make_put_request(f'{USER_URL}/change_password',
                                    body={'old_password': UserData.PASSWORD,
                                          'new_password': UserData.NEW_PASSWORD},
                                    access_token=access_token_user)
        resp = make_get_request(USER_URL, access_token=access_token_user_after_password_changed())

        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.status == HTTPStatus.OK, 'Wrong status code'

    def test_user_change_password_incorrect(self, access_token_user):
        """Checking updating user password with an incorrect old password"""
        sign_up_user()
        resp = make_put_request(f'{USER_URL}/change_password',
                                body={'old_password': create_user()['password'],
                                      'new_password': UserData.NEW_PASSWORD},
                                access_token=access_token_user)

        assert resp.status == HTTPStatus.CONFLICT, 'Wrong status code'
        assert resp.body['message'] == 'Incorrect old password', 'Wrong message'
