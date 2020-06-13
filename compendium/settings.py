# -*- coding: utf-8 -*-
import collections
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
    def defaults(self) -> Dict[Any, Any]:
        return self.__defaults

    @property
    def settings(self) -> Dict[Any, Any]:
        return self.__settings

    def __update_settings(self, new_settings):
        self.__log.debug(new_settings)
        self.__settings.update(new_settings)

    def __overlay_configs(self):
        for filepath in self.filepaths:
            self.__update_settings(self.load_config_settings(filepath))

    def __partition_configs(self, sections):
        pass

    def __last_config(self):
        self.__update_settings(self.load_config_settings(self.head))

    def compile(self, query) -> Dict[Any, Any]:
        return jmespath.compile(query)

    def list_sections(self) -> KeysView[Any]:
        return jmespath.search('keys(@)', self.__settings)

    def search(self, expression, path=None):
        return jmespath.search(
            expression,
            self.__settings,
            options=jmespath.Options(dict_cls=collections.OrderedDict),
        )

    def update(self, content):
        print(self.settings)
        self.__update_settings(content)
        print(self.settings)
        self.save_config_settings(self.head, self.__settings)
