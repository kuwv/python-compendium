# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control XML module."""

# import datetime
import errno
import logging
from os import path
from typing import Any

import xmltodict

from compendium.exceptions import LoaderError
from compendium.filetypes import FiletypesBase


class XmlConfig(FiletypesBase):
    """Manage XML configurations."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize XML configuration module."""
        logging.info('Inializing XmlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.encoder = kwargs.get('encoder', str)
        self.process_namespaces = kwargs.get('process_namespaces', False)
        self.namespaces = kwargs.get('namespaces', None)

    @staticmethod
    def extensions() -> tuple[str, ...]:
        """Return supported XML configuration file extensions."""
        return ('xml',)

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
            else:
                raise LoaderError(f"filepath {filepath!r} is not a file")
        else:
            raise LoaderError(f"filepath '{filepath!r}' does not exist")
        return content

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
                raise
