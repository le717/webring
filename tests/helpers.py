import json
from typing import Any
from urllib.parse import urlencode


__all__ = [
    "INVALID_AUTH",
    "VALID_AUTH",
    "authed_request",
    "entry_all_good",
    "entry_dead_url",
    "entry_web_archive_url",
    "from_json",
    "to_json",
]


INVALID_AUTH = "unknown-auth-key"
VALID_AUTH = "known-auth-key"


def __auth_key(key: str) -> str:
    return f"{urlencode({"auth_key": key})}"


def authed_request(*args: str, **kwargs: Any) -> str:
    endpoint = "/".join(args)
    return f"{endpoint}?{__auth_key(kwargs["auth"])}".replace("//", "/")


def from_json(data: str) -> dict | list:
    return json.loads(data)


def to_json(data: dict | list) -> str:
    return json.dumps(data)


def entry_dead_url() -> dict[str, str]:
    return {
        "title": "A broken website",
        "description": "This is a broken website.",
        "url": "https://noooooooo.tld.that.does.not.exist.at.all",
    }


def entry_web_archive_url() -> dict[str, str]:
    return {
        "title": "A Web Archive only website",
        "description": "This is a website that is only available via the Web Archive.",
        "url": "https://triangle717.wordpress.com",
    }


def entry_all_good() -> dict[str, str]:
    return {
        "title": "A working website",
        "description": "This is my website.",
        "url": "https://example.com",
    }
