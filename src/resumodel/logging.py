# Copyright (c) 2025 Hermann Agossou
# Licensed under the MIT License. See the LICENSE file for details.

"""Logging configuration for ResuModel."""

import logging
import sys
from typing import Optional

# Create a custom logger
logger = logging.getLogger("resumodel")


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """Configure logging for the application.

    Args:
        level: Logging level (default: logging.INFO)
        log_file: Optional path to log file
    """
    # Clear existing handlers
    logger.handlers.clear()
    logger.setLevel(level)

    # Create formatters
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
