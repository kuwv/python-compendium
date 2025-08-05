# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control toml configuration module."""

from __future__ import annotations

import logging
from collections.abc import MutableMapping
from configparser import ConfigParser  # ExtendedInterpolation
from io import StringIO
from os import PathLike, path
from typing import Any, IO, Union

from aiofiles.threadpool.text import AsyncTextIOWrapper

from compendium import config
from compendium.loader.base import (
    AsyncConfigFileMixin, ConfigFile, SyncConfigFileMixin
)
from compendium.exceptions import LoaderError


class IniConfig(ConfigFile):
    """Manage ini configurations."""

    extensions = ('cfg', 'cnf', 'conf', 'config', 'ini')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize toml module."""
        logging.info('Inializing IniConfig')
        self.parser = ConfigParser()
        # self.parser = ConfigParser(*args, **kwargs)
        # self.parser._interpolation = ExtendedInterpolation()
        super().__init__(*args, **kwargs)


class AsyncIniConfig(AsyncConfigFileMixin, IniConfig):
    """Manage ini configurations."""

    async def _load(self, file: AsyncTextIOWrapper) -> MutableMapping:
        """Load settings from toml configuration."""
        logging.info('loading INI configuration file')
        content = StringIO(await file.read())
        self.parser.read_file(content)
        config: MutableMapping = dict(self.parser.defaults())
        for section in self.parser.sections():
            config[section] = dict(self.parser.items(section, raw=True))
        return config

    async def _dump(
        self, config: MutableMapping, file: AsyncTextIOWrapper
    ) -> None:
        """Save settings to toml configuration."""
        logging.info('saving INI configuration file')
        update: MutableMapping = {'DEFAULT': {}}
        for k, v in dict(config).items():
            if isinstance(v, dict):
                update[k] = v
            else:
                update['DEFAULT'][k] = v
        stream = StringIO()
        self.parser.read_dict(update)
        self.parser.write(file)


class SyncIniConfig(SyncConfigFileMixin, IniConfig):
    """Manage ini configurations."""

    def _load(self, file: IO) -> MutableMapping:
        """Load settings from toml configuration."""
        logging.info('loading INI configuration file')
        self.parser.read_file(StringIO(file.read()))
        # XXX: need a handler to process default as chainmap
        # config = {'DEFAULT': dict(self.parser.defaults())}
        config: MutableMapping = dict(self.parser.defaults())
        for section in self.parser.sections():
            config[section] = dict(self.parser.items(section, raw=True))
        return config

    def _dump(self, config: MutableMapping, file: IO) -> None:
        """Save settings to toml configuration."""
        logging.info('saving INI configuration file')
        update: MutableMapping = {'DEFAULT': {}}
        for k, v in dict(config).items():
            if isinstance(v, dict):
                update[k] = v
            else:
                update['DEFAULT'][k] = v
        self.parser.read_dict(update)
        self.parser.write(file)
