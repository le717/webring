from datetime import UTC, datetime
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String


__all__ = ["Base", "RottedLinks", "WebLink"]


# Set up the flask-sqlalchemy extension for "new-style" models
class Base(DeclarativeBase): ...


db = SQLAlchemy(model_class=Base)


def now_in_utc() -> datetime:
    """Get the current datetime, expressed in UTC."""
    return datetime.now(tz=UTC)


class HelperMethods:
    def as_dict(self) -> dict[str, Any]:
        """Return a model as a dictionary."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def update_with(self, data: dict[str, Any]) -> None:
        """Update a record with the given data."""
        for k, v in data.items():
            setattr(self, k, v)
        return None


class WebLink(HelperMethods, Base):
    __tablename__ = "weblinks"
    __table_args__ = {"comment": "Store the webring entries."}

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(
        String,
    )
    date_added: Mapped[datetime] = mapped_column(
        nullable=False,
        default=now_in_utc,
        onupdate=now_in_utc,
    )
    is_dead: Mapped[bool] = mapped_column(default=False)
    is_web_archive: Mapped[bool] = mapped_column(default=False)


class RottedLinks(HelperMethods, Base):
    __tablename__ = "rotted_links"
    __table_args__ = {"comment": "Log rotting webring entries."}

    id: Mapped[str] = mapped_column(String, primary_key=True)
    times_failed: Mapped[int] = mapped_column(Integer)
