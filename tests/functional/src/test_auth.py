from http import HTTPStatus

import pytest

from tests.functional.testdata.user import get_user_data
from tests.functional.utils.helpers import make_post_request
from tests.functional.utils.routes import AUTH_URL_SIGN_UP


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
