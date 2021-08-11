from flask import abort, request
import sys_vars


API_KEY = sys_vars.get("API_KEY")


def enforce_key():
    if "key" not in request.args:
        abort(422)

    if request.args["key"] != API_KEY:
        abort(403)
