from json import JSONDecodeError

import sys_vars
from flask import current_app


__all__ = ["get"]


def get() -> dict[str, str]:
    """Get meta information about this webring instance."""
    # Attempt to fetch the webring metadata json
    try:
        meta = sys_vars.get_json("webring.json", default={})
    except JSONDecodeError:
        meta = {}

    # If any required keys are missing, fill them back in
    required_keys = ["name", "maintainer", "home_url"]
    for k in required_keys:
        if k not in meta:
            meta[k] = ""

    return meta | {
        "software": "https://github.com/le717/webring",
        "version": current_app.config["API_VERSION"],
    }
