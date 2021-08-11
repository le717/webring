from typing import Literal, TypedDict

import requests

from src.core.database import weblink
from src.core.database.schema import RottedLinks, WebLink, db
from src.core.models.RotStates import RotStates


__all__ = ["check_all", "check_one"]


class RotResult(TypedDict):
    id: str
    url: str
    result: str


def __ping_url(url: str) -> bool:
    """Check a link for rotting."""
    try:
        r = requests.head(url)
        return r.status_code == requests.codes.ok
    except Exception:
        return False


def __create(data: WebLink) -> Literal[True]:
    rot_entry = RottedLinks(id=data.id, times_failed=1)
    db.session.add(rot_entry)
    db.session.commit()
    db.session.refresh(rot_entry)
    return True


def __get(uuid: str) -> RottedLinks:
    return RottedLinks.query.filter_by(id=uuid).first()


def __update(data: RottedLinks) -> Literal[True]:
    db.session.query(RottedLinks).filter_by(id=data.id).update(
        {"times_failed": data.times_failed + 1}, synchronize_session="fetch"
    )
    db.session.commit()
    return True


def __delete(uuid: str):
    if exists := __get(uuid):
        db.session.delete(exists)
        db.session.commit()
    return True


def check_all() -> list[RotResult]:
    """Check all links for rotting."""
    results = []
    for link in weblink.get_all():
        results.append(RotResult(id=link.id, url=link.url, result=__ping_url(link.url)))
    return results


def check_one(uuid: str) -> RotResult:
    """Check a single link for rotting."""
    # The site could be pinged, so we all good
    link = weblink.get(uuid)
    if __ping_url(link.url):
        result = RotResult(id=link.id, url=link.url, result=RotStates.NO)
        __delete(uuid)

    # We could not ping the site, decide the next step
    else:
        result = RotResult(id=link.id, url=link.url, result=__record_failure(link))
    return result


def __record_failure(data: WebLink) -> RotStates:
    TIMES_FAILED_THRESHOLD = 5

    existing = __get(data.id)

    # We don't have an existing failure record, so make one
    if existing is None:
        __create(data)
        weblink.update({"id": data.id, "rotted": RotStates.MAYBE.value})
        return RotStates.MAYBE

    # We have an existing failure record, update the failure count
    print(existing.times_failed)
    if existing.times_failed < TIMES_FAILED_THRESHOLD:
        __update(existing)
        return RotStates.MAYBE

    # The failure has occurred too often, declare a dead link
    weblink.update({"id": data.id, "rotted": RotStates.YES.value})
    __delete(data.id)
    return RotStates.YES
