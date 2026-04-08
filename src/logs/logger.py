import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Any

"""
Logger configuration for Metadata Cleaner.

This module sets up logging for the application. Log messages are written both
to the console and to a rotating file under src/logs/.
"""

LOG_FILE: str = "metadata_cleaner.log"

LOG_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH: str = os.path.join(LOG_DIR, LOG_FILE)

_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

_file_handler = RotatingFileHandler(
    LOG_PATH,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8",
)
_file_handler.setLevel(logging.INFO)
_file_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.INFO)
_console_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

logging.basicConfig(level=logging.INFO, handlers=[_file_handler, _console_handler])

logger: logging.Logger = logging.getLogger("metadata_cleaner")
logger.setLevel(logging.INFO)

def set_log_level(level_str: str) -> None:
    """
    Set the logging level for the Metadata Cleaner logger.

    Parameters:
        level_str (str): The desired logging level as a string (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR').
    """
    level = getattr(logging, level_str.upper(), logging.INFO)
    root = logging.getLogger()
    root.setLevel(level)
    for handler in root.handlers:
        handler.setLevel(level)
    logger.setLevel(level)
