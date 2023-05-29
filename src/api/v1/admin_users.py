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

admin_users_bp = Blueprint('admin_users_bp', __name__)


@admin_users_bp.route('/', methods=['GET'])
def users_all():
    users = User.query.all()
    result = admin_user_all_schema.dump(users)

    for user in result:
        user['roles'] = [role['name'] for role in user['roles']]

    return jsonify(result)


@admin_users_bp.route('/<user_id>', methods=['GET'])
def user_info(user_id: UUID):
    try:
        user = User.query.filter_by(id=user_id).first()
    except (ValueError, DataError) as err:
        return {'message': str(err)}, HTTPStatus.BAD_REQUEST

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    result = admin_user_info_schema.dump(user)
    result.update({'roles': [role['name'] for role in result['roles']]})

    return jsonify(result)


@admin_users_bp.route('/<user_id>', methods=['PUT'])
def user_update(user_id: UUID):
    user_data = request.get_json()
    try:
        user = User.query.filter_by(id=user_id).first()
    except (ValueError, DataError) as err:
        return {'message': str(err)}, HTTPStatus.BAD_REQUEST

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    try:
        body = admin_user_update_schema.load(user_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    user.is_superuser = body['is_superuser']
    user.roles = []

    for role_name in body['roles']:
        role = Role.query.filter(Role.name == role_name).first()
        if not role:
            return {'message': f'Role {role_name} not found'}, HTTPStatus.NOT_FOUND

        user_role = UserRole(user_id=user_id, role_id=role.id)
        db.session.add(user_role)

    db.session.commit()

    return {'message': 'User updated successfully'}, HTTPStatus.CREATED
