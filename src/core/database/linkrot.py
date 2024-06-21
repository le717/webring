from copy import copy
from typing import TypedDict

import httpx
import sys_vars

from src.core.database import weblink
from src.core.database.schema import LinkrotHistory, WebLink, db
from src.core.logger import logger


__all__ = ["check_all", "check_one", "get_history"]


class Check(TypedDict):
    times_failed: int
    is_dead: bool
    is_web_archive: bool


class RotResult(TypedDict):
    id: str
    url: str
    result: Check


def __can_reach_site(url: str) -> bool:
    """Check a link for rotting."""
    try:
        return httpx.head(url).status_code in {
            httpx.codes.OK,
            httpx.codes.CREATED,
            httpx.codes.NO_CONTENT,
            httpx.codes.NOT_MODIFIED,
        }
    except httpx.HTTPError:
        logger.info({
            "id": "N/A",
            "url": url,
            "message": "Link could not be reached during a linkrot check.",
        })
        return False


def __check_wayback_archive(url: str) -> str:
    """Check the Web Archive for an archived URL."""
    r = httpx.get(f"https://archive.org/wayback/available?url={url}").json()
    if not r["archived_snapshots"]:
        return ""

    # Transform the provided URL to use HTTPS for the scheme
    return str(httpx.URL(r["archived_snapshots"]["closest"]["url"]).copy_with(scheme="https"))


def __record_failure(entry: WebLink, history_entry: LinkrotHistory) -> Check:
    TIMES_FAILED_THRESHOLD = sys_vars.get_int("TIMES_FAILED_THRESHOLD")
    result = Check(times_failed=0, is_dead=False, is_web_archive=False)

    # Determine how many times we've failed the rot check since the last successful check
    try:
        id_of_last_success = max(e.id for e in entry.history if e.was_alive)
    except ValueError:
        id_of_last_success = 0
    times_failed = len([
        e.id for e in entry.history if not e.was_alive and e.id > id_of_last_success
    ])
    result["times_failed"] = times_failed

    # We've failed the rot check less than the allowed threshold, only issue a warning
    if times_failed <= TIMES_FAILED_THRESHOLD:
        plural = "times" if times_failed > 1 else "time"
        message = f"Entry has failed the linkrot check {times_failed} {plural}."
        logger.error({
            "id": entry.uuid,
            "url": entry.url,
            "message": message,
        })
        history_entry.update_with({"message": message})
        db.session.commit()
        return result

    # We've failed the threshold too many times, check the Web Archive for an archived URL
    if wb_url := __check_wayback_archive(entry.url):
        # We have an WA URL, update the entry with it.
        # Make sure we copy the old URL so we can reference it in the logger message
        old_url = copy(entry.url)
        entry.update_with({"url": wb_url, "is_web_archive": True})
        result["is_web_archive"] = True
        message = "Entry has been updated to indicate a Web Archive reference."
        logger.info({
            "id": entry.uuid,
            "url": old_url,
            "message": message,
        })
        history_entry.update_with({"message": message})
        db.session.commit()
        return result

    # We can't find the site on the web archive. It's a dead entry
    entry.update_with({"is_dead": True})
    result["is_dead"] = True
    message = "Entry has been marked as a dead link."
    logger.critical({
        "id": entry.uuid,
        "url": entry.url,
        "message": message,
    })
    history_entry.update_with({"message": message})
    db.session.commit()
    return result


def check_all() -> list[RotResult]:
    """Check all links for rotting."""
    return [
        check_one(link) for link in weblink.get_all(include_rotted=True, include_web_archive=False)
    ]


def check_one(uuid: WebLink | str) -> RotResult | None:
    """Check a single entry for rotting."""
    # If we got an uuid string, then we need to look up the entry.
    # If it doesn't exist in the db, we can't do anything
    if isinstance(uuid, str) and (uuid := weblink.get(uuid)) is None:
        return None
    entry = uuid

    # If the entry is already marked as a Web Archive entry, don't do anything more.
    # We can't do much more because it's really hard to extract the original URL
    # from a WA URL without a human looking at it
    if entry.is_web_archive:
        logger.info({
            "id": entry.uuid,
            "url": entry.url,
            "message": (
                "Entry has previously been marked to as a Web Archive entry, not checking again."
            ),
        })
        times_failed = len([e.id for e in entry.history if not e.was_alive])
        return RotResult(
            id=entry.uuid,
            url=entry.url,
            result=Check(times_failed=times_failed, is_dead=False, is_web_archive=True),
        )

    # Create a history record. It may be updated later with rot results
    history_entry = LinkrotHistory(url_checked=entry.url, entry=entry)
    db.session.add(history_entry)
    db.session.commit()
    db.session.refresh(history_entry)

    # If the site could be pinged, then the site is alive
    if __can_reach_site(entry.url):
        # The site status hasn't changed
        if not entry.is_dead:
            message = "Entry remains online and available."
            history_entry.update_with({"message": message})
            db.session.commit()
            logger.info({
                "id": entry.uuid,
                "url": entry.url,
                "message": message,
            })
            return RotResult(
                id=entry.uuid,
                url=entry.url,
                result=Check(times_failed=0, is_dead=False, is_web_archive=False),
            )

        # The entry was previously marked as dead, change that
        message = "Entry was previously determined to be dead but has been revived."
        history_entry.update_with({"message": message})
        entry.update_with({
            "is_dead": False,
            "is_web_archive": False,
        })
        db.session.commit()
        logger.info({
            "id": entry.uuid,
            "url": entry.url,
            "message": message,
        })
        return RotResult(
            id=entry.uuid,
            url=entry.url,
            result=Check(times_failed=0, is_dead=False, is_web_archive=False),
        )

    # We could not ping the site, determine if it is dead or WA-only entry
    # and update our history record accordingly
    history_entry.update_with({"was_alive": False})
    db.session.commit()
    result = __record_failure(entry, history_entry)
    return RotResult(id=entry.uuid, url=entry.url, result=result)


def get_history(uuid: str) -> list[LinkrotHistory] | None:
    """Get the linkrot history for the given entry."""
    if (entry := weblink.get(uuid)) is None:
        return None
    return entry.history
