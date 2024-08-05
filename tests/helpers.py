from werkzeug.datastructures import Headers


__all__ = [
    "INVALID_AUTH",
    "VALID_AUTH",
    "entry_all_good",
    "entry_dead_url",
    "entry_web_archive_url",
    "make_auth",
    "make_url",
]


INVALID_AUTH = "unknown-auth-key"
VALID_AUTH = "known-auth-key"


def make_auth(key: str) -> Headers:
    return Headers({"Authorization": f"Bearer {key}"})


def make_url(*args: str) -> str:
    return "/".join(args).replace("//", "/")


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
