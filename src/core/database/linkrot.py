from typing import Literal, TypedDict

import httpx
import sys_vars

from src.core.database import weblink
from src.core.database.schema import RottedLinks, WebLink, db
from src.core.logger import logger


__all__ = ["check_all", "check_one", "delete"]


class Check(TypedDict):
    times_failed: int
    is_dead: bool
    is_web_archive: bool


class RotResult(TypedDict):
    id: str
    url: str
    result: Check


def __ping_url(url: str) -> bool:
    """Check a link for rotting."""
    try:
        r = httpx.head(url)
        return r.status_code in (
            httpx.codes.OK,
            httpx.codes.CREATED,
            httpx.codes.NO_CONTENT,
            httpx.codes.NOT_MODIFIED,
        )
    except httpx.HTTPError:
        logger.info({
            "id": "N/A",
            "url": url,
            "message": "Link could not be reached during a linkrot check.",
        })
        return False


def __ping_wayback_machine(url: str) -> Literal[False] | str:
    """Check the Web Archive for an archived URL."""
    r = httpx.get(f"https://archive.org/wayback/available?url={url}").json()
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
    return db.session.execute(db.select(RottedLinks).filter_by(id=uuid)).scalar_one_or_none()


def __update(rl: RottedLinks) -> Literal[True]:
    """Update the rotted log link with this instance."""
    data = rl.as_dict()
    del data["id"]
    data["times_failed"] += 1
    rl.update_with(data)
    db.session.commit()
    return True


def delete(uuid: str) -> bool:
    """Delete an item from the linkrot log."""
    if exists := __get(uuid):
        db.session.delete(exists)
        db.session.commit()
        return True
    return False


def check_all() -> list[RotResult]:
    """Check all links for rotting."""
    return [check_one(link.id) for link in weblink.get_all(include_rotted=False)]


def check_one(uuid: str) -> RotResult | None:
    """Check a single link for rotting."""
    # The uuid doesn't exist in the db, we can't do anything
    if (link := weblink.get(uuid)) is None:
        return None

    # The site could be pinged, so we all good
    if __ping_url(link.url):
        result = RotResult(
            id=link.id,
            url=link.url,
            result=Check(times_failed=0, is_dead=False, is_web_archive=False),
        )

        # A rotten link has been revived
        if delete(uuid):
            logger.info({
                "id": link.id,
                "url": link.url,
                "message": "Link has been marked to not be dead or a Web Archive reference.",
            })
            weblink.update({
                "id": link.id,
                "is_dead": 0,
                "is_web_archive": 0,
            })

    # We could not ping the site, decide the next step
    else:
        result = RotResult(id=link.id, url=link.url, result=__record_failure(link))
    return result


def __record_failure(data: WebLink) -> Check:
    TIMES_FAILED_THRESHOLD = sys_vars.get_int("TIMES_FAILED_THRESHOLD")
    result = Check(times_failed=0, is_dead=False, is_web_archive=False)

    # We don't have an existing failure record, so make one
    existing = __get(data.id)
    if existing is None:
        __create(data)
        logger.error({
            "id": data.id,
            "url": data.url,
            "message": "Linkrot check failure #1.",
        })
        result["times_failed"] = 1
        return result

    # We have an existing failure record, update the failure count
    if (existing.times_failed + 1) < TIMES_FAILED_THRESHOLD:
        __update(existing)
        logger.error({
            "id": data.id,
            "url": data.url,
            "message": f"Linkrot check failure #{existing.times_failed}.",
        })
        result["times_failed"] = existing.times_failed
        return result

    # The failure has occurred too often,
    # check the Web Archive for an archived URL
    revised_info = {"id": data.id}
    if wb_url := __ping_wayback_machine(data.url):
        revised_info["url"] = wb_url
        revised_info["is_web_archive"] = 1
        result["is_web_archive"] = True
        logger.critical({
            "id": data.id,
            "url": data.url,
            "message": "Link has been updated to indicate a Web Archive reference.",
        })

    # An archive url doesn't exist, mark as a dead link
    else:
        revised_info["is_dead"] = 1
        result["is_dead"] = True
        logger.critical({
            "id": data.id,
            "url": data.url,
            "message": "Link has been marked as a dead link.",
        })

    # Update the dead link
    weblink.update(revised_info)
    return result
