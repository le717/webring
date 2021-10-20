from datetime import datetime, timezone
import uuid
from typing import Any, Optional, OrderedDict

from markupsafe import Markup

from src.logger import LINKROT
from src.core.database.schema import WebLink, db


__all__ = ["create", "delete", "exists", "get", "get_all", "update"]


def create(data: OrderedDict) -> dict:
    """Create a single weblink."""
    entry_id = str(uuid.uuid4())
    weblink = WebLink(
        id=entry_id,
        title=Markup(data["title"]).striptags(),
        description=Markup(data["description"]).striptags(),
        url=Markup(data["url"]).striptags(),
        date_added=datetime.now(timezone.utc),
    )
    db.session.add(weblink)
    db.session.commit()
    db.session.refresh(weblink)
    LINKROT.info(
        {
            "id": entry_id,
            "url": weblink.url,
            "message": "Link has been added to the webring.",
        }
    )
    return {"id": entry_id}


def delete(uuid: str) -> bool:
    """Delete a single weblink."""
    if not exists(uuid):
        return False

    db.session.delete(get(uuid))
    db.session.commit()
    LINKROT.info(
        {
            "id": uuid,
            "url": "N/A",
            "message": "Link has been deleted from the webring.",
        }
    )
    return True


def exists(uuid: str) -> bool:
    """Determine if a weblink exists."""
    return get(uuid) is not None


def get(uuid: str) -> Optional[WebLink]:
    """Get a single weblink."""
    return WebLink.query.filter_by(id=uuid).first()


def get_all(with_rotted: bool = False, **kwargs: Any) -> list[WebLink]:
    """Get all weblinks."""
    filters = []

    # Filter out the site in the weblink we are on
    if origin := kwargs.get("http_origin"):
        filters.append(WebLink.url != origin)

    # Remove all rotted links
    if not with_rotted:
        filters.append(WebLink.is_dead != "1")
    wbs = WebLink.query.filter(*filters).all()

    # Adjust the title of the link depending on status
    for wb in wbs:
        if wb.is_dead:
            wb.title += " (Dead link)"
        elif wb.is_web_archive:
            wb.title += " (Web Archive link)"
    return wbs


def update(data: OrderedDict) -> bool:
    """Update a weblink."""
    if not exists(data["id"]):
        return False

    db.session.query(WebLink).filter_by(id=data["id"]).update(
        {k: Markup(v).striptags() for k, v in data.items() if k != "id"},
        synchronize_session="fetch",
    )
    db.session.commit()
    LINKROT.info(
        {
            "id": data["id"],
            "url": "N/A",
            "message": f"Link has been updated with the following info: `{data}`",
        }
    )
    return True
