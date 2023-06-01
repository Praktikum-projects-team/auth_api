import logging
from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import DataError

from api.v1.models.admin_users import (
    admin_user_all_schema,
    admin_user_info_schema,
    admin_user_update_schema
)
from db.models import Role, User, UserRole
from db.pg_db import db
from services.auth.role_checker import admin_required
from services.user.user_service import get_user_admin_info, get_user_info, update_user_admin, UserNotFound
from services.role.role_service import RoleNotFound

admin_users_bp = Blueprint('admin_users_bp', __name__)


@admin_users_bp.route('/', methods=['GET'])
@admin_required
def users_all():
    users = get_user_admin_info()
    result = admin_user_all_schema.dump(users)

    for user in result:
        user['roles'] = [role['name'] for role in user['roles']]

    return jsonify(result)


@admin_users_bp.route('/<user_id>', methods=['GET'])
@admin_required
def user_info(user_id: UUID):
    try:
        user = get_user_info(user_id)
    except (ValueError, DataError) as err:
        return {'message': str(err)}, HTTPStatus.BAD_REQUEST
    except UserNotFound as err:
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND

    result = admin_user_info_schema.dump(user)
    result.update({'roles': [role['name'] for role in result['roles']]})

    return jsonify(result)


@admin_users_bp.route('/<user_id>', methods=['PUT'])
@admin_required
def user_update(user_id: UUID):
    user_data = request.get_json()
    try:
        body = admin_user_update_schema.load(user_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    try:
        update_user_admin(user_id, body)
        logging.info("User with id %s updated successfully by admin", user_id)
    except (ValueError, DataError) as err:
        return {'message': str(err)}, HTTPStatus.BAD_REQUEST
    except UserNotFound as err:
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND
    except RoleNotFound as err:
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND

    return {'message': 'User updated successfully'}, HTTPStatus.CREATED
