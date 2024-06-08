from marshmallow import Schema, fields


__all__ = ["HttpError"]


class HttpError(Schema):
    """Simple HTTP error schema."""

    code = fields.Integer()
    status = fields.String()
    message = fields.String()
    errors = fields.Dict()
