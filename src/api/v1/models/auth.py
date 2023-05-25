from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load


class LoginIn(Schema):
    login = fields.Email(required=True)
    password = fields.Str(required=True)


class SignUpIn(LoginIn):
    name = fields.Str()


class LoginOut(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


login_in = LoginIn()
login_out = LoginOut()
sign_up_in = SignUpIn()
