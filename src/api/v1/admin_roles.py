from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from sqlalchemy.exc import DataError

from api.v1.models.admin_roles import admin_role_base_schema, admin_role_all_schema, admin_role_name_schema
from services.auth.role_checker import admin_required
from services.role.role_service import (
    roles_get_data,
    create_role,
    get_role_data,
    update_role,
    delete_role,
    RoleAlreadyExists,
    RoleNotFound
)

admin_roles_bp = Blueprint('admin_roles', __name__)


@admin_roles_bp.route('/', methods=['GET'])
@admin_required
def roles_all():
    roles_db = roles_get_data()
    result = admin_role_all_schema.dump(roles_db)
    current_app.logger.info('Data on all roles received successfully')

    return jsonify(result)


@admin_roles_bp.route('/', methods=['POST'])
@admin_required
def role_create():
    role_data = request.get_json()
    try:
        body = admin_role_name_schema.load(role_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    try:
        create_role(body['name'])
        current_app.logger.info('Role %s created successfully', body['name'])
    except RoleAlreadyExists as err:
        current_app.logger.info('Role creation failed: role already exists', body['name'])
        return jsonify(message=str(err)), HTTPStatus.CONFLICT

    return {'message': 'Role created successfully'}, HTTPStatus.CREATED


@admin_roles_bp.route('/<role_id>', methods=['GET'])
@admin_required
def role_info(role_id: UUID):
    try:
        role = get_role_data(role_id)
        current_app.logger.info('Role info received successfully, role_id = %s', role_id)
    except (ValueError, DataError) as err:
        current_app.logger.warning('Failed to get role info, role_id = %s', role_id)
        return {'message': str(err)}, HTTPStatus.BAD_REQUEST
    except RoleNotFound as err:
        current_app.logger.warning('Role not found, role_id = %s', role_id)
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND

    result = admin_role_base_schema.dump(role)

    return jsonify(result)


@admin_roles_bp.route('/<role_id>', methods=['PUT'])
@admin_required
def role_update(role_id: UUID):
    role_data = request.get_json()
    try:
        body = admin_role_name_schema.load(role_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    try:
        update_role(role_id, body['name'])
        current_app.logger.info('Role %s updated successfully', body['name'])
    except (ValueError, DataError) as err:
        current_app.logger.warning('Failed to get role info, role_id = %s', role_id)
        return {'message': str(err)}, HTTPStatus.BAD_REQUEST
    except RoleNotFound as err:
        current_app.logger.warning('Role not found, role_id = %s', role_id)
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND
    except RoleAlreadyExists as err:
        current_app.logger.warning('Role already exist, role_id = %s', role_id)
        return jsonify(message=str(err)), HTTPStatus.CONFLICT

    return {'message': 'Role updated successfully'}, HTTPStatus.CREATED


@admin_roles_bp.route('/<role_id>', methods=['DELETE'])
@admin_required
def role_delete(role_id: UUID):
    try:
        delete_role(role_id)
        current_app.logger.info('Role %s deleted successfully', role_id)
    except (ValueError, DataError) as err:
        current_app.logger.warning('Role delete failed, role_id = %s', role_id)
        return {'message': str(err)}, HTTPStatus.BAD_REQUEST
    except RoleNotFound as err:
        current_app.logger.warning('Role not found, role_id = %s', role_id)
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND

    return {'message': 'Role deleted successfully'}, HTTPStatus.OK
