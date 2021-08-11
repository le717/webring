from enum import Enum
from typing import TypedDict

import requests

from src.core.database import weblink as db


__all__ = ["check_all", "check_one"]


class RotResult(TypedDict):
    uuid: str
    url: str
    result: str


class RotStates(Enum):
    YES = "yes"
    NO = "no"
    MAYBE = "maybe"


def check(url: str) -> RotStates:

    try:
        r = requests.head(url)
        if r.status_code == requests.codes.ok:
            return RotStates.NO.value
    except Exception:
        return RotStates.YES.value


def check_all() -> list[RotResult]:

    results = []
    for link in db.get_all():
        results.append(RotResult(uuid=link.id, url=link.url, result=check(link.url)))
    return results


def check_one(uuid: str) -> RotResult:

    link = db.get(uuid)
    return RotResult(uuid=link.id, url=link.url, result=check(link.url))
