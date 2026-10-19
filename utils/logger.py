"""
Centralized Logging Utility for AI-QA-Suite.

Provides formatted console and rotating file logs with timestamp, level, and caller details.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from utils.config import config


def get_logger(name: str = "AI-QA-Suite") -> logging.Logger:
    """
    Get or create a configured logger instance.

    :param name: Module name or identifier
    :return: logging.Logger instance
    """
    logger = logging.getLogger(name)

    # If already configured, return existing
    if logger.handlers:
        return logger

    # Resolve log level from config
    level = getattr(logging, config.log_level, logging.INFO)
    logger.setLevel(level)

    # Format: Timestamp | Level | Name | File:Line | Message
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] (%(filename)s:%(lineno)d): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # File Handler
    log_file = config.logs_dir / "automation.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    # Avoid propagation duplication
    logger.propagate = False

    return logger


# Default framework logger
logger = get_logger("Framework")
