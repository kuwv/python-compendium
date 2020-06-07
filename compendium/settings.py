# -*- coding: utf-8 -*-
from .utils import Logger
from .filetree import FileTree
from .configs import Configs


class Settings(FileTree, Configs):
    def __getattr__(self, k):
        try:
            return self.data[k]
        except KeyError:
            raise AttributeError

    def __init__(self, application, **kwargs):
        self.__log = Logger(__name__)

        FileTree.__init__(self, application, **kwargs)
        Configs.__init__(self)

        self.__settings = {}

        # TODO: Skip all if already loaded unless 'reload' is passed

        # Load configurations
        # self.load_module(filetype)
        self.load_configs()

        if 'config' in kwargs:
            self.load_config(config_path=kwargs.get('config'))

        # TODO: writable / readonly

    @property
    def settings(self):
        return self.__settings

    def load_configs(self):
        for filepath in self.filepaths:
            self.load_config_settings(filepath)

    def get_section(self, name):
        return self.__settings[name]

    def list_sections(self, path=None):
        if path is None:
            return self.__settings.keys()
        else:
            return self.__settings[path].keys()

    def update_settings(self, new_settings):
        self.__log.debug(new_settings)
        self.__settings.update(new_settings)
