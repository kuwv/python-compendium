# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control toml configuration module.'''

import errno
import logging
from collections import defaultdict
from configparser import ConfigParser  # ExtendedInterpolation
from typing import Any, Dict, List

from compendium.filetypes_base import FiletypesBase


class IniConfig(FiletypesBase):
    '''Manage toml configurations.'''

    def __init__(self, **kwargs: Any) -> None:
        '''Initialize toml module.'''
        logging.info('Inializing TomlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.__config_parser = ConfigParser(dict_type=defaultdict)
        # self.__config_parser._interpolation = ExtendedInterpolation()

    @staticmethod
    def filetypes() -> List[str]:
        '''Return supported filetypes.'''
        return ['cfg', 'conf', 'config', 'cnf', 'ini']

    def load_config(self, filepath: str) -> Dict[str, Any]:
        '''Load settings from toml configuration.'''
        logging.info('loading INI configuration file')
        try:
            self.__config_parser.read([filepath])
        except Exception:
            logging.error('Unabled to read file')
        return self.__config_parser._sections  # type: ignore

    def dump_config(self, content: Dict[str, Any], filepath: str) -> None:
        '''Save settings to toml configuration.'''
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
