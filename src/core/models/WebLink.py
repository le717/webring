from datetime import UTC

import sys_vars
from marshmallow import Schema, fields


__all__ = ["WebLink", "WebLinkCreate", "WebLinkGet", "WebLinkId", "WebLinkUpdate"]


class WebLink(Schema):
    id = fields.UUID()
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    date_added = fields.AwareDateTime(format="iso", default_timezone=UTC)
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()


class WebLinkCreate(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    url = fields.Url(required=True)


class WebLinkGet(Schema):
    include_rotted = fields.Boolean(
        load_default=sys_vars.get_bool("FILTER_INCLUDE_ROTTED", default=True)
    )
    exclude_origin = fields.Boolean(
        load_default=sys_vars.get_bool("FILTER_EXCLUDE_ORIGIN", default=True)
    )


class WebLinkId(Schema):
    id = fields.UUID(required=True)


class WebLinkUpdate(Schema):
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()
