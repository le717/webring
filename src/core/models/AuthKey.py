from marshmallow import fields, Schema
import sys_vars


AUTH_KEYS = sys_vars.get_json("AUTH_KEYS")


__all__ = ["AuthKey"]


class AuthKey(Schema):
    auth_key = fields.String(
        required=True,
        validate=lambda x: x in AUTH_KEYS,
        error_messages={"validator_failed": "Unrecognized auth key"},
    )
