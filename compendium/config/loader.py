# -*- coding: utf-8 -*-
# import codecs
import os

from ..utils import Logger, ModuleLoader
from .config_base import ConfigBase
# TODO: Implement importlib find_module
from .filetypes.json import JsonConfig  # noqa
from .filetypes.toml import TomlConfig  # noqa
from .filetypes.yaml import YamlConfig  # noqa

from typing import Any, Dict


class ConfigFile:
    def __init__(self):
        self.__log = Logger(__name__)
        self.modules = [m for m in ConfigBase.__subclasses__()]

    def __discovery_loader(self, filetype):
        for module in self.modules:
            if filetype in module.filetypes():
                return (module.__module__ + '.' + module.__name__)
        return None

    def __load_module(self, filename: str):
        self.__log.info('Loading configuration configs')
        mod = ModuleLoader()

        # TODO: figure out which driver to load from filetypes
        filetype = self.get_filetype(filename)
        module_path = self.__discovery_loader(filetype)
        if module_path is not None:
            config_class = mod.load_classpath(module_path)
            self.__config_module = config_class()
            self.__log.info('Finished loading configs')
        else:
            self.__log.info('unable to load configs')

    def load_config(self, config_path: str):
        # TODO: Improve error handling
        if os.path.exists(config_path):
            self.__log.info(
                "Retrieving configuration: '{}'".format(config_path)
            )
            filename = self.get_filename(config_path)
            self.__load_module(filename)
            return self.__config_module.load_config(config_path)
        else:
            self.__log.info(
                "Skipping: No configuration found at: '{}'".format(config_path)
            )

    def save_config(self, config_path: str, settings: Dict[Any, Any]):
        # TODO: Improve error handling
        self.__log.info(
            "Saving configuration: '{}'".format(config_path)
        )
        filename = self.get_filename(config_path)
        self.__load_module(filename)
        self.__config_module.save_config(settings, config_path)

    def _check_path(self, filepath: str):
        if os.path.isfile(filepath):
            self.__log.debug("{} found".format(filepath))
            return True
        else:
            self.__log.debug("{} not found".format(filepath))
            return False

    @staticmethod
    def __make_directory(directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def get_filename(filepath: str):
        return filepath.rsplit('/', 1)[1]

    @staticmethod
    def split_filepath(filepath: str):
        return filepath.rsplit('/', 1)

    @staticmethod
    def get_filetype(filename: str):
        return filename.split('.')[-1]
