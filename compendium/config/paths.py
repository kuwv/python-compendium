# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide configuration filepaths.'''

import logging
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
        self._filepaths: List[str] = []
        self.base_path: Optional[str] = None

        if 'path' in kwargs:
            self.load_strategy = 'singleton'
            self._filepaths.append(kwargs['path'])
            self.base_path, self.filename = self.split_filepath(
                self._filepaths[0]
            )
            self.filetype = self.get_filetype(self.filename)
        elif 'filename' in kwargs:
            self.filename = kwargs['filename']
            self.filetype = self.get_filetype(self.filename)
        else:
            self.filename = 'settings.toml'
            self.filetype = 'toml'

    @property
    def filepaths(self):
        '''Retrieve filepaths.'''
        return self._filepaths

    @property
    def head(self):
        '''Retrieve head filepath.'''
        return self._filepaths[-1]

    # @property
    # def tail(self):
    #     '''Retrieve beggining filepath.'''
    #     return self._filepaths[0]

    def load_filepath(self, filepath: str):
        '''Load settings from configuration in filepath.'''
        logging.debug("searching for {}".format(filepath))

        if self._check_path(filepath):
            self._filepaths.append(filepath)

    # def load_filepath(self, filepath: str):
    #     '''Load configuration in filepath.'''
    #     self._load_filepath(filepath)
