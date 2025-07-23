# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control toml configuration module."""

from __future__ import annotations

import errno
import logging
from configparser import ConfigParser  # ExtendedInterpolation
from io import StringIO
from os import path
from typing import Any

import aiofiles

from compendium import config
from compendium.exceptions import LoaderError
from compendium.filetypes import FiletypesBase


class IniConfig(FiletypesBase):
    """Manage ini configurations."""

    extensions = ('cfg', 'cnf', 'conf', 'config', 'ini')

    def __new__(cls, *_: Any, **kwargs: Any) -> IniConfig:
        """Return state type."""
        return super().__new__(
            AsyncIniConfig
            if kwargs.get('async', config.DEFAULT_ASYNC_ENABLED)
            else SyncIniConfig
        )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize toml module."""
        logging.info('Inializing TomlConfig')
        self.encoding = kwargs.pop('encoding', 'utf-8')
        self.parser = ConfigParser(*args, **kwargs)
        # self.parser._interpolation = ExtendedInterpolation()


class SyncIniConfig(IniConfig):
    """Manage ini configurations."""

    def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from toml configuration."""
        logging.info('loading INI configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                with open(filepath, encoding=self.encoding) as file:
                    self.parser.read_file(StringIO(file.read()))
                    data = self.parser._sections  # type: ignore
                    for k, v in self.parser._defaults.items():  # type: ignore
                        data[k] = v
                    return data
            raise LoaderError(f"filepath {filepath!r} is not a file")
        raise LoaderError(f"filepath {filepath!r} does not exist")

    def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to toml configuration."""
        logging.info('saving INI configuration file')
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                self.parser.write(file)
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")


class AsyncIniConfig(IniConfig):
    """Manage ini configurations."""

    async def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from toml configuration."""
        logging.info('loading INI configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                async with aiofiles.open(filepath, encoding=self.encoding) as file:
                    self.parser.read_file(StringIO(await file.read()))
                    data: dict[str, Any] = self.parser._sections  # type: ignore
                    for k, v in self.parser._defaults.items():  # type: ignore
                        data[k] = v
                    return data
            raise LoaderError(f"filepath {filepath!r} is not a file")
        raise LoaderError(f"filepath {filepath!r} does not exist")

    async def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to toml configuration."""
        logging.info('saving INI configuration file')
        try:
            async with aiofiles.open(filepath, 'w', encoding=self.encoding) as file:
                stream = StringIO()
                self.parser.write(stream)
                await file.write(stream.getvalue())
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")
