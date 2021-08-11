from flask import abort, request
import sys_vars


API_KEY = sys_vars.get("API_KEY")


def enforce_key():
    """Enfore an API key for changing the webring."""
    # Don't require a key to view the webring
    if request.blueprint == "root" and request.method == "GET":
        return None

    # Make sure a key is present
    if "key" not in request.args:
        abort(422)

    # Make sure the key is correct
    if request.args["key"] != API_KEY:
        abort(403)
