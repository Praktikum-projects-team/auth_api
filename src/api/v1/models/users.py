from marshmallow import Schema, fields, validate

from api.v1.models.marshmallow_init import ma
from db.models import LoginHistory as LoginHistoryModel


class UsersSchema(Schema):
    name = fields.Str(validate=validate.Length(max=100))
    login = fields.Str(validate=validate.Length(max=50))
    created_at = fields.DateTime()


class UserChangeData(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=100))


class ChangeLogin(Schema):
    new_login = fields.Str(required=True, validate=validate.Length(max=50))


class ChangePassword(Schema):
    old_password = fields.Str(required=True, validate=validate.Length(max=50))
    new_password = fields.Str(required=True, validate=validate.Length(max=50))


class LoginHistory(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LoginHistoryModel


user_schema = UsersSchema()
user_change_data = UserChangeData()
change_login = ChangeLogin()
change_password = ChangePassword()
login_history = LoginHistory(many=True)
