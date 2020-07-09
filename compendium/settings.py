# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict, List, Optional

from dpath import util as dpath  # type: ignore

from .config.paths import ConfigPaths


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

    def _initialize_settings(self, new_settings: Dict[Any, Any]) -> None:
        logging.debug(new_settings)
        self.__settings.update(new_settings)

    # Query
    def get(self, query: str, document: Optional[Dict[Any, Any]] = None):
        if not document:
            document = self.__settings
        return dpath.get(document, query, self.separator)

    # def retrieve(self, query: str):
    #     if not self.document:
    #         self.document = self.__settings
    #     self.document = dpath.get(self.document, query, self.separator)
    #     return self

    def search(self, query: str) -> Dict[Any, Any]:
        return dpath.values(self.__settings, query, self.separator)

    def append(self, keypath: str, value: Any) -> None:
        store = [value]
        keypathpath = keypath.split(self.separator)[1:]
        for x in reversed(keypathpath):
            store = {x: store}
        dpath.merge(self.__settings, store)
        self.save(self.head)

    def update(self, keypath: str, value: Any) -> None:
        dpath.set(self.__settings, keypath, value, self.separator)
        self.save(self.head)

    def add(self, keypath: str, value: Any) -> None:
        dpath.new(self.__settings, keypath, value, self.separator)

    def create(self, keypath: str, value: Any) -> None:
        dpath.new(self.__settings, keypath, value, self.separator)
        self.save(self.head)

    def delete(self, keypath: str) -> None:
        dpath.delete(self.__settings, keypath, self.separator)
        self.save(self.head)

    def load(
        self, path: Optional[str] = None, filename: Optional[str] = None
    ) -> None:
        self._initialize_settings(self.load_config(self.head))

    def view(self) -> str:
        return self.keypath

    def save(self, path: str) -> None:
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

        Parameters:
        -----------
        merge_sections: list, optional
            Include sections to be merged

        merge_strategy: list, optional
            Strategy to used when merging: overlay, parition, and last
              - overlay will replace exsisting entries
              - partition will keeps each seettings separate
              - last will only use the last loaded
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
