from http import HTTPStatus

import pytest

from tests.functional.testdata.user import get_user_data
from tests.functional.utils.helpers import make_post_request
from tests.functional.utils.routes import (
    AUTH_URL_CHECK_ACCESS_TOKEN,
    AUTH_URL_LOGIN,
    AUTH_URL_LOGOUT,
    AUTH_URL_REFRESH,
    AUTH_URL_SIGN_UP
)


class TestAuthSignUp:

    def test_auth_sign_up(self):
        """Checking sign up"""
        user_data = get_user_data()
        user_data.pop('id')
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['msg'] == 'User created', 'Wrong message'

    def test_auth_sign_up_login(self):
        """Checking sign up login"""
        for _ in range(5):
            user_data = get_user_data()
            user_data.pop('id')
            resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

            assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
            assert resp.body['msg'] == 'User created', 'Wrong message'

    @pytest.mark.parametrize('login', ['user4@user', 'user4@', '', 'логин@', '***@***.**', 1, 0, 2.5, -1, 1000000])
    def test_auth_sign_up_login_invalid(self, login):
        """Checking sign up login invalid"""
        user_data = get_user_data()
        user_data.pop('id')
        user_data.update({'login': login})
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['message']['login'][0] == 'Not a valid email address.', 'Wrong message'

    def test_auth_sign_up_login_duplicate(self):
        """Checking sign up with duplicate login"""
        user_data = get_user_data()
        user_data.pop('id')

        for _ in range(2):
            resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

        assert resp.status == HTTPStatus.CONFLICT, 'Wrong status code'
        assert resp.body['message'] == f'User with login {user_data["login"]} already exists', 'Wrong message'

    @pytest.mark.parametrize('name', ['test_name', '100', '', 'кириллица', 'abcdefghijklmnopqrstuvwxyz', 'i'])
    def test_auth_sign_up_name(self, name):
        """Checking sign up name"""
        user_data = get_user_data()
        user_data.pop('id')
        user_data.update({'name': name})
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['msg'] == 'User created', 'Wrong message'

    @pytest.mark.parametrize('name', [1, 0, 2.5, -1, 1000000])
    def test_auth_sign_up_name_invalid(self, name):
        """Checking sign up name invalid"""
        user_data = get_user_data()
        user_data.pop('id')
        user_data.update({'name': name})
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['message']['name'][0] == 'Not a valid string.', 'Wrong message'

    def test_auth_sign_up_name_duplicate(self):
        """Checking sign up with duplicate name"""
        user_data_1 = get_user_data()
        user_data_2 = get_user_data()
        user_data_1.pop('id')
        user_data_2.pop('id')
        user_data_2.update({'name': user_data_1['name']})

        make_post_request(AUTH_URL_SIGN_UP, body=user_data_1)
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data_2)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['msg'] == 'User created', 'Wrong message'

    @pytest.mark.parametrize('password', [
        'test_password', '100', 'кириллица', 'FOU:labcd*^Яблefghi&*)jklmn', 'i', 'ы',
    ])
    def test_auth_sign_up_password(self, password):
        """Checking sign up password"""
        user_data = get_user_data()
        user_data.pop('id')
        user_data.update({'password': password})
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['msg'] == 'User created', 'Wrong message'

    @pytest.mark.parametrize('password', [1, 0, 2.5, -1, 1000000])
    def test_auth_sign_up_password_invalid(self, password):
        """Checking sign up password invalid"""
        user_data = get_user_data()
        user_data.pop('id')
        user_data.update({'password': password})
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['message']['password'][0] == 'Not a valid string.', 'Wrong message'

    def test_auth_sign_up_password_duplicate(self):
        """Checking sign up with duplicate password"""
        user_data_1 = get_user_data()
        user_data_2 = get_user_data()
        user_data_1.pop('id')
        user_data_2.pop('id')
        user_data_2.update({'password': user_data_1['password']})

        make_post_request(AUTH_URL_SIGN_UP, body=user_data_1)
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data_2)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['msg'] == 'User created', 'Wrong message'

    def test_auth_sign_up_same_login_and_password(self):
        """Checking sign up same login and password"""
        user_data = get_user_data()
        user_data.pop('id')
        user_data.update({'password': user_data['login']})
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['msg'] == 'User created', 'Wrong message'

    def test_auth_sign_up_all_field_invalid(self):
        """Checking sign up all field invalid"""
        user_data_invalid = {'login': 'test_login', 'name': 1, 'password': 1}
        resp = make_post_request(AUTH_URL_SIGN_UP, body=user_data_invalid)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['message']['login'][0] == 'Not a valid email address.', 'Wrong message'
        assert resp.body['message']['name'][0] == 'Not a valid string.', 'Wrong message'
        assert resp.body['message']['password'][0] == 'Not a valid string.', 'Wrong message'


