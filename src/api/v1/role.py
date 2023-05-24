from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from pydantic import UUID4

from api.v1.models.role import role_base_schema, role_base_schema_all, role_name_schema
from db.models import Role
from db.pg_db import db

roles = Blueprint("roles", __name__)


@roles.route("/", methods=["GET"])
def roles_all():
    roles_db = Role.query.all()
    result = role_base_schema_all.dump(roles_db)

    return jsonify(result)


@roles.route('/', methods=['POST'])
def role_create():
    role_data = request.get_json()
    role_name_errors = role_name_schema.validate(role_data)
    if role_name_errors:
        return jsonify(role_name_errors), HTTPStatus.BAD_REQUEST

    body = role_name_schema.load(role_data)
    role_exist = db.session.query(Role).filter(Role.name == body['name']).first()
    if role_exist:
        return {"msg": "Role already exist"}, HTTPStatus.CONFLICT

    new_role = Role(name=body['name'])
    db.session.add(new_role)
    db.session.commit()

    return {"msg": "Role created successfully"}, HTTPStatus.CREATED


@roles.route("/<role_id>", methods=["GET"])
def role_info(role_id: UUID4):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND

    result = role_base_schema.dump(role)

    return jsonify(result)


@roles.route("/<role_id>", methods=["PUT"])
@validate()
def role_update(role_id: UUID4):
    role_data = request.get_json()
    role_name_errors = role_name_schema.validate(role_data)
    if role_name_errors:
        return jsonify(role_name_errors), HTTPStatus.BAD_REQUEST

    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND

    body = role_name_schema.load(role_data)
    name_exist = db.session.query(Role).filter(Role.name == body['name']).first()
    if name_exist:
        return {"msg": "Role with this name already exist"}, HTTPStatus.CONFLICT

    new_role = Role(name=body['name'])
    db.session.add(new_role)
    db.session.commit()
    return {"msg": "Role created successfully"}, HTTPStatus.CREATED


@roles.route("/<role_id>", methods=["DELETE"])
@validate()
def role_delete(role_id: UUID4):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND
    db.session.query(Role).filter_by(id=role.id).delete()
    db.session.commit()
    return {"msg": "Role deleted successfully"}, HTTPStatus.OK
