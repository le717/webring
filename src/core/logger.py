import logging
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import httpx
import sys_vars
from flask import request


__all__ = ["logger", "DiscordHandler", "file_handler"]


logger = logging.getLogger("linkrot-status")
logger.setLevel(logging.DEBUG)


def _linkrot_formatter(record: logging.LogRecord) -> str:
    msg_date = datetime.fromtimestamp(record.created, tz=UTC).strftime("%B %d, %Y @ %I:%M:%S %p")
    return f""":warning: Webring Alert :warning:
Alert level: **{record.levelname.capitalize()}**
Date: {msg_date}
Webring URL: {request.root_url}

Link ID: `{record.msg["id"]}`
Link URL: {record.msg["url"]}
Message: {record.msg["message"]}"""


class DiscordHandler(logging.Handler):
    """Create a Discord webhook event handler."""

    def __init__(self) -> None:
        super().__init__()
        self.url = sys_vars.get("DISCORD_WEBHOOK_URL")

    def format(self, record: logging.LogRecord) -> dict:
        return {"content": _linkrot_formatter(record)}

    def emit(self, record: logging.LogRecord) -> logging.LogRecord:
        httpx.post(
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
        handler.format = _linkrot_formatter
    else:
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
    return handler
