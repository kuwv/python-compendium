# -*- coding: utf-8 -*-
import jmespath  # type: ignore
from .utils import Logger
from .config_manager import ConfigManager
from typing import Any, Dict, KeysView


class Settings(ConfigManager):

    __defaults: Dict[Any, Any] = {}
    __settings: Dict[Any, Any] = {}

    def __init__(self, application, **kwargs):
        '''
        merge_sections: []
        merge_strategy:
          - overlay
          - partition
          - last
        '''
        self.__log = Logger(__name__)

        super().__init__(application, **kwargs)

        # Load settings from configs
        self.merge_strategy: str = kwargs.get('merge_strategy', 'last')

        if self.merge_strategy == 'overlay':
            self.__overlay_configs()

        if self.merge_strategy == 'partition' or self.load_strategy == 'nested':
            self.__partition_configs(kwargs.get('merge_sections'))

        if self.merge_strategy == 'last':
            self.__last_config()

        # TODO: load environment variables

    @property
    def settings(self) -> Dict[Any, Any]:
        return self.__settings

    def __overlay_configs(self):
        for filepath in self.filepaths:
            self.update_settings(self.load_config_settings(filepath))

    def __partition_configs(self, sections):
        pass

    def __last_config(self):
        self.update_settings(self.load_config_settings(self.filepaths[-1]))

    def get_section(self, name) -> Dict[Any, Any]:
        return jmespath.compile(name)

    def list_sections(self, path=None) -> KeysView[Any]:
        if path is None:
            return self.__settings.keys()
        else:
            return self.__settings[path].keys()

    def update_settings(self, new_settings):
        self.__log.debug(new_settings)
        self.__settings.update(new_settings)

    def save_settings(self):
        self.save_config_settings(self.filepaths[-1], self.__settings)
