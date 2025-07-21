# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control toml configuration module."""

import errno
import logging
from configparser import ConfigParser  # ExtendedInterpolation
from os import path
from typing import Any

from compendium.exceptions import LoaderError
from compendium.filetypes import FiletypesBase


class IniConfig(FiletypesBase):
    """Manage toml configurations."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize toml module."""
        logging.info('Inializing TomlConfig')
        self.encoding = kwargs.pop('encoding', 'utf-8')
        self.__config_parser = ConfigParser(*args, **kwargs)
        # self.__config_parser._interpolation = ExtendedInterpolation()

    @staticmethod
    def extensions() -> tuple[str, ...]:
        """Return supported file extensions."""
        return ('cfg', 'conf', 'config', 'cnf', 'ini')

    def load_config(self, filepath: str) -> dict[str, Any]:
        """Load settings from toml configuration."""
        logging.info('loading INI configuration file')
        if path.exists(filepath):
            if path.isfile(filepath):
                self.__config_parser.read([filepath], encoding=self.encoding)
            else:
                raise LoaderError(f"filepath {filepath!r} is not a file")
        else:
            raise LoaderError(f"filepath {filepath!r} does not exist")
        data = self.__config_parser._sections  # type: ignore
        for k, v in self.__config_parser._defaults.items():  # type: ignore
            data[k] = v
        return data

    def dump_config(self, content: dict[str, Any], filepath: str) -> None:
        """Save settings to toml configuration."""
        logging.info('TomlConfig: saving configuration file')
        try:
            with open(filepath, 'w', encoding=self.encoding) as file:
                self.__config_parser.write(file)
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise
