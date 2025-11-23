# Copyright (c) 2025 Hermann Agossou
# Licensed under the MIT License. See the LICENSE file for details.

"""Custom exceptions for ResuModel."""


class ResuModelError(Exception):
    """Base exception for all ResuModel errors."""

    pass


class ConfigError(ResuModelError):
    """Raised when there is an error loading configuration or data files."""

    pass


class DataError(ResuModelError):
    """Raised when there is an error in the data structure or validation."""

    pass


class TemplateError(ResuModelError):
    """Raised when there is an error loading or rendering templates."""

    pass
