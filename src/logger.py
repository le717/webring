from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union

from flask import request
import requests
import sys_vars


__all__ = ["LINKROT", "DiscordHandler", "file_handler"]


LINKROT = logging.getLogger("linkrot-status")
LINKROT.setLevel(logging.DEBUG)


def __linkfot_formatter(record: logging.LogRecord) -> str:
    msg_date = datetime.fromtimestamp(record.created).strftime(
        "%B %d, %Y @ %I:%M:%S %p"
    )
    msg = f""":warning: Webring Alert :warning:
Alert level: **{record.levelname.capitalize()}**
URL: {request.base_url}
Datetime: {msg_date}
Message: {record.msg}"""
    return msg


class DiscordHandler(logging.Handler):
    """Create a Discord webhook event handler."""

    def __init__(self) -> None:
        super().__init__()
        self.url = sys_vars.get("DISCORD_WEBHOOK_URL")

    def format(self, record: logging.LogRecord) -> dict:
        return {"content": __linkfot_formatter(record)}

    def emit(self, record: logging.LogRecord) -> logging.LogRecord:
        requests.post(
            self.url,
            headers={"Content-type": "application/json"},
            json=self.format(record),
        )
        return record


def file_handler(log_name: str, *, linkrot: bool = False) -> RotatingFileHandler:
    """Create a file-based error handler."""
    handler = RotatingFileHandler(
        Path("log") / log_name,
        maxBytes=500_000,
        backupCount=5,
        delay=True,
    )

    # Apply the appropriate formatter
    if linkrot:
        handler.setLevel(logging.DEBUG)
        handler.format = __linkfot_formatter
    else:
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
    return handler
