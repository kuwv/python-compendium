# -*- coding: utf-8 -*-
import glob
import os
from .configs import Configs
from .utils import Logger
from typing import List


class ConfigManager(Configs):

    # TODO: Skip all if already loaded unless 'reload' is passed
    def __init__(self, application, **kwargs):
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
        self.enable_system_paths: str = kwargs.get('enable_system_paths', False)
        self.enable_user_paths: str = kwargs.get('enable_user_paths', False)
        self.enable_local_paths: str = kwargs.get('enable_local_paths', True)

        # TODO: writable / readonly
        self.filepaths: List[str] = []
        self.base_path: str = None

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

    @property
    def head(self):
        return self.filepaths[-1]

    @staticmethod
    def __get_supported_filetypes():
        pass

    def __load_filepath(self, path, file):
        filepath = "{p}/{f}".format(p=path, f=file)

        if self.base_path is not None:
            filepath = self.base_path + filepath

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
            self.__load_filepath('/etc/' + self.application, self.filename)
            self.__load_filepath(
                '/etc/' + self.application,
                self.application + '.' + self.filetype,
            )

        if self.enable_user_paths:
            self.__load_filepath(
                os.path.expanduser('~'),
                '.' + self.application + '.' + self.filetype,
            )
            self.__load_filepath(
                os.path.expanduser('~') + '/.' + self.application + '.d',
                self.filename,
            )

        if self.enable_local_paths:
            self.__load_filepath(os.getcwd(), self.filename)
            self.__load_filepath(
                os.getcwd(), self.application + '.' + self.filetype
            )

    def load_nested_configs(self, path=None):
        for filepath in glob.iglob('**/' + self.filename, recursive=True):
            if '/' in filepath:
                base_path, filename = self.split_filepath(filepath)
            else:
                base_path = '.'
                filename = filepath
            self.__load_filepath(base_path, filename)

    def load_config(self, filepath):
        path, self.filename = self.split_filepath(filepath)
        self.__load_filepath(path, self.filename)

    def load(self, path=None, paths=[]):
        if path:
            paths = [path]

        if self.load_strategy == 'hierarchy':
            self.load_config_filepaths()
        elif self.load_strategy == 'nested':
            self.load_nested_configs(paths[0])
        elif self.load_strategy == 'standalone':
            self.load_config(paths[0])
