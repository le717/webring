from typing import Any, OrderedDict
from flask import abort
from flask.views import MethodView

from src.blueprints import root
from src.core import models

from src.core.database import weblink as db


@root.route("/")
class WebRing(MethodView):
    @root.response(200, models.WebLink(many=True))
    def get(self):
        """Fetch webring items.

        This will return rotted links in the result set.
        """
        return db.get_all(with_rotted=True)

    @root.arguments(models.AuthKey, location="query", as_kwargs=True)
    @root.arguments(models.WebLinkCreate, location="json", as_kwargs=True)
    @root.response(201, models.WebLinkId)
    def post(self, **kwargs: Any):
        """Create a webring item."""
        del kwargs["auth_key"]
        return db.create(kwargs)


@root.route("/<uuid:id>")
class WebRing(MethodView):
    @root.arguments(models.AuthKey, location="query", as_kwargs=True)
    @root.arguments(models.WebLinkId, location="path", as_kwargs=True)
    @root.response(204, models.Empty)
    def delete(self, **kwargs: Any):
        """Delete a webring item."""
        del kwargs["auth_key"]
        db.delete(str(kwargs["id"]))

    @root.arguments(models.AuthKey, location="query", as_kwargs=True)
    @root.arguments(models.WebLinkId, location="path", as_kwargs=True)
    @root.arguments(models.WebLinkUpdate, location="json", as_kwargs=True)
    @root.response(204, models.Empty)
    @root.alt_response(400, models.HttpError)
    def patch(self, **kwargs: Any):
        """Update a webring item."""
        del kwargs["auth_key"]

        kwargs["id"] = str(kwargs["id"])
        if not db.update(kwargs):
            abort(400)
