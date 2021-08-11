from datetime import datetime, timezone
import uuid
from typing import OrderedDict


from src.core.database.schema import WebLink, db


__all__ = ["create", "delete", "exists", "get", "update"]


def create(data: OrderedDict) -> dict:
    """Create a single weblink."""
    entry_id = str(uuid.uuid4())
    weblink = WebLink(
        id=entry_id,
        title=data["title"],
        description=data["description"],
        url=data["url"],
        rotted="no",
        date_added=datetime.now(timezone.utc),
    )
    db.session.add(weblink)
    db.session.commit()
    db.session.refresh(weblink)
    return {"id": entry_id}


def delete(uuid: str) -> bool:
    """Delete a single weblink."""
    if not exists(uuid):
        return False

    db.session.delete(WebLink.query.filter_by(id=uuid).first())
    db.session.commit()
    return True


def exists(uuid: str) -> bool:
    """Determine if a weblink exists."""
    return WebLink.query.filter_by(id=uuid).first() is not None


def get() -> list[WebLink]:
    """Get all weblinks."""
    return WebLink.query.all()


def update():
    ...
