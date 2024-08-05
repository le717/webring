from collections.abc import Sequence
from typing import Any
from uuid import UUID

from flask import abort, request
from flask.views import MethodView

from src.blueprints import root
from src.core import database as db
from src.core.auth_helpers import protect_route
from src.core.models import Generic, WebLink


@root.route("/")
class WebRing(MethodView):
    @root.arguments(WebLink.RingArgs, location="query", as_kwargs=True)
    @root.response(200, WebLink.Entry(many=True))
    def get(self, **kwargs: Any) -> Sequence[db.schema.Entry]:
        """Fetch all entries.

        Provide the appropriate query string arguments to
        filter the result set as desired.
        """
        # Remove the site making the request from the result set if told to
        if kwargs["exclude_origin"]:
            kwargs["http_origin"] = request.headers.get("ORIGIN")
            del kwargs["exclude_origin"]
        return db.weblink.get_all(**kwargs)

    @protect_route()
    @root.arguments(WebLink.EntryCreate, location="json", as_kwargs=True)
    @root.response(201, WebLink.EntryId)
    @root.alt_response(400, schema=Generic.HttpError)
    @root.alt_response(403, schema=Generic.HttpError)
    def post(self, **kwargs: Any) -> dict[str, UUID]:
        """Create an entry."""
        return db.weblink.create(kwargs)


@root.route("/<uuid:id>")
class WebRingItem(MethodView):
    @protect_route()
    @root.arguments(WebLink.EntryId, location="path", as_kwargs=True)
    @root.response(204, Generic.Empty)
    @root.alt_response(400, schema=Generic.HttpError)
    @root.alt_response(403, schema=Generic.HttpError)
    @root.alt_response(422, schema=Generic.HttpError)
    def delete(self, **kwargs: Any) -> None:
        """Delete an entry."""
        db.weblink.delete(str(kwargs["id"]))

    @protect_route()
    @root.arguments(WebLink.EntryId, location="path", as_kwargs=True)
    @root.arguments(WebLink.EntryUpdate, location="json", as_kwargs=True)
    @root.response(204, Generic.Empty)
    @root.alt_response(400, schema=Generic.HttpError)
    @root.alt_response(403, schema=Generic.HttpError)
    @root.alt_response(422, schema=Generic.HttpError)
    def patch(self, **kwargs: Any) -> None:
        """Update an entry."""
        kwargs["id"] = str(kwargs["id"])
        if not db.weblink.update(kwargs):
            abort(400, message="Unable to update entry with revised details.")
