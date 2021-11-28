# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control JSON module."""

# import datetime
import errno
import json  # type: ignore
# import jsonschema  # type: ignore
import logging
import os
from typing import Any, Dict, Tuple

from compendium.filetypes_base import FiletypesBase


class JsonConfig(FiletypesBase):
    """Manage JSON configurations."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize JSON configuration module."""
        logging.info('Inializing JsonConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        # self.encoder = kwargs.get('encoder', None)

    @staticmethod
    def filetypes() -> Tuple[str, ...]:
        """Return support JSON filetypes."""
        return ('json',)

    def load_config(self, filepath: str) -> Dict[str, Any]:
        """Load settings from JSON configuration."""
        logging.info('loading JSON configuration file')
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding=self.encoding) as f:
                content = json.load(f)
        else:
            content = {}
        return content

    def dump_config(self, content: Dict[str, Any], filepath: str) -> None:
        """Save settings to JSON configuration."""
        try:
            with open(filepath, 'w') as f:
                json.dump(
                    content, f, indent=2, sort_keys=False
                    # , default=self.encoder
                )
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise

    # def validate(self, content: Dict[str, Any]) -> bool:
    #     """Validate JSON configuration."""
    #     try:
    #         jsonschema.validate(instance=content, schema=self.schema)
    #     except jsonschema.exceptions.ValidationError as err:
    #         # TODO handle validation error
    #         print(err[0])
    #         return False
    #     return True
