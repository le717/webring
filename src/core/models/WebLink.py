from datetime import UTC

import sys_vars
from marshmallow import Schema, fields


__all__ = ["AllEntries", "Entry", "EntryCreate", "EntryId", "EntryUpdate", "RingArgs"]


class Entry(Schema):
    uuid = fields.UUID(data_key="id")
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    date_added = fields.AwareDateTime(format="iso", default_timezone=UTC)
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()


class Meta(Schema):
    name = fields.String()
    maintainer = fields.String()
    home_url = fields.Url()
    software = fields.Url()
    version = fields.String()


class AllEntries(Schema):
    meta = fields.Nested(Meta)
    entries = fields.List(fields.Nested(Entry))


class EntryCreate(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    url = fields.Url(required=True)


class RingArgs(Schema):
    include_dead = fields.Boolean(load_default=sys_vars.get_bool("FILTER_INCLUDE_DEAD"))
    include_web_archive = fields.Boolean(
        load_default=sys_vars.get_bool("FILTER_INCLUDE_WEB_ARCHIVE")
    )
    exclude_origin = fields.Boolean(load_default=sys_vars.get_bool("FILTER_EXCLUDE_ORIGIN"))


class EntryId(Schema):
    id = fields.UUID(required=True)


class EntryUpdate(Schema):
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()
