from marshmallow import fields, Schema, ValidationError

from src.core.models.RotStates import RotStates


__all__ = ["WebLink", "WebLinkCreate", "WebLinkId", "WebLinkUpdate"]


def validate_rot_status(value: str) -> bool:
    """Ensure we only have valid rot status values."""
    try:
        RotStates(value)
    except ValueError:
        raise ValidationError("Linkrot status must be an acceptable value.")


class WebLink(Schema):
    id = fields.UUID()
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    rotted = fields.String(validate=validate_rot_status)
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
    rotted = fields.String(validate=validate_rot_status)
    is_dead = fields.Boolean()
    is_web_archive = fields.Boolean()
