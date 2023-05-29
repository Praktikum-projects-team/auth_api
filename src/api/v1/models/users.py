from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load
from api.v1.models.marshmallow_init import ma
from db.models import LoginHistory as LoginHistoryModel


class UsersSchema(Schema):
    name = fields.Str()
    login = fields.Str()
    created_at = fields.DateTime()


class UserChangeData(Schema):
    name = fields.Str(required=True)


class ChangeLogin(Schema):
    new_login = fields.Str(required=True)


class ChangePassword(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)


class LoginHistory(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LoginHistoryModel


user_schema = UsersSchema()
user_change_data = UserChangeData()
change_login = ChangeLogin()
change_password = ChangePassword()
login_history = LoginHistory(many=True)
