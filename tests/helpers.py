import json
from urllib.parse import urlencode
from typing import Any, Union


__all__ = [
    "INVALID_AUTH",
    "VALID_AUTH",
    "authed_request",
    "to_json",
    "invalid_item",
    "valid_item",
]


INVALID_AUTH = "unknown-auth-key"
VALID_AUTH = "known-auth-key"


def __auth_key(key: str) -> str:
    return f"{urlencode({'auth_key': key})}"


def authed_request(*args: str, **kwargs: Any) -> str:
    endpoint = "/".join(args)
    return f"{endpoint}?{__auth_key(kwargs['auth'])}"


def to_json(data) -> Union[dict, list]:
    return json.loads(data)


def invalid_item() -> dict:
    return {
        "title": "A broken website",
        "description": "This is a broken website.",
        "url": "https://nooooooooOo0.tld.that.does.not.exist.at.all",
    }


def valid_item() -> dict:
    return {
        "title": "A working website",
        "description": "This is my website.",
        "url": "https://example.com",
    }
