# -*- coding: utf-8 -*-
import glob
import os
from .utils import Logger


class FileTree(object):

    # TODO: Skip all if already loaded unless 'reload' is passed
    def __init__(self, application, **kwargs):
        self.__log = Logger(__name__)

        self.filepaths = []

        if 'path' in kwargs:
            self.filepaths = [kwargs.get('path')]
            path, self.filename = self.filepaths[0].rsplit('/', 1)
        elif 'filename' in kwargs:
            self.filename = kwargs.get('filename')
        else:
            self.filename = 'settings.toml'
        self.filetype = self.filename.split('.')[-1]

        self.application = application
        self.base_path = None

    def __add_filepath(self, path, file):
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

    def _get_posix_system_paths(self):
        self.__add_filepath('/etc/' + self.application, self.filename)
        self.__add_filepath(
            '/etc/' + self.application, self.application + '.' + self.filetype
        )

    def _get_home_paths(self):
        self.__add_filepath(
            os.path.expanduser('~'),
            '.'
            + self.application
            + '.'
            + self.filetype
        )
        self.__add_filepath(
            os.path.expanduser('~')
            + '/.'
            + self.application
            + '.d',
            self.filename
        )

    def _get_local_paths(self):
        self.__add_filepath(os.getcwd(), self.filename)
        self.__add_filepath(
            os.getcwd(),
            self.application + '.' + self.filetype
        )

    # TODO: Implement pathlib
    def _retrieve_posix_filepaths(self):
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

        # TODO: add config conditionals
        self._get_posix_system_paths()
        self._get_home_paths()
        self._get_local_paths()

    def _retrieve_nested_filepaths(self):
        for file in glob.iglob('**/*.toml', recursive=True):
            print(file)

        self.__add_filepath(
            os.getcwd(),
            self.application + '.' + self.filetype
        )

    def load_config_path(self, filepath):
        path, filename = filepath.rsplit('/', 1)
        self.__add_filepath(path, filename)

    def load_config_paths(self, pathtype='posix'):
        if pathtype == 'posix':
            self._retrieve_posix_filepaths()
        elif pathtype == 'nested':
            self._retrieve_nested_filepaths()

    @staticmethod
    def __make_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
