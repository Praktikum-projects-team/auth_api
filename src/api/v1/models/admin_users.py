from marshmallow import fields, validate

from api.v1.models.admin_roles import AdminRoleNameSchema
from api.v1.models.marshmallow_init import ma
from db.models import User


class AdminUserBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class AdminUserInfoSchema(ma.Schema):
    id = fields.UUID(required=True)
    login = fields.String(required=True, validate=validate.Length(min=1, max=50))
    created_at = fields.DateTime(required=True)
    name = fields.String(required=False, validate=validate.Length(min=1, max=50))
    is_superuser = fields.Boolean(required=True)
    roles = fields.Nested(AdminRoleNameSchema, many=True)


admin_user_base_schema = AdminUserBaseSchema()
admin_user_info_schema = AdminUserInfoSchema()
admin_user_info_schema_all = AdminUserInfoSchema(many=True)
