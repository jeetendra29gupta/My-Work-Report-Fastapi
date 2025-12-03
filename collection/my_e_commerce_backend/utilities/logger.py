import logging
import os
from logging.handlers import RotatingFileHandler

from ..utilities.config import (
    LOG_DIR,
    LOG_FILE,
    MAX_BYTES,
    BACKUP_COUNT,
)

os.makedirs(LOG_DIR, exist_ok=True)
file_path = f"{LOG_DIR}/{LOG_FILE}"


def get_logger(name: str) -> logging.Logger:
    """
    Simple logging utility usable like:
    logger = get_logger(__name__)
    Includes console logging + rotating file logging.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File Handler (rotating logs)
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=MAX_BYTES,  # 5MB
            backupCount=BACKUP_COUNT,
        )
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
