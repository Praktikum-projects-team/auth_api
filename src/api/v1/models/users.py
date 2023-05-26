from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load


class UsersSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    login = fields.String()


user = UsersSchema()