class TestAuthLogin:
    def test_auth_login(self):
        """Checking login"""
        user_data = get_user_data()
        user_data.pop('id')
        make_post_request(AUTH_URL_SIGN_UP, body=user_data)
        user_data.pop('name')
        resp = make_post_request(AUTH_URL_LOGIN, body=user_data)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in ['access_token', 'refresh_token']:
            assert field in resp.body, f'No {field} in resp'

    def test_auth_login_incorrect(self):
        """Checking login incorrect"""
        user_data = get_user_data()
        user_data.pop('id')
        make_post_request(AUTH_URL_SIGN_UP, body=user_data)
        user_data.pop('name')
        user_data.update({'login': 'user_not_exist@user.ru'})
        resp = make_post_request(AUTH_URL_LOGIN, body=user_data)

        assert resp.status == HTTPStatus.UNAUTHORIZED, 'Wrong status code'
        assert resp.body['message'] == 'Login or password is incorrect', 'Wrong message'

    def test_auth_password_incorrect(self):
        """Checking password incorrect"""
        user_data = get_user_data()
        user_data.pop('id')
        make_post_request(AUTH_URL_SIGN_UP, body=user_data)
        user_data.pop('name')
        user_data.update({'password': 'password_not_exist'})
        resp = make_post_request(AUTH_URL_LOGIN, body=user_data)

        assert resp.status == HTTPStatus.UNAUTHORIZED, 'Wrong status code'
        assert resp.body['message'] == 'Login or password is incorrect', 'Wrong message'

    @pytest.mark.parametrize('login', ['user4@user', 'user4@', '', 'логин@', '***@***.**', 1, 0, 2.5, -1, 1000000])
    def test_auth_login_invalid(self, login):
        """Checking invalid login"""
        user_data = get_user_data()
        user_data.pop('id')
        user_data.update({'login': login})
        resp = make_post_request(AUTH_URL_LOGIN, body=user_data)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['message']['login'][0] == 'Not a valid email address.', 'Wrong message'

    @pytest.mark.parametrize('password', [1, 0, 2.5, -1, 1000000])
    def test_auth_password_invalid(self, password):
        """Checking invalid password"""
        user_data = get_user_data()
        user_data.pop('id')
        user_data.update({'password': password})
        resp = make_post_request(AUTH_URL_LOGIN, body=user_data)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['message']['password'][0] == 'Not a valid string.', 'Wrong message'


