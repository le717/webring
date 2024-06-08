from flask import Response, make_response, render_template, request

from src.core.database import weblink as db
from src.core.models.WebLink import WebLink

from ..blueprints import route_embed


@route_embed.get("")
def embed() -> Response:
    """Get a small JavaScript file that automatically embeds the webring on your site."""
    # Get all current links in the webring, including dead links, excluding the current site,
    # and convert them to plain dictionaries for including in the JavaScript file directly,
    # which removes the need for a fetch request on the client
    all_links = WebLink(only=["id", "url", "title", "description"]).dump(
        db.get_all(include_rotted=True, http_origin=request.headers.get("ORIGIN")),
        many=True,
    )

    # Render the JavaScript module, taking care to indicate it's a JS file
    # so browsers correctly load it
    resp = make_response(render_template("webring-embed.js", **{"all_links": all_links}))
    resp.mimetype = "text/javascript"
    return resp
