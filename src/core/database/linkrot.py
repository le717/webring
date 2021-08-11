from typing import TypedDict

import requests

from src.core.database import weblink as db
from src.core.models.RotStates import RotStates


__all__ = ["check_all", "check_one"]


class RotResult(TypedDict):
    uuid: str
    url: str
    result: str


def __check(url: str) -> RotStates:
    """Check a link for rotting."""
    try:
        r = requests.head(url)
        if r.status_code == requests.codes.ok:
            return RotStates.NO.value
    except Exception:
        return RotStates.YES.value


def check_all() -> list[RotResult]:
    """Check all links for rotting."""
    results = []
    for link in db.get_all():
        results.append(RotResult(uuid=link.id, url=link.url, result=__check(link.url)))
    return results


def check_one(uuid: str) -> RotResult:
    """Check a single link for rotting."""
    link = db.get(uuid)
    return RotResult(uuid=link.id, url=link.url, result=__check(link.url))
