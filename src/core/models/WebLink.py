from marshmallow import fields, ValidationError

from src.core.models import OrderedSchema
from src.core.models.RotStates import RotStates


__all__ = ["WebLink", "WebLinkCreate", "WebLinkId", "WebLinkUpdate"]


def validate_rot_status(value: str) -> bool:
    """Ensure we only have valid rot status values."""
    try:
        RotStates(value)
    except ValueError:
        raise ValidationError("Linkrot status must be an acceptable value.")


class WebLink(OrderedSchema):
    id = fields.UUID()
    title = fields.String()
    description = fields.String()
    url = fields.Url()
    rotted = fields.String(validate=validate_rot_status)
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
    rotted = fields.String(validate=validate_rot_status)
