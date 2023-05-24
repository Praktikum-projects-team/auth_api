from marshmallow import fields, Schema, validate


class RoleBaseSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.String(required=True)


class RoleNameSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))


class RoleUserSchema(Schema):
    user_id = fields.UUID(required=True)
    role_id = fields.UUID(required=True)


role_base_schema = RoleBaseSchema()
role_base_schema_all = RoleBaseSchema(many=True)
role_name_schema = RoleNameSchema()
role_user_schema = RoleUserSchema()
