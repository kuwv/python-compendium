# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control JSON module."""

from __future__ import annotations

import json
import logging
from collections.abc import MutableMapping
from os import PathLike, path
from typing import Any, IO, Union

from aiofiles.threadpool.text import AsyncTextIOWrapper

from compendium import config
from compendium.exceptions import LoaderError
from compendium.loader.base import (
    AsyncConfigFileMixin, ConfigFile, SyncConfigFileMixin
)


class JsonConfig(ConfigFile):
    """Manage JSON configurations."""

    extensions = ('json',)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize JSON configuration module."""
        logging.info('Inializing JsonConfig')
        # self.encoder = kwargs.get('encoder', None)
        super().__init__(*args, **kwargs)


class AsyncJsonConfig(AsyncConfigFileMixin, JsonConfig):
    """Manage JSON configurations."""

    async def _load(self, file: AsyncTextIOWrapper) -> MutableMapping:
        """Load settings from JSON configuration."""
        logging.info('loading JSON configuration file')
        return json.loads(await file.read())

    async def _dump(
        self, config: MutableMapping, file: AsyncTextIOWrapper
    ) -> None:
        """Save settings to JSON configuration."""
        await file.write(
            json.dumps(
                dict(config),
                indent=2,
                sort_keys=False,
                # default=self.encoder
            )
        )


class SyncJsonConfig(SyncConfigFileMixin, JsonConfig):
    """Manage JSON configurations."""

    def _load(self, file: IO) -> MutableMapping:
        """Load settings from JSON configuration."""
        logging.info('loading JSON configuration file')
        return json.loads(file.read())

    def _dump(self, config: MutableMapping, file: IO) -> None:
        """Save settings to JSON configuration."""
        file.write(
            json.dumps(
                dict(config),
                indent=2,
                sort_keys=False
                # default=self.encoder
            )
        )
