from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load


class LoginIn(Schema):
    login = fields.Email(required=True)
    password = fields.DateTime(dump_only=True)


class SignUpIn(LoginIn):
    name = fields.Str()


login_in = LoginIn()
sign_up_in = SignUpIn()
