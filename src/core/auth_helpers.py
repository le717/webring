from collections.abc import Callable
from functools import wraps
from typing import Any

import sys_vars
from flask import request
from flask_smorest import abort


__all__ = ["protect_blueprint", "protect_route"]


def protect_blueprint() -> None:
    """Protect a whole blueprint with an auth key."""
    # Was an Authorization header sent?
    if request.authorization is None:
        abort(400, message="Missing HTTP Authorization header.")

    # Make sure it's a Bearer token method
    if request.authorization.type != "bearer":
        abort(400, message="Invalid authorization type.")

    # Attempt to get the auth key and validate it
    try:
        auth_keys = sys_vars.get_json("AUTH_KEYS")
        if request.authorization.token not in auth_keys:
            raise KeyError
        return None
    except (IndexError, KeyError):
        abort(403, message="Invalid auth key provided.")


def protect_route(*args) -> Callable[..., Any]:  # noqa: ARG001
    """Protect a single endpoint with an auth key.

    This decorator is useful when a single endpoint
    needs to be protected but not the entire blueprint.
    """

    def decorator(func) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable[..., Any]:
            protect_blueprint()

            return func(*args, **kwargs)

        return wrapper

    return decorator
