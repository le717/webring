from typing import Any
from flask.views import MethodView

from src.blueprints import bitrot
from src.core import models
from src.core.database import bitrot as db


@bitrot.route("/")
class BitrotCheck(MethodView):
    @bitrot.arguments(models.AuthKey, location="query", as_kwargs=True)
    @bitrot.response(200, models.RotResult(many=True))
    def post(self, **kwargs: Any):
        """Check all links in the ring for link rot."""
        del kwargs["auth_key"]
        return db.check_all()


@bitrot.route("/<uuid:id>")
class BitrotSingleCheck(MethodView):
    @bitrot.arguments(models.AuthKey, location="query", as_kwargs=True)
    @bitrot.arguments(models.WebLinkId, location="path", as_kwargs=True)
    @bitrot.response(200, models.RotResult)
    def post(self, **kwargs: Any):
        """Check a single link in the ring for link rot."""
        del kwargs["auth_key"]
        return db.check_one(str(kwargs["id"]))
