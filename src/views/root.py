from collections.abc import Sequence
from typing import Any
from uuid import UUID

from flask import abort, request
from flask.views import MethodView

from src.blueprints import root
from src.core import database as db
from src.core import models


@root.route("/")
class WebRing(MethodView):
    @root.arguments(models.WebLinkGet, location="query", as_kwargs=True)
    @root.response(200, models.WebLink(many=True))
    def get(self, **kwargs: Any) -> Sequence[db.schema.WebLink]:
        """Fetch webring items.

        Provide the appropriate query string arguments to
        filter the result set as desired.
        """
        # Remove the site making the request from the result set if told to
        query_args = {}
        if kwargs["exclude_origin"]:
            query_args["http_origin"] = request.headers.get("ORIGIN")
        return db.weblink.get_all(include_rotted=kwargs["include_rotted"], **query_args)

    @root.arguments(models.AuthKey, location="query", as_kwargs=True)
    @root.arguments(models.WebLinkCreate, location="json", as_kwargs=True)
    @root.response(201, models.WebLinkId)
    def post(self, **kwargs: Any) -> dict[str, UUID]:
        """Create a webring item."""
        del kwargs["auth_key"]
        return db.weblink.create(kwargs)


@root.route("/<uuid:id>")
class WebRing(MethodView):
    @root.arguments(models.AuthKey, location="query", as_kwargs=True)
    @root.arguments(models.WebLinkId, location="path", as_kwargs=True)
    @root.response(204, models.Empty)
    def delete(self, **kwargs: Any) -> None:
        """Delete a webring item."""
        del kwargs["auth_key"]
        db.weblink.delete(str(kwargs["id"]))

    @root.arguments(models.AuthKey, location="query", as_kwargs=True)
    @root.arguments(models.WebLinkId, location="path", as_kwargs=True)
    @root.arguments(models.WebLinkUpdate, location="json", as_kwargs=True)
    @root.response(204, models.Empty)
    @root.alt_response(400, schema=models.HttpError)
    def patch(self, **kwargs: Any) -> None:
        """Update a webring item."""
        del kwargs["auth_key"]

        kwargs["id"] = str(kwargs["id"])
        if not db.weblink.update(kwargs):
            abort(400)
