# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control toml module."""

import errno
import logging
from os import path
from typing import Any

import tomlkit

from compendium.exceptions import LoaderError
from compendium.filetypes import FiletypesBase


class TomlConfig(FiletypesBase):
    """Manage toml configurations."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize toml module."""
        logging.info('Inializing TomlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')

    @staticmethod
    def extensions() -> tuple[str, ...]:
        """Return supported file extensions."""
        return ('toml', 'tml')

    @staticmethod
    def _convert(content: Any) -> Any:
        """Recursively convert tomlkit to dict.

        See: https://github.com/sdispater/tomlkit/issues/43

        """
        # convert associative array
        if isinstance(content, dict):
            content = {
                str(k): TomlConfig._convert(v) for k, v in content.items()
            }

        # convert list
        elif isinstance(content, list):
            content = [TomlConfig._convert(x) for x in content]

        # convert scalars
        elif isinstance(content, tomlkit.items.Integer):
            content = int(content)
        elif isinstance(content, tomlkit.items.Float):
            content = float(content)
        elif isinstance(content, tomlkit.items.String):
            content = str(content)
        elif isinstance(content, tomlkit.items.Bool):
            content = bool(content)

        return content

    def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from toml configuration."""
        logging.info('loading TOML configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                with open(filepath, 'r', encoding=self.encoding) as file:
                    content = self._convert(tomlkit.parse(file.read()))
            else:
                raise LoaderError(f"filepath '{filepath!r}' is not a file")
        else:
            raise LoaderError(f"filepath '{filepath!r}' does not exist")
        return content

    def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to toml configuration."""
        logging.info('TomlConfig: saving configuration file')
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                # XXX: tomlkit is missing union of tomldocument and dict
                file.write(tomlkit.dumps(content))
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise
