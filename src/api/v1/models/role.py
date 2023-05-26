from marshmallow import fields, validate

from api.v1.models.marshmallow_init import ma
from db.models import Role


class RoleBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role


class RoleNameSchema(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))


class RoleUserSchema(ma.Schema):
    user_id = fields.UUID(required=True)
    role_id = fields.UUID(required=True)


role_base_schema = RoleBaseSchema()
role_base_schema_all = RoleBaseSchema(many=True)
role_name_schema = RoleNameSchema()
role_user_schema = RoleUserSchema()
