from marshmallow import fields, Schema


__all__ = ["WebLink", "WebLinkCreate", "WebLinkId", "WebLinkUpdate"]


class WebLink(Schema):
    id = fields.UUID()
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    date_added = fields.DateTime(format="iso")
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()


class WebLinkCreate(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    url = fields.Url(required=True)


class WebLinkId(Schema):
    id = fields.UUID(required=True)


class WebLinkUpdate(Schema):
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()
