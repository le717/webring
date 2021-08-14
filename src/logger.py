from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union

from flask import request
import requests
import sys_vars


__all__ = ["DISCORD", "DiscordHandler", "file_handler"]


DISCORD = logging.getLogger("discord")
DISCORD.setLevel(logging.DEBUG)


class DiscordHandler(logging.Handler):
    """Create a Discord webhook event handler."""

    def __init__(self) -> None:
        super().__init__()
        self.url = sys_vars.get("DISCORD_WEBHOOK_URL")

    def format(self, record: logging.LogRecord) -> dict:
        msg_date = datetime.fromtimestamp(record.created).strftime(
            "%B %d, %Y @ %I:%M:%S %p"
        )
        msg = f""":warning: Webring Alert :warning:
Alert level: **{record.levelname.capitalize()}**
URL: {request.base_url}
Datetime: {msg_date}
Message: {record.msg}"""
        return {"content": msg}

    def emit(self, record: logging.LogRecord) -> logging.LogRecord:
        requests.post(
            self.url,
            headers={"Content-type": "application/json"},
            json=self.format(record),
        )
        return record


def file_handler(log_name: str) -> RotatingFileHandler:
    """Create a file-based error handler."""
    handler = RotatingFileHandler(
        Path("log") / log_name,
        maxBytes=500_000,
        backupCount=5,
        delay=True,
    )
    handler.setLevel(logging.ERROR)
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )
    return handler
