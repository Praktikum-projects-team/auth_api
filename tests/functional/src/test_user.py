from http import HTTPStatus

from tests.functional.testdata.user import get_user_data
from tests.functional.utils.constants import UserData
from tests.functional.utils.helpers import (
    access_token_user_after_login_or_password_changed,
    create_user,
    make_get_request,
    make_put_request
)
from tests.functional.utils.routes import (
    USER_URL,
    USER_URL_CHANGE_LOGIN,
    USER_URL_CHANGE_PASSWORD,
    USER_URL_LOGIN_HISTORY
)


class TestUser:

    def test_user_info(self, user_data_with_tokens):
        """Checking info about current user"""
        resp = make_get_request(USER_URL, token=user_data_with_tokens['access_token'])

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['login'] == user_data_with_tokens['user_data']['login'], 'Wrong login'

    def test_user_change_info(self, user_data_with_tokens):
        """Checking updating info about current user"""
        resp_put = make_put_request(USER_URL, body={'name': "newname"}, token=user_data_with_tokens['access_token'])
        resp = make_get_request(USER_URL, token=user_data_with_tokens['access_token'])

        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['name'] == "newname", 'Incorrect name after changing'

    def test_user_login_history(self, user_data_with_tokens):
        """Checking to get login history of current user"""
        resp = make_get_request(USER_URL_LOGIN_HISTORY, token=user_data_with_tokens['access_token'])
        expected_fields = ['id', 'user_agent', 'auth_datetime']

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in expected_fields:
            assert field in resp.body['results'][0], f'No {field} in resp'

    def test_user_change_login(self, user_data_with_tokens):
        """Checking updating user login"""
        user_data_new = get_user_data()
        resp_put = make_put_request(USER_URL_CHANGE_LOGIN,
                                    body={'new_login': user_data_new['login']},
                                    token=user_data_with_tokens['access_token']
                                    )

        new_access_token = access_token_user_after_login_or_password_changed(
            user_data_new['login'],
            user_data_with_tokens['user_data']['password']
        )
        resp = make_get_request(USER_URL, token=new_access_token)

        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp_put.body['message'] == 'User login updated successfully', 'Wrong message'

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['login'] == user_data_new['login'], 'Wrong login'

    def test_user_change_login_duplicate(self, user_data_with_tokens):
        """Checking updating user login to the one that already exists"""
        resp = make_put_request(USER_URL_CHANGE_LOGIN,
                                body={'new_login': create_user()['login']},
                                token=user_data_with_tokens['access_token']
                                )

        assert resp.status == HTTPStatus.CONFLICT, 'Wrong status code'
        assert resp.body['message'] == 'Login already exist', 'Wrong message'

    def test_user_change_password(self, user_data_with_tokens):
        """Checking updating user password"""
        user_data_new = get_user_data()
        resp_put = make_put_request(USER_URL_CHANGE_PASSWORD,
                                    body={'old_password': user_data_with_tokens['user_data']['password'],
                                          'new_password': user_data_new['password']},
                                    token=user_data_with_tokens['access_token'])

        new_access_token = access_token_user_after_login_or_password_changed(
            user_data_with_tokens['user_data']['login'],
            user_data_new['password']
        )
        resp = make_get_request(USER_URL, token=new_access_token)

        assert resp_put.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp_put.body['message'] == 'User password updated successfully', 'Wrong message'

        assert resp.status == HTTPStatus.OK, 'Wrong status code'

    def test_user_change_password_incorrect(self, user_data_with_tokens):
        """Checking updating user password with an incorrect old password"""
        resp = make_put_request(USER_URL_CHANGE_PASSWORD,
                                body={'old_password': create_user()['password'],
                                      'new_password': UserData.NEW_PASSWORD},
                                token=user_data_with_tokens['access_token'])

        assert resp.status == HTTPStatus.CONFLICT, 'Wrong status code'
        assert resp.body['message'] == 'Incorrect old password', 'Wrong message'
