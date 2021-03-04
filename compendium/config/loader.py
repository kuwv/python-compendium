# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control configuration files.'''

import logging
import os
from typing import List, Optional

from anymod import PluginLoader  # type: ignore

import compendium
from compendium import exceptions
from compendium.settings import Settings


class ConfigFile:
    '''Manage configuration files using dynamic module loader.'''

    def __init__(
        self,
        filetype: str = 'toml',
        driver_paths: Optional[List[str]] = None,
        **kwargs,
    ):
        '''Initialize module loader.'''
        # TODO: writable / readonly
        self.filetype = filetype
        self.basepath: Optional[str] = None
        self.driver_paths: List[str] = [
            compendium.__path__[0].rsplit(os.sep, 1)[0]  # type: ignore
        ]
        if driver_paths:
            self.driver_paths += driver_paths

    def _load_module(
        self,
        filepath: Optional[str] = None,
        filetype: Optional[str] = None
    ):
        '''Dynamically load the appropriate module.'''
        logging.info('Loading configuration modules')
        __filetype = filetype or self.filetype
        loader = PluginLoader(self.driver_paths)
        __plugin_dir = loader.find_packages(name='compendium')[0]
        module_path = loader.get_import_path(
            __filetype, __plugin_dir['module_finder'].path
        )

        # TODO: Check if module is already loaded
        if module_path is not None and module_path != []:
            classname = "{}Config".format(__filetype.capitalize())
            config_class = loader.load_classpath(
                "{m}.{c}".format(m=module_path, c=classname)
            )
            self.__config_module = config_class()
            logging.info('Finished loading configs')
        else:
            raise exceptions.CompendiumDriverError(
                'driver not found'
            )

    def load_config(self, filepath: str, filetype: str = None):
        '''Use discovered module to load configuration.'''
        # TODO: Improve error handling
        if os.path.exists(filepath):
            logging.info("Retrieving configuration: '{}'".format(filepath))
            self._load_module(filetype or self.filetype)
            return self.__config_module.load_config(filepath)
        else:
            raise exceptions.CompendiumConfigFileError(
                "Skipping: No configuration found at: '{}'".format(filepath)
            )

    def dump_config(
        self,
        filepath: str,
        filetype: Optional[str] = None,
        settings: Settings = None,
    ):
        '''Use discovered module to save configuration.'''
        # TODO: Improve error handling
        logging.info("Saving configuration: '{}'".format(filepath))
        self._load_module(filetype)
        self.__config_module.dump_config(settings, filepath)
