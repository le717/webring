from typing import Any

from flask.views import MethodView
from flask_smorest import abort

from src.blueprints import linkrot
from src.core import database as db
from src.core.models import Generic, WebLink, auth, rot_result


@linkrot.route("/")
class LinkRotCheck(MethodView):
    @linkrot.arguments(auth.AuthKey, location="query", as_kwargs=True)
    @linkrot.response(200, rot_result.RotResult(many=True))
    @linkrot.alt_response(422, schema=Generic.HttpError)
    def post(self, **kwargs: Any) -> list[db.linkrot.RotResult]:
        """Check all links in the ring for link rot."""
        del kwargs["auth_key"]
        return db.linkrot.check_all()


@linkrot.route("/<uuid:id>")
class LinkRotSingleCheck(MethodView):
    @linkrot.arguments(auth.AuthKey, location="query", as_kwargs=True)
    @linkrot.arguments(WebLink.EntryId, location="path", as_kwargs=True)
    @linkrot.response(200, rot_result.RotResult)
    @linkrot.alt_response(404, schema=Generic.HttpError)
    @linkrot.alt_response(422, schema=Generic.HttpError)
    def post(self, **kwargs: Any) -> db.linkrot.RotResult | None:
        """Check a single link in the ring for link rot."""
        del kwargs["auth_key"]
        if (result := db.linkrot.check_one(str(kwargs["id"]))) is None:
            abort(404, message="That ID does not exist in the webring.")
        return result