class TestAuthLogout:

    def test_auth_logout(self, access_token_user):
        """Checking logout"""
        resp = make_post_request(AUTH_URL_LOGOUT, token=access_token_user)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'access token successfully revoked', 'Wrong message'

    def test_auth_logout_with_token_revoked(self, access_token_user):
        """Checking logout with token revoked"""
        make_post_request(AUTH_URL_LOGOUT, token=access_token_user)
        resp = make_post_request(AUTH_URL_LOGOUT, token=access_token_user)

        assert resp.status == HTTPStatus.UNAUTHORIZED, 'Wrong status code'
        assert resp.body['msg'] == 'Token has been revoked', 'Wrong message'

    def test_auth_logout_without_access_token(self):
        """Checking logout without access token"""
        resp = make_post_request(AUTH_URL_LOGOUT)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == 'Not enough segments', 'Wrong message'

    @pytest.mark.parametrize('access_token', ['access_token_str', 1, 0, 2.5, -1, 1000000])
    def test_auth_logout_with_access_token_invalid(self, access_token):
        """Checking logout with access token invalid"""
        resp = make_post_request(AUTH_URL_LOGOUT, token=access_token)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == 'Not enough segments', 'Wrong message'

    def test_auth_logout_with_access_token_empty(self):
        """Checking logout with access token empty"""
        resp = make_post_request(AUTH_URL_LOGOUT, token='')

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'", 'Wrong message'


class TestAuthCheckAccessToken:

    def test_auth_check_access_token(self, user_data_with_tokens):
        """Checking access token"""
        resp = make_post_request(AUTH_URL_CHECK_ACCESS_TOKEN, token=user_data_with_tokens['access_token'])

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['user'] == user_data_with_tokens['user_data']['login'], 'Wrong answer'

    def test_auth_check_access_token_revoked(self, access_token_user):
        """Checking access token with token revoked"""
        make_post_request(AUTH_URL_LOGOUT, token=access_token_user)
        resp = make_post_request(AUTH_URL_CHECK_ACCESS_TOKEN, token=access_token_user)

        assert resp.status == HTTPStatus.UNAUTHORIZED, 'Wrong status code'
        assert resp.body['msg'] == 'Token has been revoked', 'Wrong message'

    def test_auth_check_without_access_token(self):
        """Checking without access token"""
        resp = make_post_request(AUTH_URL_CHECK_ACCESS_TOKEN)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == 'Not enough segments', 'Wrong message'

    @pytest.mark.parametrize('access_token', ['access_token_str', 1, 0, 2.5, -1, 1000000])
    def test_auth_check_access_token_invalid(self, access_token):
        """Checking with access token invalid"""
        resp = make_post_request(AUTH_URL_CHECK_ACCESS_TOKEN, token=access_token)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == 'Not enough segments', 'Wrong message'

    def test_auth_check_access_token_empty(self):
        """Checking with access token empty"""
        resp = make_post_request(AUTH_URL_CHECK_ACCESS_TOKEN, token='')

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'", 'Wrong message'


class TestAuthRefresh:

    def test_auth_refresh(self, user_data_with_tokens):
        """Checking refresh"""
        resp = make_post_request(AUTH_URL_REFRESH, token=user_data_with_tokens['refresh_token'])

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in ['access_token', 'refresh_token']:
            assert field in resp.body, f'No {field} in resp'

    def test_auth_refresh_token_revoked(self, user_data_with_tokens):
        """Checking refresh token with token revoked"""
        make_post_request(AUTH_URL_LOGOUT, token=user_data_with_tokens['refresh_token'])
        resp = make_post_request(AUTH_URL_REFRESH, token=user_data_with_tokens['refresh_token'])

        assert resp.status == HTTPStatus.UNAUTHORIZED, 'Wrong status code'
        assert resp.body['msg'] == 'Token has been revoked', 'Wrong message'

    def test_auth_without_refresh_token(self):
        """Checking without refresh token"""
        resp = make_post_request(AUTH_URL_REFRESH)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == 'Not enough segments', 'Wrong message'

    @pytest.mark.parametrize('refresh_token', ['refresh_token_str', 1, 0, 2.5, -1, 1000000])
    def test_auth_refresh_token_invalid(self, refresh_token):
        """Checking refresh with access token invalid"""
        resp = make_post_request(AUTH_URL_REFRESH, token=refresh_token)

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == 'Not enough segments', 'Wrong message'

    def test_auth_refresh_token_empty(self):
        """Checking with refresh token empty"""
        resp = make_post_request(AUTH_URL_REFRESH, token='')

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert resp.body['msg'] == "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'", 'Wrong message'
