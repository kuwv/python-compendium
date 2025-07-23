# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control JSON module."""

from __future__ import annotations

import errno
import json
import logging
from os import path
from typing import Any

import aiofiles

from compendium import config
from compendium.exceptions import LoaderError
from compendium.filetypes import FiletypesBase


class JsonConfig(FiletypesBase):
    """Manage JSON configurations."""

    extensions = ('json',)

    def __new__(cls, *_: Any, **kwargs: Any) -> JsonConfig:
        """Return state type."""
        return super().__new__(
            AsyncJsonConfig
            if kwargs.get('async', config.DEFAULT_ASYNC_ENABLED)
            else SyncJsonConfig
        )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize JSON configuration module."""
        logging.info('Inializing JsonConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        # self.encoder = kwargs.get('encoder', None)


class SyncJsonConfig(JsonConfig):
    """Manage JSON configurations."""

    def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from JSON configuration."""
        logging.info('loading JSON configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                with open(filepath, 'r', encoding=self.encoding) as file:
                    return json.loads(file.read())
            raise LoaderError(f"filepath '{filepath!r}' is not a file")
        raise LoaderError(f"filepath '{filepath!r}' does not exist")

    def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to JSON configuration."""
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                file.write(
                    json.dumps(
                        content,
                        indent=2,
                        sort_keys=False
                        # default=self.encoder
                    )
                )
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")


class AsyncJsonConfig(JsonConfig):
    """Manage JSON configurations."""

    async def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from JSON configuration."""
        logging.info('loading JSON configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                async with aiofiles.open(
                    filepath, 'r', encoding=self.encoding
                ) as file:
                    return json.loads(await file.read())
            raise LoaderError(f"filepath '{filepath!r}' is not a file")
        raise LoaderError(f"filepath '{filepath!r}' does not exist")

    async def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to JSON configuration."""
        try:
            async with aiofiles.open(filepath, 'w', encoding=self.encoding) as file:
                await file.write(
                    json.dumps(
                        content,
                        indent=2,
                        sort_keys=False,
                        # default=self.encoder
                    )
                )
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")
