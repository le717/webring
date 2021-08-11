from marshmallow import fields, validate
import sys_vars

from src.core.models import OrderedSchema

AUTH_KEY = sys_vars.get("AUTH_KEY")


__all__ = ["AuthKey"]


class AuthKey(OrderedSchema):
    auth_key = fields.String(
        required=True,
        validate=lambda x: x == AUTH_KEY,
        error_messages={"validator_failed": "Unrecognized auth key"},
    )
