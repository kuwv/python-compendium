# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide exceptions for Compendium."""


class CompendiumException(Exception):
    """Provide base errors in Compendium."""


class CompendiumDriverError(CompendiumException):
    """Provide exceptions for driver errors."""


class CompendiumConfigFileError(CompendiumException):
    """Provide exceptions for ConfigFile errors."""


class CompendiumConfigManagerError(CompendiumException):
    """Provide exceptions for Config Manager errors."""


class CompendiumSettingsError(CompendiumException):
    """Provide exceptions for Settings errors."""
