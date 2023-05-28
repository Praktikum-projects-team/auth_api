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
from db.queries.admin_users import get_user_roles_by_user_id

admin_users_bp = Blueprint("admin_users_bp", __name__)


@admin_users_bp.route("/", methods=["GET"])
def users_all():
    roles_db = User.query.all()
    result = admin_user_all_schema.dump(roles_db)

    for user in result:
        user['roles'] = get_user_roles_by_user_id(user['id'])

    return jsonify(result)


@admin_users_bp.route("/<user_id>", methods=["GET"])
def user_info(user_id: UUID):
    try:
        user = User.query.filter_by(id=user_id).first()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST

    if not user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    result = admin_user_info_schema.dump(user)
    result.update({"roles": get_user_roles_by_user_id(user_id)})

    return jsonify(result)


@admin_users_bp.route("/<user_id>", methods=["PUT"])
def user_update(user_id: UUID):
    user_data = request.get_json()
    try:
        user = User.query.filter_by(id=user_id).first()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST

    if not user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    try:
        body = admin_user_update_schema.load(user_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    user.is_superuser = body['is_superuser']
    db.session.commit()

    for role_name in body['roles']:
        role_exist = Role.query.filter(Role.name == role_name).first()
        if not role_exist:
            return {"message": f"Role {role_name} not found"}, HTTPStatus.NOT_FOUND

        user_role_exist = UserRole.query.filter(UserRole.user_id == user_id, UserRole.role_id == role_exist.id).first()
        if not user_role_exist:
            user_role = UserRole(user_id=user_id, role_id=role_exist.id)
            db.session.add(user_role)
            db.session.commit()

    all_user_roles = get_user_roles_by_user_id(user_id)
    for role_name in all_user_roles:
        if role_name not in body['roles']:
            user_role = UserRole.query.filter(
                UserRole.user_id == user_id,
                UserRole.role_id == Role.query.filter(Role.name == role_name).first().id
            ).first()
            db.session.delete(user_role)
            db.session.commit()

    return {"message": "User updated successfully"}, HTTPStatus.CREATED
