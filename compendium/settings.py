# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

import logging
import os
from typing import Any, ClassVar, Dict, List, Optional

from dpath import util as dpath  # type: ignore

from .config.paths import ConfigPaths


class Settings:
    '''Manage settings loaded from confiugrations.'''

    __defaults: ClassVar[Dict[Any, Any]] = {}
    __environs: ClassVar[Dict[Any, Any]] = {}

    def __init__(self, application: str, **kwargs):
        '''Initialize settings store.'''
        self.__settings: Dict[Any, Any] = {}
        if 'defaults' in kwargs and self.__defaults == {}:
            self.__defaults = kwargs.get('defaults')

        # Load settings from configs
        self.separator: str = kwargs.get('separator', '/')

        self.prefix = kwargs.get('prefix', application.upper() + '_')

    @property
    def defaults(self) -> Dict[Any, Any]:
        '''Return default settings.'''
        return self.__defaults

    @property
    def settings(self) -> Dict[Any, Any]:
        '''Return settings.'''
        return self.__settings

    def load_environment(self) -> None:
        '''Load environment variables.'''
        # TODO: Change env key from '_' to dict path
        env = [
            {k.replace(self.prefix, '').lower(): v}
            for k, v in os.environ.items()
            if k.startswith(self.prefix)
        ]
        if env != []:
            self.__environs = {'env': env}

    def _initialize_settings(self, new_settings: Dict[Any, Any]) -> None:
        '''Load settings store.'''
        logging.debug(new_settings)
        self.__settings.update(new_settings)
        self.load_environment()

    # Query
    def get(
        self,
        query: str,
        document: Optional[Dict[Any, Any]] = None,
        default: Optional[Any] = None,
    ):
        '''Get value from settings with key.'''
        if not document:
            document = self.__settings
        documents = [self.__environs, document, self.__defaults]
        for doc in documents:
            try:
                return dpath.get(doc, query, self.separator)
                break
            except KeyError:
                pass
        return default

    # def retrieve(self, query: str):
    #     '''Retrieve value from settings with key.'''
    #     if not self.document:
    #         self.document = self.__settings
    #     self.document = dpath.get(self.document, query, self.separator)
    #     return self

    def search(self, query: str) -> Dict[Any, Any]:
        '''Search settings matching query.'''
        return dpath.values(self.__settings, query, self.separator)

    def append(self, keypath: str, value: Any) -> None:
        '''Append to a list located at keypath.'''
        store = [value]
        keypath_dir = keypath.split(self.separator)[1:]
        for x in reversed(keypath_dir):
            store = {x: store}
        dpath.merge(self.__settings, store)
        self.save(self.head)

    def update(self, keypath: str, value: Any) -> None:
        '''Update value located at keypath.'''
        dpath.set(self.__settings, keypath, value, self.separator)
        self.save(self.head)

    def add(self, keypath: str, value: Any) -> None:
        '''Add key/value pair located at keypath.'''
        dpath.new(self.__settings, keypath, value, self.separator)

    def create(self, keypath: str, value: Any) -> None:
        '''Create new key/value pair located at path.'''
        dpath.new(self.__settings, keypath, value, self.separator)
        self.save(self.head)

    def delete(self, keypath: str) -> None:
        '''Delete key/value located at keypath.'''
        dpath.delete(self.__settings, keypath, self.separator)
        self.save(self.head)

    def view(self) -> str:
        '''View current keypath location.'''
        return self.keypath


class SettingsManager(Settings, ConfigPaths):
    def __init__(self, application, **kwargs):
        '''Initialize single settings management.

        merge_sections: []
        merge_strategy:
          - overlay
          - partition
          - last
        '''
        Settings.__init__(self, application, **kwargs)
        ConfigPaths.__init__(self, application, **kwargs)

        self.merge_strategy: Optional[str] = kwargs.get('merge_strategy', None)
        self.merge_sections: List[str] = kwargs.get('merge_sections', [])

        self.writable: Optional[bool] = kwargs.get('writable', False)

    def load(
        self, filename: Optional[str] = None, path: Optional[str] = None
    ) -> None:
        '''Load settings from configuration file.'''
        self._initialize_settings(self.load_config(self.head))

    def save(self, path: str) -> None:
        '''Save settings to configuraiton.'''
        self.save_config(self.head, self.settings)


class NestedSettingsManager(SettingsManager):
    '''Manage settings from nested configurations.'''

    def __init__(self, application, **kwargs):
        '''Initialize nested settings management.'''
        super().__init__(application, **kwargs)

        self.load_strategy = 'nested'

    def load(self, path: Optional[str] = None, filename: Optional[str] = None):
        '''Load settings from nested configuration.'''
        self.load_configs()
        settings = []
        for filepath in self.filepaths:
            settings.append(
                {'filepath': filepath, **self.load_config(filepath)}
            )
        self._initialize_settings({'settings': settings})


class HierarchySettingsManager(SettingsManager):
    '''Manage settings from hierarchy configurations.'''

    def __init__(self, application, **kwargs):
        '''Initialize settings from hirarchy filepaths.

        :param merge_sections: list, optional
            Include sections to be merged

        :param merge_strategy: list, optional
            Strategy to used when merging: overlay, parition, and last
              - overlay will replace exsisting entries
              - partition will keeps each seettings separate
              - last will only use the last loaded
        '''
        super().__init__(application, **kwargs)

        self.merge_strategy: Optional[str] = kwargs.get('merge_strategy', None)
        self.merge_sections: List[str] = kwargs.get('merge_sections', [])

    def load(self, path: Optional[str] = None, filename: Optional[str] = None):
        '''Load settings from hierarchy filepaths.'''
        self.load_configs()
        settings = {}
        for filepath in self.filepaths:
            dpath.merge(settings, self.load_config(filepath), flags=2)
        self._initialize_settings(settings)
