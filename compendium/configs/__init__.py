# -*- coding: utf-8 -*-
# import codecs
import os
from .config_base import ConfigBase
from .ini import IniConfig  # noqa
from .json import JsonConfig  # noqa
from .toml import TomlConfig  # noqa
from .yaml import YamlConfig  # noqa
from ..utils import ModuleLoader
from ..utils import Logger


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
        filetype = filename.split('.')[-1]
        module_path = self.__discovery_loader(filetype)
        if module_path is not None:
            config_class = mod.load_classpath(module_path)
            self._config_file = config_class()
            self.__log.info('Finished loading configs')
        else:
            self.__log.info('unable to load configs')

    def load_config_settings(self, config_path):
        # TODO: Improve error handling
        if os.path.exists(config_path):
            self.__log.info("Loading configuration: '{}'".format(config_path))
            filename = config_path.rsplit('/', 1)[1]
            self.__load_module(filename)
            self._config_file.load_config(filepath=config_path)
            self.update_settings(self._config_file.get_config())
            self.__log.info(
                "Finished loading configuration: '{}'".format(config_path)
            )
        else:
            self.__log.info(
                "Skipping: No configuration found at: '{}'".format(config_path)
            )

    # def load_configs(self, filepaths):
    #     for filepath in filepaths:
    #         self.load_config_settings(filepath)
