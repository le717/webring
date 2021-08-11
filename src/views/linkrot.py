from typing import Any
from flask.views import MethodView

from src.blueprints import linkrot
from src.core import models
from src.core.database import linkrot as db


@linkrot.route("/")
class LinkRotCheck(MethodView):
    @linkrot.arguments(models.AuthKey, location="query", as_kwargs=True)
    @linkrot.response(200, models.RotResult(many=True))
    def post(self, **kwargs: Any):
        """Check all links in the ring for link rot."""
        del kwargs["auth_key"]
        return db.check_all()


@linkrot.route("/<uuid:id>")
class LinkRotSingleCheck(MethodView):
    @linkrot.arguments(models.AuthKey, location="query", as_kwargs=True)
    @linkrot.arguments(models.WebLinkId, location="path", as_kwargs=True)
    @linkrot.response(200, models.RotResult)
    def post(self, **kwargs: Any):
        """Check a single link in the ring for link rot."""
        del kwargs["auth_key"]
        return db.check_one(str(kwargs["id"]))
