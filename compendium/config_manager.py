# -*- coding: utf-8 -*-
import glob
import os
from typing import List, Optional, Union

from .config import ConfigFile
from .utils import Logger


class ConfigPaths(ConfigFile):

    # TODO: Skip all if already loaded unless 'reload' is passed
    def __init__(self, application: str, **kwargs: str):
        '''
        load_strategy:
          - singleton
          - hierarchy
          - nested
        '''
        self.__log = Logger(__name__)
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
        elif 'filename' in kwargs:
            self.filename = kwargs.get('filename')
            self.filetype = self.get_filetype(self.filename)
        else:
            self.filename = 'settings.toml'
            self.filetype = 'toml'

    # @property
    # def tail(self):
    #     return self.filepaths[0]

    @property
    def head(self):
        return self.filepaths[-1]

    def __load_filepath(self, filepath: str):
        self.__log.debug("searching for {f}".format(f=filepath))

        if self._check_path(filepath):
            self.filepaths.append(filepath)

    # TODO: Implement pathlib
    def load_config_filepaths(self):
        '''Load config paths based on priority
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
        self.__log.info('populating settings locations')
        # TODO: Make directory if not exists

        if self.enable_system_paths:
            self.__load_filepath(
                '/etc/' + self.application + '/' + self.filename
            )
            self.__load_filepath(
                '/etc/'
                + self.application
                + '/'
                + self.application
                + '.'
                + self.filetype
            )

        if self.enable_user_paths:
            self.__load_filepath(
                os.path.expanduser('~')
                + '/.'
                + self.application
                + '.'
                + self.filetype
            )
            self.__load_filepath(
                os.path.expanduser('~')
                + '/.'
                + self.application
                + '.d/'
                + self.filename
            )

        if self.enable_local_paths:
            self.__load_filepath(os.getcwd() + '/' + self.filename)
            self.__load_filepath(
                os.getcwd() + '/' + self.application + '.' + self.filetype
            )

    def load_nested_configs(self, path: Optional[str] = None):
        for filepath in glob.iglob('**/' + self.filename, recursive=True):
            self.__load_filepath(filepath)

    def load_config_filepath(self, filepath: str):
        self.__load_filepath(filepath)

    def load_configs(self, path: Optional[str] = None):
        if path:
            self.load_config_filepath(path)
        elif self.load_strategy == 'nested':
            self.load_nested_configs(path)
        elif self.load_strategy == 'hierarchy':
            self.load_config_filepaths()


class ConfigManager(ConfigPaths):
    '''Allow multiple single path settings instances of each config'''

    pass
