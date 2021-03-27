# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control configuration files.'''

import logging
import os
from typing import Any, Dict, Optional, Type
# from weakref import ref

from compendium import exceptions
from compendium.config import ConfigBase
from compendium.config.filetypes.json import JsonConfig  # noqa
from compendium.config.filetypes.toml import TomlConfig  # noqa
from compendium.config.filetypes.xml import XmlConfig  # noqa
from compendium.config.filetypes.yaml import YamlConfig  # noqa


class ConfigFile:
    '''Manage configuration files using dynamic module loader.'''

    def __init__(
        self,
        filetype: str = 'toml',
        **kwargs,
    ) -> None:
        '''Initialize module loader.'''
        # TODO: writable / readonly
        self.filetype = filetype
        self.modules = [m for m in ConfigBase.__subclasses__()]

    @staticmethod
    def get_filetype(filepath: str) -> Optional[str]:
        '''Get filetype from filepath.'''
        if '.' in filepath:
            return os.path.splitext(filepath)[1].strip('.')
        else:
            return None

    def _get_class(
        self,
        filetype: Optional[str] = None
    ) -> Optional[Type[ConfigBase]]:
        '''Get class object from filetype module.'''
        filetype = filetype or self.filetype
        for module in self.modules:
            if filetype in module.filetypes():  # type: ignore
                return module
        return None

    def load_config(
        self,
        filepath: str,
        filetype: str = None
    ) -> Dict[str, Any]:
        '''Use discovered module to load configuration.'''
        if os.path.exists(filepath):
            logging.info("Retrieving configuration: '{}'".format(filepath))
            Class = self._get_class(filetype)
            if Class:
                cls = Class()
                return cls.load_config(filepath=filepath)
            else:
                raise exceptions.CompendiumDriverError(
                    "Error: No class found for: '{}'".format(filepath)
                )
        else:
            raise exceptions.CompendiumConfigFileError(
                "Skipping: No configuration found at: '{}'".format(filepath)
            )

    def dump_config(self, filepath: str, settings: Dict[str, Any]) -> None:
        '''Use discovered module to save configuration.'''
        logging.info("Saving configuration: '{}'".format(filepath))
        Class = self._get_class(self.get_filetype(filepath))
        if Class:
            cls = Class()
            cls.dump_config(settings, filepath)
        else:
            raise exceptions.CompendiumDriverError(
                "Skipping: No class found for: '{}'".format(filepath)
            )
