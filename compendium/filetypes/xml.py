# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control XML module."""
# import datetime
import errno
import logging
import os
from typing import Any, Dict, Tuple

import xmltodict  # type: ignore

from compendium.filetypes_base import FiletypesBase


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
    def filetypes() -> Tuple[str, ...]:
        """Return supported XML configuration filetypes."""
        return ('xml',)

    def load_config(self, filepath: str) -> Dict[str, Any]:
        """Load settings from XML configuration."""
        logging.info('loading XML configuration file')
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                content = xmltodict.parse(
                    f.read(),
                    encoding=self.encoding,
                    process_namespaces=self.process_namespaces,
                    namespaces=self.namespaces
                )
        else:
            content = {}
        return content

    def dump_config(self, content: Dict[str, Any], filepath: str) -> None:
        """Save settings to XML configuration."""
        try:
            with open(filepath, 'w') as f:
                f.write(
                    xmltodict.unparse(
                        content,
                        encoding=self.encoding,
                        pretty=True
                    )
                )
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise
