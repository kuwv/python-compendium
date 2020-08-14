# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide configuration filepaths.'''
import glob
import logging
import os
from typing import List, Optional, Union

from . import ConfigFile


class ConfigPaths(ConfigFile):
    '''Manage configuration paths.'''

    # TODO: Skip all if already loaded unless 'reload' is passed
    def __init__(self, application: str, **kwargs: str):
        '''Initialize configuration path topology.

        load_strategy:
          - singleton
          - hierarchy
          - nested
        '''
        super().__init__()

        self.application: str = application

        self.load_strategy: str = kwargs.get('load_strategy', 'hierarchy')
        self.enable_system_paths: Union[str, bool] = kwargs.get(
            'enable_system_paths', False
        )
        self.enable_user_paths: Union[str, bool] = kwargs.get(
            'enable_user_paths', False
        )
        self.enable_local_paths: Union[str, bool] = kwargs.get(
            'enable_local_paths', True
        )

        # TODO: writable / readonly
        self.filepaths: List[str] = []
        self.base_path: Optional[str] = None

        if 'path' in kwargs:
            self.load_strategy = 'singleton'
            self.filepaths.append(kwargs.get('path'))
            self.base_path, self.filename = self.split_filepath(
                self.filepaths[0]
            )
            self.filetype = self.get_filetype(self.filename)
        elif 'filename' in kwargs:
            self.filename = kwargs.get('filename')
            self.filetype = self.get_filetype(self.filename)
        else:
            self.filename = 'settings.toml'
            self.filetype = 'toml'

    # @property
    # def tail(self):
    #     '''Retrieve beggining filepath.'''
    #     return self.filepaths[0]

    @property
    def head(self):
        '''Retrieve head filepath.'''
        return self.filepaths[-1]

    def _load_filepath(self, filepath: str):
        '''Load settings from configuration in filepath.'''
        logging.debug("searching for {}".format(filepath))

        if self._check_path(filepath):
            self.filepaths.append(filepath)

    # TODO: Implement pathlib
    def load_config_filepaths(self):
        '''Load config paths based on priority.

        First(lowest) to last(highest)
        1. Load settings.<FILETYPE> from /etc/<APP>
            - /etc/<APP>/settings.<FILETYPE>
            - /etc/<APP>/<CONFIG>.<FILETYPE>
        2. Load user configs
            - ~/.<APP>.<FILETYPE>
            - ~/.<APP>.d/settings.<FILETYPE>
        3. Load config in PWD
            - ./settings.<FILETYPE>
            - ./<CONFIG>.<FILETYPE>
        4. Runtime configs: (environment.py)
            - /etc/sysconfig/<APP>
            - .env
            - <CLI>
        '''
        logging.info('populating settings locations')
        # TODO: Make directory if not exists

        if self.enable_system_paths:
            self._load_filepath(
                '/etc/' + self.application + '/' + self.filename
            )
            self._load_filepath(
                '/etc/'
                + self.application
                + '/'
                + self.application
                + '.'
                + self.filetype
            )

        if self.enable_user_paths:
            self._load_filepath(
                os.path.expanduser('~')
                + '/.'
                + self.application
                + '.'
                + self.filetype
            )
            self._load_filepath(
                os.path.expanduser('~')
                + '/.'
                + self.application
                + '.d/'
                + self.filename
            )

        if self.enable_local_paths:
            self._load_filepath(os.getcwd() + '/' + self.filename)
            self._load_filepath(
                os.getcwd() + '/' + self.application + '.' + self.filetype
            )

    def load_nested_configs(self, path: Optional[str] = None):
        '''Load configurations located in nested directory path.'''
        for filepath in glob.iglob('/**/' + self.filename, recursive=True):
            self._load_filepath(filepath)

    def load_config_filepath(self, filepath: str):
        '''Load configuration in filepath.'''
        self._load_filepath(filepath)

    def load_configs(self, path: Optional[str] = None):
        '''Choose configuration filepath topology.'''
        if path:
            self.load_config_filepath(path)
        elif self.load_strategy == 'nested':
            self.load_nested_configs(path)
        elif self.load_strategy == 'hierarchy':
            self.load_config_filepaths()


# class NestedConfigPaths(ConfigPaths):
#     pass
#
#     def load_configs(self, path: Optional[str] = None):
#         for filepath in glob.iglob('/**/' + self.filename, recursive=True):
#             self._load_filepath(filepath)


# class HiararchyConfigPaths(ConfigPaths):
#     pass
