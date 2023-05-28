import logging
from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import DataError

from api.v1.models.admin_users import admin_user_all_schema, admin_user_base_schema, admin_user_info_schema
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