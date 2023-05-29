from http import HTTPStatus

import pytest

from tests.functional.utils.constants import RoleName
from tests.functional.testdata.user import get_user_data
from tests.functional.utils.helpers import create_user, make_get_request, make_put_request
from tests.functional.utils.routes import ADMIN_USER_URL


class TestAdminUsers:

    def test_admin_userss_all(self):
        """Checking to get a list of users"""
        for _ in range(3):
            create_user()
        resp = make_get_request(ADMIN_USER_URL)
        expected_fields = ['id', 'name', 'login', 'created_at', 'roles', 'is_superuser']

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in expected_fields:
            assert field in resp.body[0], f'No {field} in resp'

    def test_admin_users_info(self):
        """Checking info about user"""
        user_data = create_user()
        resp = make_get_request(f'{ADMIN_USER_URL}/{user_data["id"]}')

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['id'] == user_data['id'], 'Wrong id'
        assert resp.body['name'] == user_data['name'], 'Wrong name'
        assert resp.body['login'] == user_data['login'], 'Wrong login'
        assert resp.body['created_at'] == user_data['created_at'], 'Wrong created_at'
        assert resp.body['is_superuser'] == user_data['is_superuser'], 'Wrong is_superuser'
        assert resp.body['roles'] == [RoleName.USER], 'Wrong roles'

    def test_admin_users_info_not_found(self):
        """Checking info about user that does not exist"""
        user_data = get_user_data()
        resp = make_get_request(f'{ADMIN_USER_URL}/{user_data["id"]}')

        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert resp.body['message'] == 'User not found', 'Wrong message'

    @pytest.mark.parametrize('roles_name, is_superuser', [
        ([RoleName.ADMIN], False),
        ([RoleName.ADMIN, RoleName.USER], True),
        (['123'], False),
        (['*^%$'], True)
    ])
    def test_admin_users_update(self, roles_name, is_superuser):
        """Checking update user"""
        user_data = create_user()

        resp = make_put_request(
            f'{ADMIN_USER_URL}/{user_data["id"]}',
            body={'roles': roles_name, 'is_superuser': is_superuser}
        )

        resp_after_update = make_get_request(f'{ADMIN_USER_URL}/{user_data["id"]}')

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['message'] == 'User updated successfully', 'Wrong message'

        assert resp_after_update.body['id'] == user_data['id'], 'Wrong id'
        assert resp_after_update.body['name'] == user_data['name'], 'Wrong name'
        assert resp_after_update.body['login'] == user_data['login'], 'Wrong login'
        assert resp_after_update.body['created_at'] == user_data['created_at'], 'Wrong created_at'
        assert resp_after_update.body['is_superuser'] == is_superuser, 'Wrong is_superuser'
        assert resp_after_update.body['roles'] == roles_name, 'Wrong roles'

    def test_admin_users_update_not_found(self):
        """Checking update user not found"""
        user_data = get_user_data()

        resp = make_put_request(
            f'{ADMIN_USER_URL}/{user_data["id"]}',
            body={'roles': RoleName.USER, 'is_superuser': False}
        )

        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert resp.body['message'] == 'User not found', 'Wrong message'

    @pytest.mark.parametrize('roles_name', [['role_name_not_exist'], ['123'], ['*^%$']])
    def test_admin_users_update_not_exist_role(self, roles_name):
        """Checking update user on role not exist"""
        user_data = create_user()

        resp = make_put_request(
            f'{ADMIN_USER_URL}/{user_data["id"]}',
            body={'roles': roles_name, 'is_superuser': False}
        )

        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert resp.body['message'] == f'Role {roles_name[0]} not found', 'Wrong message'
