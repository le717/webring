from typing import Literal, TypedDict, Union

import requests
import sys_vars

from src.logger import LINKROT
from src.core.database import weblink
from src.core.database.schema import RottedLinks, WebLink, db
from src.core.models.RotStates import RotStates


__all__ = ["check_all", "check_one", "delete"]


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


def __ping_wayback_machine(url: str) -> Union[Literal[False], str]:
    """Check the Web Archive for an archived URL."""
    r = requests.get(f"https://archive.org/wayback/available?url={url}").json()
    if not r["archived_snapshots"]:
        return False
    return r["archived_snapshots"]["closest"]["url"]


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


def delete(uuid: str) -> bool:
    if exists := __get(uuid):
        db.session.delete(exists)
        db.session.commit()
        return True
    return False


def check_all() -> list[RotResult]:
    """Check all links for rotting."""
    return [check_one(link.id) for link in weblink.get_all()]


def check_one(uuid: str) -> RotResult:
    """Check a single link for rotting."""
    # The site could be pinged, so we all good
    link = weblink.get(uuid)
    if __ping_url(link.url):
        result = RotResult(id=link.id, url=link.url, result=RotStates.NO.value)

        # A rotten link has been revived
        if delete(uuid):
            LINKROT.info(
                f"Link {link.url} (`{link.id}`) has been revived to a rotten status of **{RotStates.NO.value}**."
            )
            weblink.update(
                {
                    "id": link.id,
                    "rotted": RotStates.NO.value,
                    "title": link.title.removesuffix(" (Dead Link)"),
                }
            )

    # We could not ping the site, decide the next step
    else:
        result = RotResult(
            id=link.id, url=link.url, result=__record_failure(link).value
        )
    return result


def __record_failure(data: WebLink) -> RotStates:
    TIMES_FAILED_THRESHOLD = sys_vars.get_int("TIMES_FAILED_THRESHOLD")

    # We don't have an existing failure record, so make one
    existing = __get(data.id)
    if existing is None:
        __create(data)
        weblink.update({"id": data.id, "rotted": RotStates.MAYBE.value})
        LINKROT.error(
            f"Link {data.url} (`{data.id}`) has been given a rotten status of **{RotStates.MAYBE.value}**."
        )
        return RotStates.MAYBE

    # We have an existing failure record, update the failure count
    if (existing.times_failed + 1) < TIMES_FAILED_THRESHOLD:
        __update(existing)
        LINKROT.error(
            f"Link {data.url} (`{data.id}`) linkrot check failure #{existing.times_failed}."
        )
        return RotStates.MAYBE

    # The failure has occurred too often,
    # check the Web Archive for an archived URL
    revised_info = {"id": data.id, "rotted": RotStates.YES.value}
    LINKROT.critical(
        f"Link {data.url} (`{data.id}`) has been given a rotten status of **{RotStates.YES.value}**."
    )
    if wb_url := __ping_wayback_machine(data.url):
        revised_info["url"] = wb_url
        LINKROT.critical(
            f"Link {data.url} (`{data.id}`) has been updated to point to the Web Archive."
        )

    # An archive url doesn't exist, tag the title as a dead link
    else:
        revised_info["title"] = f"{data.title} (Dead Link)"
        LINKROT.critical(
            f"Link {data.url} (`{data.id}`) has been updated to indicate a dead link."
        )
        delete(data.id)

    # Update the dead link
    weblink.update(revised_info)
    return RotStates.YES
