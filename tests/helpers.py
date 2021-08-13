import json
from urllib.parse import urlencode
from typing import Any, Union


__all__ = [
    "INVALID_AUTH",
    "VALID_AUTH",
    "authed_request",
    "from_json",
    "to_json",
    "item_all_good",
    "item_dead_url",
]


INVALID_AUTH = "unknown-auth-key"
VALID_AUTH = "known-auth-key"


def __auth_key(key: str) -> str:
    return f"{urlencode({'auth_key': key})}"


def authed_request(*args: str, **kwargs: Any) -> str:
    endpoint = "/".join(args)
    return f"{endpoint}?{__auth_key(kwargs['auth'])}".replace("//", "/")


def from_json(data: str) -> Union[dict, list]:
    return json.loads(data)


def to_json(data: Union[dict, list]) -> str:
    return json.dumps(data)


def item_dead_url() -> dict:
    return {
        "title": "A broken website",
        "description": "This is a broken website.",
        "url": "https://noooooooo.tld.that.does.not.exist.at.all",
    }


def item_all_good() -> dict:
    return {
        "title": "A working website",
        "description": "This is my website.",
        "url": "https://example.com",
    }
