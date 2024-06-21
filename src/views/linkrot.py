from typing import Any

from flask.views import MethodView
from flask_smorest import abort

from src.blueprints import linkrot
from src.core import database as db
from src.core.database.schema import LinkrotHistory
from src.core.models import Generic, WebLink, rot_result


@linkrot.route("/")
class LinkRotCheck(MethodView):
    @linkrot.response(200, rot_result.RotResult(many=True))
    @linkrot.alt_response(400, schema=Generic.HttpError)
    @linkrot.alt_response(403, schema=Generic.HttpError)
    @linkrot.alt_response(422, schema=Generic.HttpError)
    def post(self) -> list[db.linkrot.RotResult]:
        """Check all links in the ring for link rot."""
        return db.linkrot.check_all()


@linkrot.route("/<uuid:id>")
class LinkRotSingleCheck(MethodView):
    @linkrot.arguments(WebLink.EntryId, location="path", as_kwargs=True)
    @linkrot.response(200, rot_result.RotResult)
    @linkrot.alt_response(400, schema=Generic.HttpError)
    @linkrot.alt_response(403, schema=Generic.HttpError)
    @linkrot.alt_response(404, schema=Generic.HttpError)
    @linkrot.alt_response(422, schema=Generic.HttpError)
    def post(self, **kwargs: Any) -> db.linkrot.RotResult | None:
        """Check a single link in the ring for link rot."""
        if (result := db.linkrot.check_one(str(kwargs["id"]))) is None:
            abort(404, message="That ID does not exist in the webring.")
        return result


@linkrot.route("/<uuid:id>/history")
class History(MethodView):
    @linkrot.arguments(WebLink.EntryId, location="path", as_kwargs=True)
    @linkrot.response(200, rot_result.HistoryEntry(many=True))
    @linkrot.alt_response(400, schema=Generic.HttpError)
    @linkrot.alt_response(403, schema=Generic.HttpError)
    @linkrot.alt_response(404, schema=Generic.HttpError)
    @linkrot.alt_response(422, schema=Generic.HttpError)
    def get(self, **kwargs: Any) -> list[LinkrotHistory]:
        if (result := db.linkrot.get_history(str(kwargs["id"]))) is None:
            abort(404, message="Linkrot history is not available for this entry.")
        return result
