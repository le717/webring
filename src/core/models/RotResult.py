from marshmallow import Schema, fields


__all__ = ["RotResult"]


class Result(Schema):
    times_failed = fields.Integer()
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()


class RotResult(Schema):
    id = fields.UUID()
    url = fields.Url()
    result = fields.Nested(Result())
