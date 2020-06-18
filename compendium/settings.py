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

        self.merge_strategy: Optional[str] = kwargs.get('merge_strategy', None)
        self.merge_sections: List[str] = kwargs.get('merge_sections', [])

        if self.merge_strategy == 'partition':
            self.load_strategy = 'nested'

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
        self.load_configs()
        for filepath in self.filepaths:
            self.__initialize_settings(self.load_config(filepath))

    def __partition_configs(self):
        self.load_configs()
        # dpath.merge(sections)

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

    def load(self, path: Optional[str] = None, filename: Optional[str] = None):
        if self.merge_strategy == 'overlay':
            self.__overlay_configs()
        elif (
            self.merge_strategy == 'partition' or self.load_strategy == 'nested'
        ):
            self.__partition_configs()
        else:
            self.__initialize_settings(self.load_config(self.head))


class NestedSettings:
    pass


class HierarchySettings:
    pass
