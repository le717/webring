from typing import Any

from flask.views import MethodView
from flask_smorest import abort

from src.blueprints import linkrot
from src.core import database as db
from src.core import models
from src.core.models import Generic


@linkrot.route("/")
class LinkRotCheck(MethodView):
    @linkrot.arguments(models.AuthKey, location="query", as_kwargs=True)
    @linkrot.response(200, models.RotResult(many=True))
    @linkrot.alt_response(422, schema=Generic.HttpError)
    def post(self, **kwargs: Any) -> list[db.linkrot.RotResult]:
        """Check all links in the ring for link rot."""
        del kwargs["auth_key"]
        return db.linkrot.check_all()


@linkrot.route("/<uuid:id>")
class LinkRotSingleCheck(MethodView):
    @linkrot.arguments(models.AuthKey, location="query", as_kwargs=True)
    @linkrot.arguments(models.WebLinkId, location="path", as_kwargs=True)
    @linkrot.response(200, models.RotResult)
    @linkrot.alt_response(404, schema=Generic.HttpError)
    @linkrot.alt_response(422, schema=Generic.HttpError)
    def post(self, **kwargs: Any) -> db.linkrot.RotResult | None:
        """Check a single link in the ring for link rot."""
        del kwargs["auth_key"]
        if (result := db.linkrot.check_one(str(kwargs["id"]))) is None:
            # TODO: Make this message display in the response
            abort(404, message="That ID does not exist in the webring.")
        return result
