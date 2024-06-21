from collections.abc import Sequence
from typing import Any
from uuid import UUID

from flask import abort, request
from flask.views import MethodView

from src.blueprints import root
from src.core import database as db
from src.core.models import Generic, WebLink, auth


@root.route("/")
class WebRing(MethodView):
    @root.arguments(WebLink.RingArgs, location="query", as_kwargs=True)
    @root.response(200, WebLink.Entry(many=True))
    def get(self, **kwargs: Any) -> Sequence[db.schema.WebLink]:
        """Fetch all entries.

        Provide the appropriate query string arguments to
        filter the result set as desired.
        """
        # Remove the site making the request from the result set if told to
        if kwargs["exclude_origin"]:
            kwargs["http_origin"] = request.headers.get("ORIGIN")
            del kwargs["exclude_origin"]
        return db.weblink.get_all(**kwargs)

    @root.arguments(auth.AuthKey, location="query", as_kwargs=True)
    @root.arguments(WebLink.EntryCreate, location="json", as_kwargs=True)
    @root.response(201, WebLink.EntryId)
    def post(self, **kwargs: Any) -> dict[str, UUID]:
        """Create an entry."""
        del kwargs["auth_key"]
        return db.weblink.create(kwargs)


@root.route("/<uuid:id>")
class WebRingItem(MethodView):
    @root.arguments(auth.AuthKey, location="query", as_kwargs=True)
    @root.arguments(WebLink.EntryId, location="path", as_kwargs=True)
    @root.response(204, Generic.Empty)
    @root.alt_response(422, schema=Generic.HttpError)
    def delete(self, **kwargs: Any) -> None:
        """Delete an entry."""
        del kwargs["auth_key"]
        db.weblink.delete(str(kwargs["id"]))

    @root.arguments(auth.AuthKey, location="query", as_kwargs=True)
    @root.arguments(WebLink.EntryId, location="path", as_kwargs=True)
    @root.arguments(WebLink.EntryUpdate, location="json", as_kwargs=True)
    @root.response(204, Generic.Empty)
    @root.alt_response(400, schema=Generic.HttpError)
    @root.alt_response(422, schema=Generic.HttpError)
    def patch(self, **kwargs: Any) -> None:
        """Update an entry."""
        del kwargs["auth_key"]

        kwargs["id"] = str(kwargs["id"])
        if not db.weblink.update(kwargs):
            # TODO: Add response message
            abort(400)
