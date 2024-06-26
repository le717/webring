from flask import Response, make_response, render_template, request
from webargs.flaskparser import use_kwargs

from src.blueprints import route_embed
from src.core.database import weblink as db
from src.core.models.WebLink import Entry, RingArgs


__all__ = ["embed"]


@route_embed.get("")
@use_kwargs(RingArgs().fields, location="query")
def embed(**kwargs) -> Response:
    """Get a small JavaScript file that automatically embeds the webring on your site.

    Provide the appropriate query string arguments to filter the result set as desired.
    """
    # Remove the site making the request from the result set if told to
    if kwargs["exclude_origin"]:
        kwargs["http_origin"] = request.headers.get("ORIGIN")
        del kwargs["exclude_origin"]

    # Get all current links in the webring, including dead links, excluding the current site,
    # and convert them to plain dictionaries for including in the JavaScript file directly,
    # which removes the need for a fetch request on the client
    all_links = Entry(only=["uuid", "url", "title", "description"]).dump(
        db.get_all(**kwargs),
        many=True,
    )

    # Render the JavaScript module, taking care to indicate it's a JS file
    # so browsers correctly load it
    resp = make_response(render_template("webring-embed.js", all_links=all_links))
    resp.mimetype = "text/javascript"
    return resp
