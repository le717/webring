from flask import Blueprint
from flask_smorest import Blueprint as APIBlueprint

from src.core.auth_helpers import protect_blueprint


__all__ = ["all_blueprints", "route_embed"]


def _api_factory(
    partial_module_string: str,
    url_prefix: str,
    *,
    protected: bool = False,
    description: str = "",
) -> APIBlueprint:
    """Generate a blueprint registration."""
    import_path = f"src.views.{partial_module_string}"
    blueprint = APIBlueprint(
        partial_module_string, import_path, url_prefix=url_prefix, description=description
    )

    if protected:
        blueprint.before_request(protect_blueprint)
        blueprint.description += (
            "\n\n<strong>Note</strong>: This endpoint can only be used with an auth key "
            "with the appropriate permissions."
        )
    else:
        blueprint.description += (
            "\n\n<strong>Note</strong>: Some endpoints may require an API key "
            "with the appropriate permissions."
        )
    return blueprint


root = _api_factory("root", "/")
linkrot = _api_factory("linkrot", "/linkrot", protected=True)

all_blueprints = (root, linkrot)
route_embed = Blueprint("embed", "src.views.embed", url_prefix="/webring-embed.js")
