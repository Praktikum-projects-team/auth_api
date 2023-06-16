from marshmallow import Schema, fields, validate


class LoginIn(Schema):
    login = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(max=50))


class SignUpIn(LoginIn):
    name = fields.Str(validate=validate.Length(max=100))


class LoginOut(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


class LoginInOauth(Schema):
    login = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(max=50))


login_in = LoginIn()
login_out = LoginOut()
sign_up_in = SignUpIn()
login_in_oauth = LoginInOauth()
