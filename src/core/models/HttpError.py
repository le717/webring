import marshmallow as ma


__all__ = ["HttpError"]


class HttpError(ma.Schema):
    """Simple HTTP error schema."""

    code = ma.fields.Integer()
    status = ma.fields.String()
    message = ma.fields.String()
    errors = ma.fields.Dict()
