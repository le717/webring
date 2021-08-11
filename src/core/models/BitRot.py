from marshmallow import fields

from src.core.models import OrderedSchema


__all__ = ["RotResult"]


class RotResult(OrderedSchema):
    uuid = fields.UUID()
    url = fields.Url()
    result = fields.String()
