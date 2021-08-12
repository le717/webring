from marshmallow import fields, validate
import sys_vars

from src.core.models import OrderedSchema

AUTH_KEYS = sys_vars.get_json("AUTH_KEYS")


__all__ = ["AuthKey"]


class AuthKey(OrderedSchema):
    auth_key = fields.String(
        required=True,
        validate=lambda x: x in AUTH_KEYS,
        error_messages={"validator_failed": "Unrecognized auth key"},
    )
