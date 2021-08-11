from os import fspath
from importlib import import_module
from pathlib import Path

from flask import Flask, app
from flask_cors import CORS
from flask_smorest import Api
import sys_vars

from src import logger
from src.blueprints import all_blueprints
from src.core.database.schema import db


def create_app():
    """Create an instance of the app."""
    app = Flask(__name__)
    CORS(app)

    # Put the app secret key into the expected key
    app.config["SECRET_KEY"] = sys_vars.get("SECRET_KEY")
    app.config.update(sys_vars.get_json("api.json"))

    # Don't enable API docs in prod
    if app.config["ENV"] == "production":
        app.config["OPENAPI_URL_PREFIX"] = None

    # Create a database connection
    db_path = sys_vars.get_path("DB_PATH").resolve()
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{fspath(db_path)}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Create the database if needed
    if not db_path.exists():
        with app.app_context():
            db.create_all()

    # Add a file logger to record errors
    app.logger.addHandler(logger.file_handler())

    # Init API use handling
    api = Api(app)

    # Register the resources
    for bp in all_blueprints:
        import_module(bp.import_name)
        api.register_blueprint(bp)

    return app
