import logging
from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import DataError

from api.v1.models.admin_users import admin_user_base_schema, admin_user_info_schema
from db.models import User, UserRole
from db.pg_db import db

admin_users_bp = Blueprint("admin_users_bp", __name__)


# Todo добавить ручку получения всех юзеров списком

@admin_users_bp.route("/<user_id>", methods=["GET"])
def user_info(user_id: UUID):
    try:
        user = User.query.filter_by(id=user_id).first()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST

    if not user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    try:
        user_roles = UserRole.query.filter_by(user_id=user_id).all()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST

    result = admin_user_info_schema.dump(user)
    result_user_roles = [role.name for role in user_roles]
    result.update({"roles": result_user_roles})

    return jsonify(result)
