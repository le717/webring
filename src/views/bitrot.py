from typing import Any
from flask.views import MethodView

from src.blueprints import bitrot
from src.core import models


@bitrot.route("/")
class BitrotCheck(MethodView):
    @bitrot.response(204, models.Empty)
    def post(self):
        return True
