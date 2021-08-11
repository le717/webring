from typing import OrderedDict
from flask.views import MethodView
from flask_smorest import abort

from src.blueprints import root
from src.core import models

from src.core.database import weblink as db


@root.route("/")
class WebRing(MethodView):
    @root.response(200, models.WebLink(many=True))
    def get(self):
        """Fetch webring items."""
        return db.get()

    @root.arguments(models.WebLinkCreate, location="json")
    @root.response(201, models.WebLinkId)
    def post(self, data: OrderedDict):
        """Create a webring item."""
        return db.create(data)

    @root.arguments(models.WebLinkId, location="json")
    @root.response(204, models.Empty)
    def delete(self, data: OrderedDict):
        """Delete a webring item."""
        db.delete(str(data["id"]))
