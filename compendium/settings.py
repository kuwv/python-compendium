# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict, List, Optional

from dpath import util as dpath  # type: ignore

from .config_manager import ConfigPaths


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
        super().__init__(application, **kwargs)

        self.__settings: Dict[Any, Any] = {}

        # Load settings from configs
        self.separator: str = kwargs.get('separator', '/')

        self.merge_strategy: Optional[str] = kwargs.get('merge_strategy', None)
        self.merge_sections: List[str] = kwargs.get('merge_sections', [])

        self.writable: Optional[bool] = kwargs.get('writable', False)
        # TODO: load environment variables

    # @property
    # def defaults(self) -> Dict[Any, Any]:
    #     return self.__defaults

    @property
    def settings(self) -> Dict[Any, Any]:
        return self.__settings

    def _initialize_settings(self, new_settings: Dict[Any, Any]):
        logging.debug(new_settings)
        self.__settings.update(new_settings)

    # Query
    def get(self, key: str, document: Optional[Dict[Any, Any]] = None):
        if not document:
            document = self.__settings
        return dpath.get(document, key, self.separator)

    def search(self, query: str):
        return dpath.values(self.__settings, query, self.separator)

    def append(self, query: str, value: Any):
        dpath.merge(self.__settings, value)
        self.save(self.head)

    def update(self, key: str, value: Any):
        dpath.set(self.__settings, key, value, self.separator)
        self.save(self.head)

    def create(self, key: str, value: Any):
        dpath.new(self.__settings, key, value, self.separator)
        self.save(self.head)

    def delete(self, key: str):
        dpath.delete(self.__settings, key, self.separator)
        self.save(self.head)

    def load(self, path: Optional[str] = None, filename: Optional[str] = None):
        self._initialize_settings(self.load_config(self.head))

    def view(self):
        return self.query

    def save(self, path: str):
        self.save_config(self.head, self.__settings)


class NestedSettings(Settings):
    def __init__(self, application, **kwargs):
        super().__init__(application, **kwargs)

        self.load_strategy = 'nested'

    def load(self, path: Optional[str] = None, filename: Optional[str] = None):
        self.load_configs()
        settings = []
        for filepath in self.filepaths:
            settings.append(
                {'filepath': filepath, **self.load_config(filepath)}
            )
        self._initialize_settings({'settings': settings})


class HierarchySettings(Settings):
    def __init__(self, application, **kwargs):
        '''
        merge_sections: []
        merge_strategy:
          - overlay
          - partition
          - last
        '''
        super().__init__(application, **kwargs)

        self.merge_strategy: Optional[str] = kwargs.get('merge_strategy', None)
        self.merge_sections: List[str] = kwargs.get('merge_sections', [])

    def load(self, path: Optional[str] = None, filename: Optional[str] = None):
        self.load_configs()
        settings = {}
        for filepath in self.filepaths:
            dpath.merge(settings, self.load_config(filepath), flags=2)
        self._initialize_settings(settings)
