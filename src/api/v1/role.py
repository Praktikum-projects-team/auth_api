from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.v1.models.role import role_base_schema, role_base_schema_all, role_name_schema
from db.models import Role
from db.pg_db import db

roles = Blueprint("roles", __name__)


@roles.route("/", methods=["GET"])
def roles_all():
    try:
        roles_db = Role.query.all()
    except Exception as err:
        return {"message": str(err)}, HTTPStatus.UNPROCESSABLE_ENTITY

    result = role_base_schema_all.dump(roles_db)

    return jsonify(result)


@roles.route('/', methods=['POST'])
def role_create():
    role_data = request.get_json()
    role_name_errors = role_name_schema.validate(role_data)
    if role_name_errors:
        return jsonify(role_name_errors), HTTPStatus.BAD_REQUEST

    try:
        body = role_name_schema.load(role_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    role_exist = db.session.query(Role).filter(Role.name == body['name']).first()
    if role_exist:
        return {"message": "Role already exist"}, HTTPStatus.CONFLICT

    new_role = Role(name=body['name'])
    db.session.add(new_role)
    db.session.commit()

    return {"message": "Role created successfully"}, HTTPStatus.CREATED


@roles.route("/<role_id>", methods=["GET"])
def role_info(role_id: UUID):
    try:
        role = Role.query.filter_by(id=role_id).first()
    except Exception as err:
        return {"message": str(err)}, HTTPStatus.UNPROCESSABLE_ENTITY

    if not role:
        return {"message": "Role not found"}, HTTPStatus.NOT_FOUND

    result = role_base_schema.dump(role)

    return jsonify(result)


@roles.route("/<role_id>", methods=["PUT"])
def role_update(role_id: UUID):
    role_data = request.get_json()
    role_name_errors = role_name_schema.validate(role_data)
    if role_name_errors:
        return jsonify(role_name_errors), HTTPStatus.BAD_REQUEST

    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"message": "Role not found"}, HTTPStatus.NOT_FOUND

    try:
        body = role_name_schema.load(role_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    name_exist = db.session.query(Role).filter(Role.name == body['name']).first()
    if name_exist:
        return {"message": "Role with this name already exist"}, HTTPStatus.CONFLICT

    role.name = body['name']
    db.session.commit()
    return {"message": "Role updated successfully"}, HTTPStatus.CREATED


@roles.route("/<role_id>", methods=["DELETE"])
def role_delete(role_id: UUID):
    try:
        role = Role.query.filter_by(id=role_id).first()
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    if not role:
        return {"message": "Role not found"}, HTTPStatus.NOT_FOUND

    db.session.query(Role).filter_by(id=role.id).delete()
    db.session.commit()

    return {"message": "Role deleted successfully"}, HTTPStatus.OK
