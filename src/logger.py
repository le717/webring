import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


__all__ = ["file_handler"]


def file_handler(log_path: Path) -> RotatingFileHandler:
    """Create a file-based error handler."""
    handler = RotatingFileHandler(
        log_path / "error.log",
        maxBytes=500_000,
        backupCount=5,
        delay=True,
    )
    handler.setLevel(logging.ERROR)
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )
    return handler
