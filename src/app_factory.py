from os import fspath
from importlib import import_module
import logging

from alembic import command
from alembic.config import Config
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
import sys_vars

from src import logger
from src.blueprints import all_blueprints
from src.core.database.schema import db


def create_app():
    """Instance the app."""
    # Create the app and enable CORS support
    app = Flask(__name__)
    CORS(app)

    # Put the app secret key into the expected key
    app.config["SECRET_KEY"] = sys_vars.get("SECRET_KEY")
    app.config.update(sys_vars.get_json("api.json"))

    # Don't enable API docs in prod
    if app.config["ENV"] == "production":
        app.config["OPENAPI_URL_PREFIX"] = None

    # Add a file logger to record errors
    app.logger.addHandler(logger.file_handler("error-app.log"))

    # Enable Discord webhook event logging, falling back to a text log
    if sys_vars.get_bool("ENABLE_DISCORD_LOGGING"):
        logger.LINKROT.addHandler(logger.DiscordHandler())
    else:
        logger.LINKROT.addHandler(
            logger.file_handler("error-linkrot.log", linkrot=True)
        )

    # Register the API endpoints
    api = Api(app)
    for bp in all_blueprints:
        import_module(bp.import_name)
        api.register_blueprint(bp)

    # Create a database connection
    db_path = sys_vars.get_path("DB_PATH").resolve()
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path.as_posix()}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

        # Create the database if needed
        if not db_path.exists():
            db.create_all()

            # Tell Alembic this is a new database and we don't need
            # to update it to a newer schema
            alembic_cfg = Config("alembic.ini")
            command.stamp(alembic_cfg, "head")

    return app
