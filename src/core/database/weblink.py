from datetime import datetime, timezone
import uuid
from typing import Optional, OrderedDict

from markupsafe import Markup

from src.core.database.schema import WebLink, db
from src.core.database.linkrot import check_one, delete as delete_rot


__all__ = ["create", "delete", "exists", "get", "get_all", "update"]


def create(data: OrderedDict) -> dict:
    """Create a single weblink."""
    entry_id = str(uuid.uuid4())
    weblink = WebLink(
        id=entry_id,
        title=Markup(data["title"]).striptags(),
        description=Markup(data["description"]).striptags(),
        url=Markup(data["url"]).striptags(),
        rotted="no",
        date_added=datetime.now(timezone.utc),
    )
    db.session.add(weblink)
    db.session.commit()
    db.session.refresh(weblink)

    # Check the linkrot status
    check_one(entry_id)
    return {"id": entry_id}


def delete(uuid: str) -> bool:
    """Delete a single weblink."""
    if not exists(uuid):
        return False

    db.session.delete(WebLink.query.filter_by(id=uuid).first())
    db.session.commit()
    delete_rot(uuid)
    return True


def exists(uuid: str) -> bool:
    """Determine if a weblink exists."""
    return WebLink.query.filter_by(id=uuid).first() is not None


def get(uuid: str) -> Optional[WebLink]:
    """Get a single weblink."""
    return WebLink.query.filter_by(id=uuid).first()


def get_all(with_rotted: bool = False) -> list[WebLink]:
    """Get all weblinks."""
    filters = []
    if not with_rotted:
        filters.append(WebLink.rotted != "yes")
    return WebLink.query.filter(*filters).all()


def update(data: OrderedDict) -> bool:
    """Update a weblink."""
    if not exists(data["id"]):
        return False

    db.session.query(WebLink).filter_by(id=data["id"]).update(
        data, synchronize_session="fetch"
    )
    db.session.commit()

    # Check the linkrot status if the url was changed
    if "url" in data:
        check_one(data["id"])
    return True
