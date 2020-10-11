# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control configuration files.'''

import logging
import os
from typing import Any, Dict, List, Optional

from anymod import ModuleLoader  # type: ignore


class ConfigFile:
    '''Manage configuration files using dynamic module loader.'''

    def __init__(
        self,
        filetype: str = None,
        driver_directories: List[str] = [
            os.path.join('compendium', 'config', 'filetypes')
        ],
        **kwargs
    ):
        '''Initialize module loader.'''
        # TODO: writable / readonly
        self.driver_directories = driver_directories
        self._filepaths: List[str] = []
        self.base_path: Optional[str] = None
        self.filename = 'settings.toml'
        self.filetype = 'toml'

        def __get_filetype(self, args):
            if 'filetype' in args:
                return args['filetype']
            else:
                return self.get_filetype(self.filename)

        if 'path' in kwargs:
            self._filepaths.append(kwargs['path'])
            self.base_path, self.filename = self.split_filepath(
                self._filepaths[0]
            )
            self.filetype = __get_filetype(self, kwargs)
        elif 'filename' in kwargs:
            self.filename = kwargs['filename']
            self.filetype = __get_filetype(self, kwargs)

    def _load_module(self):
        '''Dynamically load the appropriate module.'''
        logging.info('Loading configuration modules')
        mod = ModuleLoader(self.driver_directories)
        module_path = mod.discover_module_path(self.filetype)

        if module_path is not None:
            classname = ".{p}Config".format(p=self.filetype.capitalize())
            config_class = mod.load_classpath(
                "{m}{c}".format(m=module_path, c=classname)
            )
            self.__config_module = config_class()
            logging.info('Finished loading configs')
        else:
            logging.info('Unable to load configs')

    def load_config(self, config_path: str):
        '''Use discovered module to load configuration.'''
        # TODO: Improve error handling
        if os.path.exists(config_path):
            logging.info("Retrieving configuration: '{}'".format(config_path))
            if not self.filetype:
                filename = self.get_filename(config_path)
                self.filetype = self.get_filetype(filename)
            self._load_module()
            return self.__config_module.load_config(config_path)
        else:
            logging.info(
                "Skipping: No configuration found at: '{}'".format(config_path)
            )

    def save_config(self, config_path: str, settings: Dict[Any, Any]):
        '''Use duscovered module to save configuration.'''
        # TODO: Improve error handling
        logging.info("Saving configuration: '{}'".format(config_path))
        # filename = self.get_filename(config_path)
        self._load_module()
        self.__config_module.save_config(settings, config_path)

    def _check_path(self, filepath: str):
        '''Check if configuraion exists at path.'''
        if os.path.isfile(filepath):
            logging.debug("{} found".format(filepath))
            return True
        else:
            logging.debug("{} not found".format(filepath))
            return False

    @staticmethod
    def get_filename(filepath: str):
        '''Get the name of the file.'''
        return filepath.rsplit('/', 1)[1]

    @staticmethod
    def split_filepath(filepath: str):
        '''Separate filename from filepath.'''
        return filepath.rsplit('/', 1)

    @staticmethod
    def get_filetype(filename: str):
        '''Get filetype from filename.'''
        return filename.split('.')[-1]

    @property
    def head(self):
        '''Retrieve head filepath.'''
        return self._filepaths[-1]

    # @property
    # def tail(self):
    #     '''Retrieve beggining filepath.'''
    #     return self._filepaths[0]

    @property
    def filepaths(self):
        '''Retrieve filepaths.'''
        return self._filepaths

    def load_filepath(self, filepath: str):
        '''Load settings from configuration in filepath.'''
        logging.debug("searching for {}".format(filepath))

        if self._check_path(filepath):
            self._filepaths.append(filepath)
