"""Tests for logging configuration."""

import logging
import pytest

from resumodel.logging import setup_logging, logger


def test_setup_logging_default_level() -> None:
    """Test logging setup with default INFO level."""
    setup_logging()
    assert logger.level == logging.INFO


def test_setup_logging_debug_level() -> None:
    """Test logging setup with DEBUG level."""
    setup_logging(level=logging.DEBUG)
    assert logger.level == logging.DEBUG


def test_setup_logging_warning_level() -> None:
    """Test logging setup with WARNING level."""
    setup_logging(level=logging.WARNING)
    assert logger.level == logging.WARNING


def test_logger_has_handler() -> None:
    """Test that logger has a StreamHandler configured."""
    setup_logging()
    assert len(logger.handlers) > 0
    # Check that at least one handler is a StreamHandler
    has_stream_handler = any(
        isinstance(h, logging.StreamHandler) for h in logger.handlers
    )
    assert has_stream_handler


def test_logger_name() -> None:
    """Test that logger has correct name."""
    assert logger.name == "resumodel"


def test_setup_logging_idempotent() -> None:
    """Test that calling setup_logging multiple times doesn't add duplicate handlers."""
    setup_logging()
    initial_handler_count = len(logger.handlers)

    setup_logging()

    # Should not add more handlers
    assert len(logger.handlers) == initial_handler_count
