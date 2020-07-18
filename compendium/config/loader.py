'''Control configuration files.'''
# -*- coding: utf-8 -*-
# import codecs
import logging
import os
from typing import Any, Dict

from anymod import ModuleLoader
from .config_base import ConfigBase

# TODO: Implement importlib find_module
from .filetypes.json import JsonConfig  # noqa
from .filetypes.toml import TomlConfig  # noqa
from .filetypes.xml import XmlConfig  # noqa
from .filetypes.yaml import YamlConfig  # noqa


class ConfigFile:
    '''Manage configuration files using dynamic module loader.'''

    def __init__(self):
        '''Initialize module loader.

        Retrieve supported filetypes from each module
        '''
        self.modules = [m for m in ConfigBase.__subclasses__()]

    def __discovery_loader(self, filetype):
        '''Load the module matching the supported filetype.'''
        for module in self.modules:
            if filetype in module.filetypes():
                return (module.__module__ + '.' + module.__name__)
        return None

    def _load_module(self, filetype: str):
        '''Dynamically load the appropriate module.'''
        logging.info('Loading configuration configs')
        mod = ModuleLoader()

        # TODO: figure out which driver to load from filetypes
        module_path = self.__discovery_loader(filetype)
        if module_path is not None:
            config_class = mod.load_classpath(module_path)
            self.__config_module = config_class()
            logging.info('Finished loading configs')
        else:
            logging.info('unable to load configs')

    def load_config(self, config_path: str, filetype: str = None):
        '''Use discovered module to load configuration.'''
        # TODO: Improve error handling
        if os.path.exists(config_path):
            logging.info("Retrieving configuration: '{}'".format(config_path))
            if not filetype:
                filename = self.get_filename(config_path)
                filetype = self.get_filetype(filename)
            self._load_module(filetype)
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
        self._load_module(filename)
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
