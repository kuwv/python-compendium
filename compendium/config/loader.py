'''Control configuration files.'''
# -*- coding: utf-8 -*-
# import codecs
import logging
import os
from typing import Any, Dict

from anymod import ModuleLoader


class ConfigFile:
    '''Manage configuration files using dynamic module loader.'''

    def __init__(self, filetype=None, driver_directories=['compendium/config/filetypes']):
        '''Initialize module loader.'''
        self.filetype = filetype
        self.driver_directories = driver_directories

    def _load_module(self):
        '''Dynamically load the appropriate module.'''
        logging.info('Loading configuration modules')
        mod = ModuleLoader(self.driver_directories)
        module_path = mod.discover_module_path(self.filetype)

        if module_path is not None:
            classname = '.' + self.filetype.capitalize() + 'Config'
            config_class = mod.load_classpath(module_path + classname)
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
        filename = self.get_filename(config_path)
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
        '''Get filetype from filename.

        :param filename: str, required
            Filename to retrieve filetype
        '''
        return filename.split('.')[-1]
