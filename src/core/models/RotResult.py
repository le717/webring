from marshmallow import fields, Schema


__all__ = ["RotResult"]


class RotResult(Schema):
    id = fields.UUID()
    url = fields.Url()
    result = fields.String()
