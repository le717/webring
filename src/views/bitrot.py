from typing import Any
from flask.views import MethodView

from src.blueprints import bitrot
from src.core import models
from src.core.database import bitrot as db


@bitrot.route("/")
class BitrotCheck(MethodView):
    @bitrot.response(200, models.RotResult(many=True))
    def post(self):
        return db.check_all()


@bitrot.route("/<uuid:uuid>")
class BitrotSingleCheck(MethodView):
    @bitrot.response(200, models.RotResult)
    def post(self, uuid: str):
        return db.check_one(str(uuid))
