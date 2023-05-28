from marshmallow import fields, validate

from api.v1.models.marshmallow_init import ma
from db.models import Role


class AdminRoleBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role


class AdminRoleNameSchema(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))


admin_role_base_schema = AdminRoleBaseSchema()
admin_role_base_schema_all = AdminRoleBaseSchema(many=True)
admin_role_name_schema = AdminRoleNameSchema()
