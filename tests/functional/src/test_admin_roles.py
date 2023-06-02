from http import HTTPStatus

import pytest

from tests.functional.testdata.role import get_role_data, get_role_id_by_name
from tests.functional.utils.helpers import (
    make_delete_request,
    make_get_request,
    make_post_request,
    make_put_request
)
from tests.functional.utils.routes import ROLES_URL


class TestRole:

    def test_admin_roles_all(self, access_token_admin):
        """Checking to get a list of roles"""
        for _ in range(3):
            role_data = get_role_data()
            make_post_request(ROLES_URL, body={'name': role_data['name']}, token=access_token_admin)

        resp = make_get_request(ROLES_URL, token=access_token_admin)
        expected_fields = ['id', 'name']

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        for field in expected_fields:
            assert field in resp.body[0], f'No {field} in resp'

    def test_admin_roles_create(self, access_token_admin):
        """Checking the creation of a new role"""
        role_data = get_role_data()
        resp = make_post_request(ROLES_URL, body={'name': role_data['name']}, token=access_token_admin)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['message'] == 'Role created successfully', 'Wrong message'

    def test_admin_roles_create_duplicate(self, access_token_admin):
        """Checking the creation of a duplicate role"""
        role_data = get_role_data()
        make_post_request(ROLES_URL, body={'name': role_data['name']}, token=access_token_admin)
        resp = make_post_request(ROLES_URL, body={'name': role_data['name']}, token=access_token_admin)

        assert resp.status == HTTPStatus.CONFLICT, 'Wrong status code'
        assert resp.body['message'] == 'Role already exist', 'Wrong message'

    def test_admin_roles_info(self, access_token_admin):
        """Checking info about role"""
        role_data = get_role_data()
        make_post_request(ROLES_URL, body={'name': role_data['name']}, token=access_token_admin)
        role_id = get_role_id_by_name(role_data['name'], access_token=access_token_admin)
        resp = make_get_request(f'{ROLES_URL}/{role_id}', token=access_token_admin)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['id'] == role_id, 'Wrong id'
        assert resp.body['name'] == role_data['name'], 'Wrong name'

    def test_admin_roles_info_not_found(self, access_token_admin):
        """Checking info about role that does not exist"""
        role_data = get_role_data()
        resp = make_get_request(f'{ROLES_URL}/{role_data["id"]}', token=access_token_admin)

        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert resp.body['message'] == 'Role not found in db', 'Wrong message'

    def test_admin_roles_update(self, access_token_admin):
        """Checking update role"""
        role_data_1 = get_role_data()
        role_data_2 = get_role_data()
        make_post_request(ROLES_URL, body={'name': role_data_1['name']}, token=access_token_admin)
        role_id = get_role_id_by_name(role_data_1['name'], access_token=access_token_admin)

        resp = make_put_request(
            f'{ROLES_URL}/{role_id}', body={'name': role_data_2['name']}, token=access_token_admin
        )
        resp_role_after_update = make_get_request(f'{ROLES_URL}/{role_id}', token=access_token_admin)

        assert resp.status == HTTPStatus.CREATED, 'Wrong status code'
        assert resp.body['message'] == 'Role updated successfully', 'Wrong message'
        assert resp_role_after_update.body['name'] == role_data_2['name'], 'Wrong update name'

    def test_admin_roles_update_duplicate(self, access_token_admin):
        """Checking update role duplicate"""
        role_data = get_role_data()
        make_post_request(ROLES_URL, body={'name': role_data['name']}, token=access_token_admin)
        role_id = get_role_id_by_name(role_data['name'], access_token=access_token_admin)

        make_put_request(f'{ROLES_URL}/{role_id}', body={'name': role_data['name']}, token=access_token_admin)
        resp = make_put_request(
            f'{ROLES_URL}/{role_id}', body={'name': role_data['name']}, token=access_token_admin
        )

        assert resp.status == HTTPStatus.CONFLICT, 'Wrong status code'
        assert resp.body['message'] == 'Role with this name already exist in db', 'Wrong message'

    def test_admin_roles_update_not_found(self, access_token_admin):
        """Checking update role that does not exist"""
        role_data = get_role_data()
        resp = make_put_request(
            f'{ROLES_URL}/{role_data["id"]}', body={'name': role_data['name']}, token=access_token_admin
        )
        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert resp.body['message'] == 'Role not found in db', 'Wrong message'

    def test_admin_roles_delete(self, access_token_admin):
        """Checking delete role"""
        role_data = get_role_data()
        make_post_request(ROLES_URL, body={'name': role_data['name']}, token=access_token_admin)
        role_id = get_role_id_by_name(role_data['name'], access_token=access_token_admin)
        resp = make_delete_request(f'{ROLES_URL}/{role_id}', token=access_token_admin)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['message'] == 'Role deleted successfully', 'Wrong message'

    def test_admin_roles_delete_not_found(self, access_token_admin):
        """Checking delete role that does not exist"""
        role_data = get_role_data()
        resp = make_delete_request(f'{ROLES_URL}/{role_data["id"]}', token=access_token_admin)

        assert resp.status == HTTPStatus.NOT_FOUND, 'Wrong status code'


