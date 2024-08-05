import sys_vars
from flask import current_app


__all__ = ["get"]


def get() -> dict[str, str]:
    """Get meta information about this webring instance."""
    return sys_vars.get_json("webring.json") | {
        "software": "https://github.com/le717/webring",
        "version": current_app.config["API_VERSION"],
    }
