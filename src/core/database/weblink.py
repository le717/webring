import uuid
from datetime import UTC, datetime
from typing import Any

from markupsafe import Markup
from sqlalchemy import func

from src.core.database.schema import WebLink, db
from src.core.logger import logger

__all__ = ["create", "delete", "exists", "get", "get_all", "update"]


def create(data: dict) -> dict[str, uuid.UUID]:
    """Create a single weblink."""
    entry_id = str(uuid.uuid4())
    weblink = WebLink(
        id=entry_id,
        title=Markup(data["title"]).striptags(),
        description=Markup(data["description"]).striptags(),
        url=Markup(data["url"]).striptags(),
        date_added=datetime.now(UTC),
    )
    db.session.add(weblink)
    db.session.commit()
    db.session.refresh(weblink)
    logger.info({
        "id": entry_id,
        "url": weblink.url,
        "message": "Link has been added to the webring.",
    })
    return {"id": entry_id}


def delete(uuid: str) -> bool:
    """Delete a single weblink."""
    if not exists(uuid):
        return False

    db.session.delete(get(uuid))
    db.session.commit()
    logger.info({
        "id": uuid,
        "url": "N/A",
        "message": "Link has been deleted from the webring.",
    })
    return True


def exists(uuid: str) -> bool:
    """Determine if a weblink exists."""
    return get(uuid) is not None


def get(uuid: str) -> WebLink | None:
    """Get a single weblink."""
    return db.session.execute(db.select(WebLink).filter_by(id=uuid)).scalar_one_or_none()


def get_all(include_rotted: bool = False, **kwargs: Any) -> list[WebLink]:
    """Get all weblinks."""
    filters = []

    # Filter out the site in the weblink we are on.
    # Make sure we normalize the casing of the two URLs to better ensure we filter correctly
    if origin := kwargs.get("http_origin"):
        filters.append(func.lower(WebLink.url) != func.lower(origin))

    # Remove all rotted links
    if not include_rotted:
        filters.append(WebLink.is_dead != "1")
    wbs = db.session.execute(db.select(WebLink).filter(*filters)).scalars().all()

    # Adjust the title of the link depending on status
    for wb in wbs:
        if wb.is_dead:
            wb.title += " (Dead link)"
        elif wb.is_web_archive:
            wb.title += " (Web Archive link)"
    return wbs


def update(data: dict) -> bool:
    """Update a weblink."""
    wb_id = data.pop("id")
    if (wb := get(wb_id)) is None:
        return False

    wb.update_with(data)
    db.session.commit()
    logger.info({
        "id": wb_id,
        "url": "N/A",
        "message": f"Link has been updated with the following info: `{data}`",
    })
    return True
