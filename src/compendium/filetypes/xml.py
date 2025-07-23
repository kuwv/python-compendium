# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control XML module."""

# import datetime
import errno
import logging
from os import path
from typing import Any

import aiofiles
import xmltodict

from compendium import config
from cmplendium.loader.base import ConfigFile
from compendium.exceptions import LoaderError
from compendium.filetypes import FiletypesBase


class XmlConfig(FiletypesBase):
    """Manage XML configurations."""

    extensions = ('xml',)

    def __new__(cls, *_: Any, **kwargs: Any) -> XmlConfig:
        """Return state type."""
        return super().__new__(
            AsyncXmlConfig
            if kwargs.get('async', config.DEFAULT_ASYNC_ENABLED)
            else cls
        )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize XML configuration module."""
        logging.info('Inializing XmlConfig')
        self.encoding = kwargs.get('encoding', config.DEFAULT_ENCODING)
        self.encoder = kwargs.get('encoder', str)
        self.process_namespaces = kwargs.get('process_namespaces', False)
        self.namespaces = kwargs.get('namespaces', None)


class SyncXmlConfig(XmlConfig):
    """Manage XML configurations."""

    def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from XML configuration."""
        logging.info('loading XML configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                with open(filepath, 'r', encoding=self.encoding) as file:
                    content = xmltodict.parse(
                        file.read(),
                        encoding=self.encoding,
                        process_namespaces=self.process_namespaces,
                        namespaces=self.namespaces,
                    )
                    return content
            raise LoaderError(f"filepath {filepath!r} is not a file")
        raise LoaderError(f"filepath '{filepath!r}' does not exist")

    def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to XML configuration."""
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                file.write(
                    xmltodict.unparse(
                        content, encoding=self.encoding, pretty=True
                    )
                )
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")


class AsyncXmlConfig(XmlConfig):
    """Manage XML configurations."""

    async def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from XML configuration."""
        logging.info('loading XML configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                async with aiofiles.open(
                    filepath, 'r', encoding=self.encoding
                ) as file:
                    content = await file.read(),
                    return xmltodict.parse(
                        content,
                        encoding=self.encoding,
                        process_namespaces=self.process_namespaces,
                        namespaces=self.namespaces,
                    )
            raise LoaderError(f"filepath {filepath!r} is not a file")
        raise LoaderError(f"filepath '{filepath!r}' does not exist")

    async def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to XML configuration."""
        try:
            async with aiofiles.open(
                filepath, 'w', encoding=self.encoding
            ) as file:
                xml = xmltodict.unparse(
                    content, encoding=self.encoding, pretty=True
                )
                await file.write(xml)
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise LoaderError(f"unable to save to '{filepath!r}")
