# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control toml module."""

from __future__ import annotations

import logging
from collections.abc import MutableMapping
from os import PathLike, path
from typing import Any, IO, Union

import tomlkit
from aiofiles.threadpool.text import AsyncTextIOWrapper

from compendium import config
from compendium.exceptions import LoaderError
from compendium.loader.base import (
    AsyncConfigFileMixin, ConfigFile, SyncConfigFileMixin
)


class TomlConfig(ConfigFile):
    """Manage toml configurations."""

    extensions = ('tml', 'toml')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize toml module."""
        logging.info('Inializing TomlConfig')
        super().__init__(*args, **kwargs)

    @staticmethod
    def _convert(config: Any) -> Any:
        """Recursively convert tomlkit to dict.

        See: https://github.com/sdispater/tomlkit/issues/43

        """
        # convert associative array
        if isinstance(config, dict):
            config = {
                str(k): TomlConfig._convert(v) for k, v in config.items()
            }
        # convert list
        elif isinstance(config, list):
            config = [TomlConfig._convert(x) for x in config]
        # convert scalars
        elif isinstance(config, tomlkit.items.Integer):
            config = int(config)
        elif isinstance(config, tomlkit.items.Float):
            config = float(config)
        elif isinstance(config, tomlkit.items.String):
            config = str(config)
        elif isinstance(config, tomlkit.items.Bool):
            config = bool(config)
        return config


class AsyncTomlConfig(AsyncConfigFileMixin, TomlConfig):
    """Manage toml configurations."""

    async def _load(self, file: AsyncTextIOWrapper) -> MutableMapping:
        """Load settings from toml configuration."""
        logging.info('loading TOML configuration file')
        return self._convert(tomlkit.parse(await file.read()))

    async def _dump(
        self, config: MutableMapping, file: AsyncTextIOWrapper
    ) -> None:
        """Save settings to toml configuration."""
        logging.info('saving TOML configuration file')
        # XXX: tomlkit is missing union of tomldocument and dict
        await file.write(tomlkit.dumps(dict(config)))


class SyncTomlConfig(SyncConfigFileMixin, TomlConfig):
    """Manage toml configurations."""

    def _load(self, file: IO) -> MutableMapping:
        """Load settings from toml configuration."""
        logging.info('loading TOML configuration file')
        return self._convert(tomlkit.parse(file.read()))

    def _dump(self, config: MutableMapping, file: IO) -> None:
        """Save settings to toml configuration."""
        logging.info('saving TOML configuration file')
        # XXX: tomlkit is missing union of tomldocument and dict
        file.write(tomlkit.dumps(dict(config)))
