import os
from pathlib import Path

import pytest

os.environ["SYS_VARS_PATH"] = (Path.cwd() / "tests" / "secrets").as_posix()

from src.app_factory import create_app
from src.core.database.schema import db
from tests.helpers import VALID_AUTH


@pytest.fixture
def app():
    os.environ["ENV"] = "testing"
    os.environ["DB_PATH"] = "tests/db/database.db"
    os.environ["AUTH_KEYS"] = f'["{VALID_AUTH}"]'
    os.environ["SECRET_KEY"] = "testing-secret-key"
    os.environ["TIMES_FAILED_THRESHOLD"] = "3"
    os.environ["ENABLE_DISCORD_LOGGING"] = "false"
    Path("tests/db").mkdir(parents=True, exist_ok=True)

    app = create_app()
    yield app

    with app.app_context():
        db.drop_all()
        Path(os.environ["DB_PATH"]).unlink()
        Path("tests/db").rmdir()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
