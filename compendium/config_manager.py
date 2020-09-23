# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

from typing import Any, Dict, List, Optional

from dpath import util as dpath  # type: ignore

from .config.paths import ConfigPaths
from .settings import Settings


class ConfigManager(Settings, ConfigPaths):
    '''Manage settings from cache.'''

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
        self, path: Optional[str] = None, filename: Optional[str] = None
    ) -> None:
        '''Load settings from configuration file.'''
        self._initialize_settings(self.load_config(self.head))

    def save(self, path: str, filetype: str = None) -> None:
        '''Save settings to configuraiton.'''
        self.save_config(self.head, self.settings)


class NestedConfigManager(ConfigManager):
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


class HierarchyConfigManager(ConfigManager):
    '''Manage settings from hierarchy configurations.'''

    def __init__(self, application, **kwargs):
        '''Initialize settings from hirarchy filepaths.

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
        '''Load settings from hierarchy filepaths.'''
        self.load_configs()
        settings: Dict[Any, Any] = {}
        for filepath in self.filepaths:
            dpath.merge(settings, self.load_config(filepath), flags=2)
        self._initialize_settings(settings)
