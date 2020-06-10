# -*- coding: utf-8 -*-
# import codecs
import os
from .config_base import ConfigBase
# TODO: Implement importlib find_module
from .json import JsonConfig  # noqa
from .toml import TomlConfig  # noqa
from .yaml import YamlConfig  # noqa
from ..utils import Logger, ModuleLoader


class Configs:
    def __init__(self):
        self.__log = Logger(__name__)
        self.modules = [m for m in ConfigBase.__subclasses__()]

    def __discovery_loader(self, filetype):
        for module in self.modules:
            if filetype in module.filetypes():
                return (module.__module__ + '.' + module.__name__)
        return None

    def __load_module(self, filename):
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

    def load_config_settings(self, config_path):
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

    def save_config_settings(self, config_path, settings):
        # TODO: Improve error handling
        self.__log.info(
            "Saving configuration: '{}'".format(config_path)
        )
        filename = self.get_filename(config_path)
        self.__load_module(filename)
        self.__config_module.save_config(settings, config_path)

    def _check_path(self, filepath):
        if os.path.isfile(filepath):
            self.__log.debug("{f} found".format(f=filepath))
            return True
        else:
            self.__log.debug("{f} not found".format(f=filepath))
            return False

    @staticmethod
    def __make_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def get_filename(filepath):
        return filepath.rsplit('/', 1)[1]

    @staticmethod
    def get_base_path(filepath):
        return filepath.rsplit('/', 1)[0]

    @staticmethod
    def split_filepath(filepath):
        return filepath.rsplit('/', 1)

    @staticmethod
    def get_filetype(filename):
        return filename.split('.')[-1]
