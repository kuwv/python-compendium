# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control toml module."""

from __future__ import annotations

import errno
import logging
from os import path
from typing import Any

import aiofiles
import tomlkit

from compendium import config
from compendium.exceptions import LoaderError
from compendium.filetypes import FiletypesBase


class TomlConfig(FiletypesBase):
    """Manage toml configurations."""

    extensions = ('toml', 'tml')

    def __new__(cls, *_: Any, **kwargs: Any) -> TomlConfig:
        """Return state type."""
        return super().__new__(
            AsyncTomlConfig
            if kwargs.get('async', config.DEFAULT_ASYNC_ENABLED)
            else SyncTomlConfig
        )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize toml module."""
        logging.info('Inializing TomlConfig')
        self.encoding = kwargs.get('encoding', config.DEFAULT_ENCODING)

    @staticmethod
    def _convert(content: Any) -> Any:
        """Recursively convert tomlkit to dict.

        See: https://github.com/sdispater/tomlkit/issues/43

        """
        # convert associative array
        if isinstance(content, dict):
            content = {
                str(k): TomlConfig._convert(v) for k, v in content.items()
            }
        # convert list
        elif isinstance(content, list):
            content = [TomlConfig._convert(x) for x in content]
        # convert scalars
        elif isinstance(content, tomlkit.items.Integer):
            content = int(content)
        elif isinstance(content, tomlkit.items.Float):
            content = float(content)
        elif isinstance(content, tomlkit.items.String):
            content = str(content)
        elif isinstance(content, tomlkit.items.Bool):
            content = bool(content)
        return content


class SyncTomlConfig(TomlConfig):
    """Manage toml configurations."""

    def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from toml configuration."""
        logging.info('loading TOML configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                with open(filepath, 'r', encoding=self.encoding) as file:
                    return self._convert(tomlkit.parse(file.read()))
            raise LoaderError(f"filepath '{filepath!r}' is not a file")
        raise LoaderError(f"filepath '{filepath!r}' does not exist")

    def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to toml configuration."""
        logging.info('saving TOML configuration file')
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                # XXX: tomlkit is missing union of tomldocument and dict
                file.write(tomlkit.dumps(content))
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")


class AsyncTomlConfig(TomlConfig):
    """Manage toml configurations."""

    async def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from toml configuration."""
        logging.info('loading TOML configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                async with aiofiles.open(filepath, 'w') as file:
                    return self._convert(tomlkit.parse(await file.read()))
            raise LoaderError(f"filepath '{filepath!r}' is not a file")
        raise LoaderError(f"filepath '{filepath!r}' does not exist")

    async def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to toml configuration."""
        logging.info('saving TOML configuration file')
        try:
            async with aiofiles.open(
                filepath, 'w', encoding=self.encoding
            ) as file:
                # XXX: tomlkit is missing union of tomldocument and dict
                await file.write(tomlkit.dumps(content))
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")