class TestRoleParams:

    check_params_role_id_status_code = [
        ('ddaa3878-0f37-4135-966f-49458b0e33bf', HTTPStatus.NOT_FOUND),
        ('ddaa0000-0f37-4135-966f-49458b0e00bf', HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.BAD_REQUEST),
        (0, HTTPStatus.BAD_REQUEST),
        (1, HTTPStatus.BAD_REQUEST),
        (2.5, HTTPStatus.BAD_REQUEST),
        ('uuid', HTTPStatus.BAD_REQUEST),
        ('ddaa3878-0f37-4135-966f', HTTPStatus.BAD_REQUEST),
        ('%#$*', HTTPStatus.BAD_REQUEST)
    ]

    check_params_name = [-1, 0, 1, 2.5]

    @pytest.mark.parametrize('role_id, status_code', check_params_role_id_status_code)
    def test_admin_roles_info_invalid_param(self, access_token_admin, role_id, status_code):
        """Checking info about role with invalid param"""
        resp = make_get_request(f'{ROLES_URL}/{role_id}', token=access_token_admin)

        assert resp.status == status_code, 'Wrong status code'

    @pytest.mark.parametrize('name', check_params_name)
    def test_admin_roles_create_invalid_param(self, access_token_admin, name):
        """Checking create role with invalid param"""
        resp = make_post_request(ROLES_URL, body={'name': name}, token=access_token_admin)

        assert resp.status == HTTPStatus.BAD_REQUEST, 'Wrong status code'

    @pytest.mark.parametrize('role_id, status_code', check_params_role_id_status_code)
    def test_admin_roles_update_invalid_param_role_id(self, access_token_admin, role_id, status_code):
        """Checking update role with invalid param"""
        role_data = get_role_data()
        resp = make_put_request(
            f'{ROLES_URL}/{role_id}', body={'name': role_data['name']}, token=access_token_admin
        )

        assert resp.status == status_code, 'Wrong status code'

    @pytest.mark.parametrize('name', check_params_name)
    def test_admin_roles_update_invalid_param_name(self, access_token_admin, name):
        """Checking update role with invalid param"""
        role_data = get_role_data()
        make_post_request(ROLES_URL, body={'name': role_data['name']}, token=access_token_admin)
        role_id = get_role_id_by_name(role_data['name'], access_token=access_token_admin)

        resp = make_put_request(f'{ROLES_URL}/{role_id}', body={'name': name}, token=access_token_admin)

        assert resp.status == HTTPStatus.BAD_REQUEST, 'Wrong status code'

    @pytest.mark.parametrize('role_id, status_code', check_params_role_id_status_code)
    def test_admin_roles_delete_invalid_param(self, access_token_admin, role_id, status_code):
        """Checking delete role with invalid param"""
        resp = make_delete_request(f'{ROLES_URL}/{role_id}', token=access_token_admin)

        assert resp.status == status_code, 'Wrong status code'
