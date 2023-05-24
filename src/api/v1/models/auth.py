from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load


class LoginIn(Schema):
    login = fields.Email(required=True)
    password = fields.DateTime(dump_only=True)


class SignUpIn(LoginIn):
    name = fields.Str()


class LoginOut(Schema):
    access_token = fields.Str
    refresh_token = fields.Str


login_in = LoginIn()
login_out = LoginOut()
sign_up_in = SignUpIn()
