from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import DataError

from api.v1.models.admin_roles import admin_role_base_schema, admin_role_base_schema_all, admin_role_name_schema
from db.models import Role
from db.pg_db import db

admin_roles_bp = Blueprint("admin_roles_bp", __name__)


@admin_roles_bp.route("/", methods=["GET"])
def roles_all():
    roles_db = Role.query.all()
    result = admin_role_base_schema_all.dump(roles_db)

    return jsonify(result)


@admin_roles_bp.route('/', methods=['POST'])
def role_create():
    role_data = request.get_json()
    try:
        body = admin_role_name_schema.load(role_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    role_exist = db.session.query(Role).filter(Role.name == body['name']).first()
    if role_exist:
        return {"message": "Role already exist"}, HTTPStatus.CONFLICT

    new_role = Role(name=body['name'])
    db.session.add(new_role)
    db.session.commit()

    return {"message": "Role created successfully"}, HTTPStatus.CREATED


@admin_roles_bp.route("/<role_id>", methods=["GET"])
def role_info(role_id: UUID):
    try:
        role = Role.query.filter_by(id=role_id).first()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST

    if not role:
        return {"message": "Role not found"}, HTTPStatus.NOT_FOUND

    result = admin_role_base_schema.dump(role)

    return jsonify(result)


@admin_roles_bp.route("/<role_id>", methods=["PUT"])
def role_update(role_id: UUID):
    role_data = request.get_json()
    try:
        role = Role.query.filter_by(id=role_id).first()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST

    if not role:
        return {"message": "Role not found"}, HTTPStatus.NOT_FOUND

    try:
        body = admin_role_name_schema.load(role_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    name_exist = db.session.query(Role).filter(Role.name == body['name']).first()
    if name_exist:
        return {"message": "Role with this name already exist"}, HTTPStatus.CONFLICT

    role.name = body['name']
    db.session.commit()
    return {"message": "Role updated successfully"}, HTTPStatus.CREATED


@admin_roles_bp.route("/<role_id>", methods=["DELETE"])
def role_delete(role_id: UUID):
    try:
        role = Role.query.filter_by(id=role_id).first()
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    if not role:
        return {"message": "Role not found"}, HTTPStatus.NOT_FOUND

    db.session.query(Role).filter_by(id=role.id).delete()
    db.session.commit()

    return {"message": "Role deleted successfully"}, HTTPStatus.OK
