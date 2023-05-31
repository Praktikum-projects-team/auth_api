from http import HTTPStatus

import pytest

from tests.functional.testdata.user import get_user_data
from tests.functional.utils.constants import RoleName
from tests.functional.utils.helpers import (
    create_role,
    create_user,
    get_user_id_by_login,
    make_get_request,
    make_put_request
)
from tests.functional.utils.routes import ADMIN_USER_URL


class TestAdminUsers:

    def test_admin_users_all(self, access_token_admin):
        """Checking to get a list of users"""
        for _ in range(3):
            create_user()
        resp = make_get_request(ADMIN_USER_URL, access_token=access_token_admin)
        expected_fields = ['id', 'name', 'login', 'created_at', 'roles', 'is_superuser']

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in expected_fields:
            assert field in resp.body[0], f'No {field} in resp'

    def test_admin_users_info(self, access_token_admin):
        """Checking info about user"""
        user_data = create_user()
        user_id = get_user_id_by_login(user_data['login'], access_token=access_token_admin)
        resp = make_get_request(f'{ADMIN_USER_URL}/{user_id}', access_token=access_token_admin)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['id'] == user_id, 'Wrong id'
        assert resp.body['name'] == user_data['name'], 'Wrong name'
        assert resp.body['login'] == user_data['login'], 'Wrong login'
        assert resp.body['created_at'], 'Created_at not in resp'
        assert resp.body['is_superuser'] is False, 'Wrong is_superuser'
        assert resp.body['roles'] == [RoleName.USER], 'Wrong roles'

    def test_admin_users_info_not_found(self, access_token_admin):
        """Checking info about user that does not exist"""
        user_data = get_user_data()
        resp = make_get_request(f'{ADMIN_USER_URL}/{user_data["id"]}', access_token=access_token_admin)

        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert resp.body['message'] == 'User not found', 'Wrong message'

    @pytest.mark.parametrize('roles_name, is_superuser', [
        ([RoleName.ADMIN], False),
        ([RoleName.ADMIN, RoleName.USER], True),
        (['new_role'], False),
        (['123'], False),
        (['*^%$'], True)
    ])
    def test_admin_users_update(self, access_token_admin, roles_name, is_superuser):
        """Checking update user"""
        user_data = create_user()
        user_id = get_user_id_by_login(user_data['login'], access_token=access_token_admin)
        for role in roles_name:
            create_role(role, access_token=access_token_admin)

        resp = make_put_request(
            f'{ADMIN_USER_URL}/{user_id}',
            body={'roles': roles_name, 'is_superuser': is_superuser},
            access_token=access_token_admin
        )

        resp_after_update = make_get_request(f'{ADMIN_USER_URL}/{user_id}', access_token=access_token_admin)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['message'] == 'User updated successfully', 'Wrong message'

        assert resp_after_update.body['id'] == user_id, 'Wrong id'
        assert resp_after_update.body['name'] == user_data['name'], 'Wrong name'
        assert resp_after_update.body['login'] == user_data['login'], 'Wrong login'
        assert resp_after_update.body['created_at'], 'Created_at not in resp'
        assert resp_after_update.body['is_superuser'] == is_superuser, 'Wrong is_superuser'
        assert resp_after_update.body['roles'] == roles_name, 'Wrong roles'

    def test_admin_users_update_not_found(self, access_token_admin):
        """Checking update user not found"""
        user_data = get_user_data()

        resp = make_put_request(
            f'{ADMIN_USER_URL}/{user_data["id"]}',
            body={'roles': RoleName.USER, 'is_superuser': False},
            access_token=access_token_admin
        )

        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert resp.body['message'] == 'User not found', 'Wrong message'

    @pytest.mark.parametrize('roles_name', [['role_name_not_exist'], ['456'], ['***']])
    def test_admin_users_update_not_exist_role(self, access_token_admin, roles_name):
        """Checking update user on role not exist"""
        user_data = create_user()
        user_id = get_user_id_by_login(user_data['login'], access_token=access_token_admin)

        resp = make_put_request(
            f'{ADMIN_USER_URL}/{user_id}',
            body={'roles': roles_name, 'is_superuser': False},
            access_token=access_token_admin
        )

        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert resp.body['message'] == f'Role {roles_name[0]} not found', 'Wrong message'
