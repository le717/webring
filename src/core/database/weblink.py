import uuid
from datetime import UTC, datetime
from typing import Any

from markupsafe import Markup
from sqlalchemy import func

from src.core.database.schema import Entry, db
from src.core.logger import logger


__all__ = ["create", "delete", "get", "get_all", "update"]


def create(data: dict) -> dict[str, uuid.UUID]:
    """Create an entry."""
    entry_id = str(uuid.uuid4())
    entry = Entry(
        uuid=entry_id,
        title=Markup(data["title"]).striptags(),
        description=Markup(data["description"]).striptags(),
        url=Markup(data["url"]).striptags(),
        date_added=datetime.now(tz=UTC),
    )
    db.session.add(entry)
    db.session.commit()
    db.session.refresh(entry)
    logger.info({
        "id": entry_id,
        "url": entry.url,
        "message": "Entry has been added to the webring.",
    })
    return {"id": entry_id}


def delete(uuid: str) -> bool:
    """Delete an entry."""
    if (entry := get(uuid)) is None:
        return False

    db.session.delete(entry)
    db.session.commit()
    logger.info({
        "id": uuid,
        "url": "N/A",
        "message": "Entry has been deleted from the webring.",
    })
    return True


def get(uuid: str) -> Entry | None:
    """Get an entry."""
    return db.session.execute(db.select(Entry).filter_by(uuid=uuid)).scalar_one_or_none()


def get_all(**kwargs: Any) -> list[Entry]:
    """Get all entries."""
    filters = []

    # Filter out the site in the entry we are on.
    # Make sure we normalize the casing of the two URLs to better ensure we filter correctly
    if origin := kwargs.get("http_origin"):
        filters.append(func.lower(Entry.url) != func.lower(origin))

    # Filter out dead and/or Web Archive only links
    if not kwargs["include_rotted"]:
        filters.append(Entry.is_dead == False)
    if not kwargs["include_web_archive"]:
        filters.append(Entry.is_web_archive == False)
    entries = db.session.execute(db.select(Entry).filter(*filters)).scalars().all()

    # Adjust the title of the link depending on status
    for entry in entries:
        if entry.is_dead:
            entry.title += " (Dead link)"
        elif entry.is_web_archive:
            entry.title += " (Web Archive link)"
    return entries


def update(data: dict) -> bool:
    """Update an entry."""
    uuid = data.pop("id")
    if (entry := get(uuid)) is None:
        return False

    entry.update_with(data)
    db.session.commit()
    logger.info({
        "id": uuid,
        "url": "N/A",
        "message": f"Entry has been updated with the following info: `{data}`",
    })
    return True
