from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union

import requests
import sys_vars


__all__ = ["DISCORD", "DiscordHandler", "file_handler"]

DISCORD = logging.getLogger("discord")


class DiscordHandler(logging.Handler):
    """Create a Discord webhook event handler."""

    def __init__(self) -> None:
        super().__init__()
        self.url = sys_vars.get("DISCORD_WEBHOOK_URL")

    def format(self, record: logging.LogRecord) -> dict:
        msg = f"""Date/Time: {datetime.fromtimestamp(record.created).isoformat()}
Message: {record.msg}"""
        return {"username": "Arcana Webring", "content": msg}

    def emit(self, record: logging.LogRecord):
        return requests.post(
            self.url,
            headers={"Content-type": "application/json"},
            json=self.format(record),
        ).content


def discord_handler() -> Union[DiscordHandler, logging.NullHandler]:
    """Create a Discord handler if enabled."""
    if sys_vars.get_bool("ENABLE_DISCORD_LOGGING", default=False):
        return DiscordHandler()
    else:
        return logging.NullHandler()


def file_handler() -> RotatingFileHandler:
    """Create a file-based error handler."""
    handler = RotatingFileHandler(
        Path("log") / "error.log",
        maxBytes=500_000,
        backupCount=5,
        delay=True,
    )
    handler.setLevel(logging.ERROR)
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )
    return handler
