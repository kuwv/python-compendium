# -*- coding: utf-8 -*-
import glob
import os
from .utils import Logger
from .configs import Configs


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

        self.application = application

        if 'load_strategy' in kwargs:
            self.load_strategy = kwargs.get('load_strategy')
        else:
            self.load_strategy = 'hierarchy'

        # TODO: writable / readonly
        self.filepaths = []
        self.base_path = None

        if 'enable_system_paths' in kwargs:
            self.enable_system_paths = kwargs.get('enable_system_paths')
        else:
            self.enable_system_paths = True

        if 'enable_local_paths' in kwargs:
            self.enable_local_paths = kwargs.get('enable_local_paths')
        else:
            self.enable_local_paths = True

        if 'path' in kwargs:
            self.filepaths = [kwargs.get('path')]
            # self.load_strategy = 'singleton'
            path, self.filename = self.split_filepath(self.filepaths[0])
            # self.load_config_path(kwargs.get('path'))
        elif 'filename' in kwargs:
            self.filename = kwargs.get('filename')
            self.filetype = self.get_filetype(self.filename)
            self.load_config_paths()
        else:
            self.filename = 'settings.toml'
            self.filetype = self.get_filetype(self.filename)
            self.load_config_paths()

    def __load_filepath(self, path, file):
        filepath = "{p}/{f}".format(p=path, f=file)

        if self.base_path is not None:
            filepath = self.base_path + filepath
        self.__log.debug("searching for {f}".format(f=filepath))

        if os.path.isfile(filepath):
            self.filepaths.append(filepath)
            self.__log.debug("{f} found".format(f=filepath))
        else:
            self.__log.debug("{f} not found".format(f=filepath))

    @staticmethod
    def __get_supported_filetypes():
        pass

    def _load_hierarchy_paths(self):
        self.__load_filepath('/etc/' + self.application, self.filename)
        self.__load_filepath(
            '/etc/' + self.application,
            self.application + '.' + self.filetype
        )

    def _load_user_paths(self):
        self.__load_filepath(
            os.path.expanduser('~'),
            '.' + self.application + '.' + self.filetype,
        )
        self.__load_filepath(
            os.path.expanduser('~') + '/.' + self.application + '.d',
            self.filename,
        )

    def _load_local_paths(self):
        self.__load_filepath(os.getcwd(), self.filename)
        self.__load_filepath(
            os.getcwd(), self.application + '.' + self.filetype
        )

    # TODO: Implement pathlib
    def _load_hierarchy_filepaths(self):
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
            self._load_hierarchy_paths()

        if self.enable_local_paths:
            self._load_user_paths()
            self._load_local_paths()

    def _load_nested_filepaths(self, path=None):
        for file in glob.iglob('**/*.toml', recursive=True):
            print(file)

        self.__load_filepath(
            os.getcwd(), self.application + '.' + self.filetype
        )

    def load_config_path(self, filepath):
        path, self.filename = self.split_filepath(filepath)
        self.__load_filepath(path, self.filename)

    def load_config_paths(self, paths=[], load_strategy='hierarchy'):
        if load_strategy == 'hierarchy':
            self._load_hierarchy_filepaths()
        elif load_strategy == 'nested':
            self._load_nested_filepaths(paths[0])
        elif load_strategy == 'standalone':
            self.load_config_path(paths[0])

    @staticmethod
    def __make_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
