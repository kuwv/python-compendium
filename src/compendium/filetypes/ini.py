# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control toml configuration module."""

import errno
import logging
from configparser import ConfigParser  # ExtendedInterpolation
from typing import Any, Dict, Tuple

from compendium.filetypes_base import FiletypesBase


class IniConfig(FiletypesBase):
    """Manage toml configurations."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize toml module."""
        logging.info('Inializing TomlConfig')
        self.encoding = kwargs.pop('encoding', 'utf-8')
        self.__config_parser = ConfigParser(*args, **kwargs)
        # self.__config_parser._interpolation = ExtendedInterpolation()

    @staticmethod
    def filetypes() -> Tuple[str, ...]:
        """Return supported filetypes."""
        return ('cfg', 'conf', 'config', 'cnf', 'ini')

    def load_config(self, filepath: str) -> Dict[str, Any]:
        """Load settings from toml configuration."""
        logging.info('loading INI configuration file')
        try:
            self.__config_parser.read([filepath], encoding=self.encoding)
        except Exception:
            logging.error('Unable to read file')
        data = self.__config_parser._sections  # type: ignore
        for k, v in self.__config_parser._defaults.items():  # type: ignore
            data[k] = v
        return data

    def dump_config(self, content: Dict[str, Any], filepath: str) -> None:
        """Save settings to toml configuration."""
        logging.info('TomlConfig: saving configuration file')
        try:
            with open(filepath, 'w') as f:
                self.__config_parser.write(f)
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise
