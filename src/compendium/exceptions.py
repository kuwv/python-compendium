# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide exceptions for Compendium."""


class CompendiumException(Exception):
    """Provide base errors in Compendium."""


class DriverError(CompendiumException):
    """Provide exceptions for driver errors."""


class ConfigFileError(CompendiumException):
    """Provide exceptions for ConfigFile errors."""


class ConfigManagerError(CompendiumException):
    """Provide exceptions for Config Manager errors."""


class SettingsError(CompendiumException):
    """Provide exceptions for Settings errors."""
