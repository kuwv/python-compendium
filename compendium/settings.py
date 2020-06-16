# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional

# TODO: test ASQ as async
from dpath import util as dpath  # type: ignore

from .config_manager import ConfigPaths
from .utils import Logger


class Settings(ConfigPaths):

    # __defaults: ClassVar[Dict[Any, Any]] = {}

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

        self.__settings: Dict[Any, Any] = {}

        # Load settings from configs
        self.separator: str = kwargs.get('separator', '.')
        self.merge_strategy: str = kwargs.get('merge_strategy', 'last')
        self.merge_sections: List[str] = kwargs.get('merge_sections', [])

        # TODO: load environment variables

    # @property
    # def defaults(self) -> Dict[Any, Any]:
    #     return self.__defaults

    @property
    def settings(self) -> Dict[Any, Any]:
        return self.__settings

    def __initialize_settings(self, new_settings: Dict[Any, Any]):
        self.__log.debug(new_settings)
        self.__settings.update(new_settings)

    # Merge stategy
    def __overlay_configs(self):
        for filepath in self.filepaths:
            self.__initialize_settings(self.load_config(filepath))

    def __partition_configs(self, sections):
        # dpath.merge(sections)
        pass

    def __last_config(self):
        self.__initialize_settings(self.load_config(self.head))

    # Query
    def create(self, key: str, value: Any):
        dpath.new(self.__settings, key, value, self.separator)
        self.save_config(self.head, self.__settings)

    def get(self, key: str):
        return dpath.get(self.__settings, key, self.separator)

    def search(self, query: str):
        return dpath.values(self.__settings, query, self.separator)

    def update(self, key: str, value: Any):
        dpath.set(self.__settings, key, value, self.separator)
        self.save_config(self.head, self.__settings)

    def delete(self, key: str):
        dpath.delete(self.__settings, key, self.separator)
        self.save_config(self.head, self.__settings)

    def load(self, filepath: Optional[str] = None):
        if self.merge_strategy == 'overlay':
            self.__overlay_configs()

        if self.merge_strategy == 'partition' or self.load_strategy == 'nested':
            self.__partition_configs(self.merge_sections)

        if self.merge_strategy == 'last':
            self.__last_config()
