from http import HTTPStatus

from flask import Blueprint
from flask_pydantic import validate
from pydantic import UUID4

from api.v1.models.role import RoleBase, RoleName
from db.models import Role
from db.pg_db import db

roles = Blueprint("roles", __name__)


@roles.route("/", methods=["GET"])
@validate(response_many=True)
def roles_all():
    return [RoleBase(id=role.id, name=role.name) for role in Role.query.all()]


@roles.route("/", methods=["POST"])
@validate()
def role_create(body: RoleBase):
    role_exist = db.session.query(Role).filter(Role.name == body.name).first()
    if role_exist:
        return {"msg": "Role already exist"}, HTTPStatus.CONFLICT
    new_role = Role(name=body.name)
    db.session.add(new_role)
    db.session.commit()
    return {"msg": "Role created successfully"}, HTTPStatus.CREATED


@roles.route("/{role_id}", methods=["GET"])
def role_info(role_id: UUID4):
    role = Role.query.filter_by(id=role_id).first()
    return RoleBase(id=role.id, name=role.name)


@roles.route("/<role_id>", methods=["PUT"])
@validate()
def role_update(role_id: UUID4, body: RoleName):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND
    name_exist = Role.query.filter_by(name=body.name).first()
    if name_exist:
        return {"msg": "Role with this name already exist"}, HTTPStatus.CONFLICT
    role.name = body.name
    db.session.query(Role).filter_by(id=role.id).update({"name": role.name})
    db.session.commit()
    return RoleBase(id=role.id, name=role.name)


@roles.route("/<role_id>", methods=["DELETE"])
@validate()
def role_delete(role_id: UUID4):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND
    db.session.query(Role).filter_by(id=role.id).delete()
    db.session.commit()
    return {"msg": "Role deleted successfully"}, HTTPStatus.OK
