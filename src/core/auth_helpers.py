from collections.abc import Callable
from functools import wraps
from typing import Any

import sys_vars
from flask import request
from flask_smorest import abort
from httpx import codes


__all__ = ["protect_blueprint", "protect_route"]

AUTH_KEYS = sys_vars.get_json("AUTH_KEYS")


def protect_blueprint() -> None:
    """Protect a whole blueprint with an auth key."""
    # Was an Authorization header sent?
    if request.authorization is None:
        abort(codes.BAD_REQUEST, message="Missing HTTP Authorization header.")

    # Make sure it's a Bearer token method
    if request.authorization.type != "bearer":
        abort(codes.BAD_REQUEST, message="Invalid authorization type.")

    # Attempt to get the auth key and validate it
    if request.authorization.token not in AUTH_KEYS:
        abort(codes.FORBIDDEN, message="Unknown auth key provided.")
    return None


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
