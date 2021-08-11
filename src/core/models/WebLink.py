from marshmallow import fields

from src.core.models import OrderedSchema


__all__ = ["WebLink", "WebLinkCreate", "WebLinkId", "WebLinkUpdate"]


class WebLink(OrderedSchema):
    id = fields.UUID()
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    rotted = fields.String()
    date_added = fields.DateTime(format="iso")


class WebLinkCreate(OrderedSchema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    url = fields.Url(required=True)


class WebLinkId(OrderedSchema):
    id = fields.UUID(required=True)


class WebLinkUpdate(OrderedSchema):
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    rotted = fields.String()
