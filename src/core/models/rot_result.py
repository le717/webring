from datetime import UTC

from marshmallow import Schema, fields


__all__ = ["HistoryEntry", "RotResult"]


class _Result(Schema):
    times_failed = fields.Integer()
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()


class RotResult(Schema):
    id = fields.UUID()
    url = fields.Url()
    result = fields.Nested(_Result())


class HistoryEntry(Schema):
    date_checked = fields.AwareDateTime(format="iso", default_timezone=UTC)
    url_checked = fields.Url(absolute=True)
    was_alive = fields.Boolean()
    message = fields.String()
