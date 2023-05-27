from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load


class UsersSchema(Schema):
    name = fields.Str()
    login = fields.Str()
    created_at = fields.DateTime()


class UserChangeData(Schema):
    name = fields.Str()


class ChangeLogin(Schema):
    new_login = fields.Str()


class ChangePassword(Schema):
    old_password = fields.Str()
    new_password = fields.Str()


class LoginHistory(Schema):
    user_id = fields.UUID()
    user_agent = fields.Str()
    auth_datetime = fields.DateTime()


user_schema = UsersSchema()
user_change_data = UserChangeData()
change_login = ChangeLogin()
change_password = ChangePassword()
login_history = LoginHistory(many=True)
