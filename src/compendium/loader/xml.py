# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control XML module."""

from __future__ import annotations

import logging
from collections.abc import MutableMapping
from os import PathLike, path
from typing import Any, IO, Union

import xmltodict
from aiofiles.threadpool.text import AsyncTextIOWrapper

from compendium import config
from compendium.exceptions import LoaderError
from compendium.loader.base import (
    AsyncConfigFileMixin, ConfigFile, SyncConfigFileMixin
)


class XmlConfig(ConfigFile):
    """Manage XML configurations."""

    extensions = ('xml',)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize XML configuration module."""
        logging.info('Inializing XmlConfig')
        self.encoder = kwargs.pop('encoder', str)
        self.process_namespaces = kwargs.pop('process_namespaces', False)
        self.namespaces = kwargs.pop('namespaces', None)
        super().__init__(*args, **kwargs)


class AsyncXmlConfig(AsyncConfigFileMixin, XmlConfig):
    """Manage XML configurations."""

    async def _load(self, file: AsyncTextIOWrapper) -> MutableMapping:
        """Load settings from XML configuration."""
        logging.info('loading XML configuration file')
        content = await file.read(),
        return xmltodict.parse(
            content,
            encoding=self.encoding,
            process_namespaces=self.process_namespaces,
            namespaces=self.namespaces,
        )

    async def _dump(
        self, content: MutableMapping, file: AsyncTextIOWrapper
    ) -> None:
        """Save settings to XML configuration."""
        xml = xmltodict.unparse(
            dict(content), encoding=self.encoding, pretty=True
        )
        await file.write(xml)


class SyncXmlConfig(SyncConfigFileMixin, XmlConfig):
    """Manage XML configurations."""

    def _load(self, file: IO) -> MutableMapping:
        """Load settings from XML configuration."""
        logging.info('loading XML configuration file')
        content = xmltodict.parse(
            file.read(),
            encoding=self.encoding,
            process_namespaces=self.process_namespaces,
            namespaces=self.namespaces,
        )
        return content

    def _dump(self, content: MutableMapping, file: IO) -> None:
        """Save settings to XML configuration."""
        file.write(
            xmltodict.unparse(content, encoding=self.encoding, pretty=True)
        )
