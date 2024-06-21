import os
from pathlib import Path
from typing import Any

import pytest


os.environ["SYS_VARS_PATH"] = (Path.cwd() / "tests" / "secrets").as_posix()

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

from src.app_factory import create_app
from src.core.database.schema import Base, db
from tests.helpers import VALID_AUTH


@pytest.fixture()
def app(tmp_path: Path):
    db_path: Path = tmp_path / "database.db"
    os.environ["ENV"] = "testing"
    os.environ["DB_PATH"] = db_path.as_posix()
    os.environ["AUTH_KEYS"] = f'["{VALID_AUTH}"]'
    os.environ["SECRET_KEY"] = "testing-secret-key"
    os.environ["TIMES_FAILED_THRESHOLD"] = "3"
    os.environ["ENABLE_DISCORD_LOGGING"] = "false"

    app = create_app()
    with app.app_context():
        # Create the database tables if needed
        if not bool(inspect(db.engine).get_table_names()):
            Base.metadata.create_all(db.engine)

            # Tell Alembic this is a new database and
            # we don't need to update it to a newer schema
            command.stamp(Config("alembic.ini"), "head")
    return app


@pytest.fixture()
def client(app) -> Any:
    return app.test_client()


@pytest.fixture()
def runner(app) -> Any:
    return app.test_cli_runner()
