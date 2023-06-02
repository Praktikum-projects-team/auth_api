from marshmallow import Schema, fields, validate

from api.v1.models.marshmallow_init import ma
from db.models import LoginHistory as LoginHistoryModel


class PaginateIn(Schema):
    page = fields.Int(validate=validate.Range(min=1, error='page must be positive number'), default=1)
    per_page = fields.Int(validate=validate.Range(min=1, error='per_page must be positive number'), default=20)


class PaginateOut(PaginateIn):
    pages_total = fields.Int()


paginate_in = PaginateIn()
