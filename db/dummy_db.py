import sys
from pathlib import Path

import sys_vars
from flask import Flask


# We have to add the app path to the path to get the db schema
sys.path.insert(0, Path(__file__).parent.parent.as_posix())

from src.core.database.schema import db


def create_app() -> Flask:
    """Dummy Flask instance used for database management."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret tunnel"

    db_path = sys_vars.get_path("DB_PATH").resolve()
    with app.app_context():
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path.as_posix()}"
        db.init_app(app)
    return app
