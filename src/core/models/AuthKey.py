import sys_vars
from marshmallow import Schema, fields

AUTH_KEYS = sys_vars.get_json("AUTH_KEYS")


__all__ = ["AuthKey"]


class AuthKey(Schema):
    auth_key = fields.String(
        required=True,
        validate=lambda x: x in AUTH_KEYS,
        error_messages={"validator_failed": "Unrecognized auth key"},
    )
