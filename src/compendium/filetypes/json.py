# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control JSON module."""

import errno
import json
import logging
from os import path
from typing import Any

from compendium.filetypes import FiletypesBase
from compendium.exceptions import LoaderError


class JsonConfig(FiletypesBase):
    """Manage JSON configurations."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize JSON configuration module."""
        logging.info('Inializing JsonConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        # self.encoder = kwargs.get('encoder', None)

    @staticmethod
    def extensions() -> tuple[str, ...]:
        """Return support JSON file extensions."""
        return ('json',)

    def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from JSON configuration."""
        logging.info('loading JSON configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                with open(filepath, 'r', encoding=self.encoding) as file:
                    content = json.load(file)
            else:
                raise LoaderError(f"filepath '{filepath!r}' is not a file")
        else:
            raise LoaderError(f"filepath '{filepath!r}' does not exist")
        return content

    def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to JSON configuration."""
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                json.dump(
                    content,
                    file,
                    indent=2,
                    sort_keys=False
                    # , default=self.encoder
                )
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise

    # def validate(self, content: dict[str, Any]) -> bool:
    #     """Validate JSON configuration."""
    #     try:
    #         jsonschema.validate(instance=content, schema=self.schema)
    #     except jsonschema.exceptions.ValidationError as err:
    #         # TODO handle validation error
    #         print(err[0])
    #         return False
    #     return True
