from importlib import import_module

import sys_vars
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from src.blueprints import all_blueprints, route_embed
from src.core import logger
from src.core.database.schema import db


def create_app() -> Flask:
    """Instance the app."""
    # Create the app and enable CORS support
    app = Flask(__name__)
    CORS(app)

    # Put the app secret key into the expected key
    app.config["SECRET_KEY"] = sys_vars.get("SECRET_KEY")
    app.config.update(sys_vars.get_json("api.json"))

    # Don't enable API docs in prod
    if sys_vars.get("FLASK_ENV") == "production":
        app.config["OPENAPI_URL_PREFIX"] = None

    # Set up a file logger, additionally enabling the Discord webhook event logging if requested
    logger.logger.addHandler(logger.file_handler("error-linkrot.log", linkrot=True))
    if sys_vars.get_bool("ENABLE_DISCORD_LOGGING"):
        logger.logger.addHandler(logger.DiscordHandler())

    # Register the API endpoints
    api = Api(app)
    for bp in all_blueprints:
        import_module(bp.import_name)
        api.register_blueprint(bp)

    # Register the embed endpoint
    import_module(route_embed.import_name)
    app.register_blueprint(route_embed)

    # Create a database connection
    db_path = sys_vars.get_path("DB_PATH").resolve()
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path.as_posix()}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

    return app
