import os
import pytest

os.environ["SYS_VARS_PATH"] = f"{os.getcwd()}/tests/secrets"

from src.app_factory import create_app
from src.core.database.schema import db
from tests.helpers import VALID_AUTH


@pytest.fixture
def app():
    os.environ["ENV"] = "testing"
    os.environ["DB_PATH"] = "tests/db/database.db"
    os.environ["AUTH_KEYS"] = f'["{VALID_AUTH}"]'
    os.environ["SECRET_KEY"] = "testing-secret-key"
    os.makedirs("tests/db")

    app = create_app()
    yield app

    with app.app_context():
        db.drop_all()
        os.unlink(os.environ["DB_PATH"])
        os.rmdir("tests/db")


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
