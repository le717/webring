from flask import Blueprint as FlBlueprint
from flask_smorest import Blueprint


__all__ = ["all_blueprints", "route_embed"]


def _factory(partial_module_string: str, url_prefix: str) -> Blueprint:
    """Generate a blueprint registration."""
    import_path = f"src.views.{partial_module_string}"
    return Blueprint(partial_module_string, import_path, url_prefix=url_prefix)


root = _factory("root", "/")
linkrot = _factory("linkrot", "/linkrot")

all_blueprints = (root, linkrot)
route_embed = FlBlueprint("embed", "src.views.embed", url_prefix="/webring-embed.js")
