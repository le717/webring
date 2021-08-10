from flask_smorest import Blueprint


def _factory(partial_module_string: str, url_prefix: str) -> Blueprint:
    """Generate a blueprint registration."""
    import_path = f"src.views.{partial_module_string}"
    return Blueprint(partial_module_string, import_path, url_prefix=f"{url_prefix}")


root = _factory("access", "/")
bitrot = _factory("access", "/bitrot")

all_blueprints = (root, bitrot)
