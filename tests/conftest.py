import os
import pytest

os.environ["SYS_VARS_PATH"] = f"{os.getcwd()}/secrets"

from src.app_factory import create_app
from src.core.database.schema import db


@pytest.fixture
def app():
    os.environ["SECRET_KEY"] = "testing-secret-key"
    os.environ["DB_PATH"] = "tests/db/database.db"
    os.environ["ENV"] = "testing"
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
