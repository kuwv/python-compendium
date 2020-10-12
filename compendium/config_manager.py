# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

import glob
import logging
import os
import platform
from typing import Any, Dict, List, Optional, Union

from dpath import util as dpath  # type: ignore

from . import logger
from .config import ConfigFile
from .settings import Settings


class ConfigManager(Settings, ConfigFile):
    '''Manage settings from cache.'''

    def __init__(self, application, **kwargs):
        '''Initialize single settings management.

        merge_sections: []
        merge_strategy:
          - overlay
          - partition
          - last

        '''
        if kwargs.get('debug', False):
            logger.basicConfig()
            logger.getLogger().setLevel(logging.DEBUG)

        self._filepaths: List[str] = []
        self._enumerate_paths(
            filepath=kwargs.get('path', None),
            filename=kwargs.get('filename', None),
            filetype=kwargs.get('filetype', None)
        )

        ConfigFile.__init__(self, **kwargs)
        Settings.__init__(self, application, **kwargs)

        self.merge_strategy: Optional[str] = kwargs.get('merge_strategy', None)
        self.merge_sections: List[str] = kwargs.get('merge_sections', [])

        self.writable: Optional[bool] = kwargs.get('writable', False)

    @property
    def head(self):
        '''Retrieve head filepath.'''
        return self._filepaths[-1]

    # @property
    # def tail(self):
    #     '''Retrieve beggining filepath.'''
    #     return self._filepaths[0]

    @property
    def filepaths(self):
        '''Retrieve filepaths.'''
        return self._filepaths

    def _enumerate_paths(
        self,
        filepath: str = None,
        filename: str = None,
        filetype: str = None,
    ):
        if self._filepaths == []:
            if filepath:
                self._filepaths.append(filepath)
                self.base_path, self.filename = self.split_filepath(filepath)
                self.filetype = self.get_filetype(self.filename)
            elif filename:
                self.filename = filename
                self.filetype = self.get_filetype(self.filename)
            else:
                self.filename = 'settings.toml'
                self.filetype = 'toml'

    def _check_path(self, filepath: str):
        '''Check if configuraion exists at path.'''
        if os.path.isfile(filepath):
            logging.debug("{} found".format(filepath))
            return True
        else:
            logging.debug("{} not found".format(filepath))
            return False

    def load_filepath(self, filepath: str):
        '''Load settings from configuration in filepath.'''
        logging.debug("searching for {}".format(filepath))

        if self._check_path(filepath):
            self._filepaths.append(filepath)

    def load(
        self, path: Optional[str] = None, filetype: Optional[str] = None
    ) -> None:
        '''Load settings from configuration file.'''
        self._enumerate_paths(filepath=path, filetype=filetype)
        self._initialize_settings(self.load_config(self.head))

    def save(self, path: str, filetype: str = None) -> None:
        '''Save settings to configuraiton.'''
        self.save_config(self.head, self.settings)


class NestedConfigManager(ConfigManager):
    '''Manage settings from nested configurations.'''

    def __init__(self, application, **kwargs):
        '''Initialize nested settings management.'''
        super().__init__(application, **kwargs)

    def _load_configs(self, path: Optional[str] = None):
        '''Load configurations located in nested directory path.'''
        for filepath in glob.iglob(
            "/**/{f}".format(f=self.filename), recursive=True
        ):
            self.load_filepath(filepath)

    def load(self, path: Optional[str] = None, filetype: Optional[str] = None):
        '''Load settings from nested configuration.'''
        self._load_configs()
        settings = []
        for filepath in self._filepaths:
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

        self.enable_system_paths: Union[str, bool] = kwargs.get(
            'enable_system_paths', False
        )
        self.enable_user_paths: Union[str, bool] = kwargs.get(
            'enable_user_paths', False
        )
        self.enable_local_paths: Union[str, bool] = kwargs.get(
            'enable_local_paths', True
        )

    # TODO: Implement pathlib
    def _load_configs(self):
        r'''Load config paths based on priority.

        First(lowest) to last(highest)
        1. Load settings.<FILETYPE> from /etc/<APP>
          - /etc/<APP>/settings.<FILETYPE>
          - /etc/<APP>/<FILENAME>
        2. Load user configs
          - Windows: ~\\AppData\\Local\\<COMPANY>\\<APP>\\<FILENAME>
          - Darwin: ~/Library/Application Support/<APP>/<FILENAME>
          - Linux: ~/.config/<APP>/<FILENAME>
          - ~/.<APP>.<FILETYPE>
          - ~/.<APP>.d/<FILENAME>
        3. Load config in PWD
          - ./settings.<FILETYPE>
          - ./<FILENAME>
        4. Runtime configs:
          - /etc/sysconfig/<APP>
          - .env
          - <CLI>

        '''
        logging.info('populating settings locations')

        if self.enable_system_paths and os.name == 'posix':
            self.load_filepath(
                os.path.join(os.sep, 'etc', self.application, self.filename)
            )
            self.load_filepath(
                os.path.join(os.sep, 'etc', self.application, self.filename)
            )
        # TODO: Add windows/linux compliant service path config option

        if self.enable_user_paths:
            if platform.system() == 'Windows':
                __user_app_path = os.path.join('AppData', 'Local')

            if platform.system() == 'Darwin':
                __user_app_path = os.path.join('Library', 'Application Support')

            if platform.system() == 'Linux':
                __user_app_path = '.config'

            self.load_filepath(
                os.path.join(
                    os.path.expanduser('~'),
                    __user_app_path,
                    self.application,
                    self.filename,
                )
            )

            self.load_filepath(
                os.path.join(
                    os.path.expanduser('~'),
                    ".{a}.{f}".format(a=self.application, f=self.filetype),
                )
            )
            self.load_filepath(
                os.path.join(
                    os.path.expanduser('~'),
                    ".{a}.d".format(a=self.application),
                    self.filename,
                )
            )

        if self.enable_local_paths:
            self.load_filepath(os.path.join(os.getcwd(), self.filename))
            self.load_filepath(
                os.path.join(
                    os.getcwd(),
                    "{a}.{f}".format(a=self.application, f=self.filetype),
                )
            )

    def load(self, path: Optional[str] = None, filetype: Optional[str] = None):
        '''Load settings from hierarchy filepaths.'''
        self._load_configs()
        settings: Dict[Any, Any] = {}
        for filepath in self._filepaths:
            dpath.merge(settings, self.load_config(filepath), flags=2)
        self._initialize_settings(settings)
