from datetime import UTC, datetime
from sqlite3 import Connection as SQLite3Connection
from typing import Any, ClassVar

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, event, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


__all__ = ["Base", "LinkrotHistory", "WebLink"]


# Set up the flask-sqlalchemy extension for "new-style" models
class Base(DeclarativeBase): ...


db = SQLAlchemy(model_class=Base)


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record) -> None:  # noqa: ARG001
    """Make cascading deletes work on SQLite.

    Taken from https://stackoverflow.com/a/62327279
    """
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def now_in_utc() -> datetime:
    """Get the current datetime, expressed in UTC."""
    return datetime.now(tz=UTC)


class HelperMethods:
    def as_dict(self) -> dict[str, Any]:
        """Return a model as a dictionary."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def update_with(self, data: dict[str, Any], /) -> None:
        """Update a record with the given data."""
        for k, v in data.items():
            setattr(self, k, v)
        return None


class WebLink(HelperMethods, Base):
    __tablename__: str = "weblinks"
    __table_args__: ClassVar = {"comment": "Store the webring entries."}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]
    date_added: Mapped[datetime] = mapped_column(
        default=now_in_utc,
        onupdate=now_in_utc,
    )
    is_dead: Mapped[bool] = mapped_column(default=False)
    is_web_archive: Mapped[bool] = mapped_column(default=False)
    uuid: Mapped[str]

    history: Mapped[list["LinkrotHistory"]] = relationship(
        back_populates="entry", passive_deletes=True
    )


class LinkrotHistory(HelperMethods, Base):
    __tablename__: str = "linkrot_history"
    __table_args__: ClassVar = {"comment": "Audit log of linkrot checks."}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_checked: Mapped[datetime] = mapped_column(default=now_in_utc)
    url_checked: Mapped[str]
    was_alive: Mapped[bool] = mapped_column(default=True)
    message: Mapped[str] = mapped_column(default="")
    entry_id: Mapped[int] = mapped_column(
        ForeignKey("weblinks.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    entry: Mapped["WebLink"] = relationship(back_populates="history")
