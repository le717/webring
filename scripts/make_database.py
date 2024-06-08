import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

# We have to add the app path to the path to get the db
sys.path.insert(0, Path(__file__).parent.parent.as_posix())


from db.dummy_db import create_app
from src.core.database.schema import db


def create_database() -> None:
    """Create a brand new copy of the database."""
    app = create_app()
    with app.app_context():
        # Create the database tables if needed
        if not bool(inspect(db.engine).get_table_names()):
            print("Creating new database...")  # noqa: T201
            db.create_all()

            # Tell Alembic this is a new database and
            # we don't need to update it to a newer schema
            alembic_cfg = Config("alembic.ini")
            command.stamp(alembic_cfg, "head")


if __name__ == "__main__":
    create_database()
