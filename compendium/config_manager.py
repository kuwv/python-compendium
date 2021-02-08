# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

import glob
import logging
import os
import platform
from typing import Any, Dict, List, Optional, Set, Union

from .config import ConfigFile
from .settings import Settings

log = logging.getLogger(__name__)


class ConfigManager(ConfigFile):
    '''Manage settings from cache.'''

    def __init__(self, application: str, **kwargs):
        '''Initialize single settings management.

        merge_sections: []
        merge_strategy:
          - overlay
          - partition
          - last

        '''
        if 'log_level' in kwargs:
            log.setLevel(getattr(logging, kwargs.pop('log_level').upper()))
        if 'log_handler' in kwargs:
            log_handler = kwargs.pop('log_handler')
            log.addHandler(logging.StreamHandler(log_handler))  # type: ignore

        self._filepaths: List[str] = []
        self.filename = kwargs.get('filename', 'settings.toml')
        self.filetype = kwargs.get('filetype', self.get_filetype(self.filename))

        ConfigFile.__init__(self, self.filetype, **kwargs)
        self.settings = Settings(application, **kwargs)

        self.merge_strategy: Optional[str] = kwargs.get('merge_strategy', None)
        self.merge_sections: Set[str] = kwargs.get('merge_sections', set())

        self.writable: Optional[bool] = kwargs.get('writable', False)

    # def __getattr__(self, k: str) -> Optional[str]:
    #     if hasattr(self.settings, k):
    #         print('It does')
    #     try:
    #         return self.settings.get(k)
    #     except Exception as err:
    #         print(err)
    #         return None

    # def __setattr__(self, k: str, v: Any) -> None:
    #     self.__settings[k] = v

    @property
    def application(self) -> str:
        return self.settings.application

    @property
    def defaults(self) -> Dict[Any, Any]:
        return self.settings.defaults

    @property
    def head(self) -> str:
        '''Retrieve head filepath.'''
        return self._filepaths[-1] if self._filepaths != [] else ''

    # @property
    # def tail(self) -> str:
    #     '''Retrieve beggining filepath.'''
    #     return self._filepaths[0] if self._filepaths != [] else ''

    @property
    def filepaths(self) -> List[str]:
        '''Retrieve filepaths.'''
        return self._filepaths

    @staticmethod
    def split_filepath(filepath: str) -> List[str]:
        '''Separate filename from filepath.'''
        return filepath.rsplit('/', 1)

    @staticmethod
    def get_filename(filepath: str) -> str:
        '''Get the name of the file.'''
        return filepath.rsplit('/', 1)[1]

    @staticmethod
    def get_filetype(filename: str) -> str:
        '''Get filetype from filename.'''
        return filename.split('.')[-1]

    def _initialize_settings(self, settings: Dict[Any, Any]) -> None:
        self.settings._initialize_settings(settings)
        print('initial settings', self.settings.__dict__)

    def _check_filepath(self, filepath: str) -> bool:
        '''Check if configuraion exists at path.'''
        if os.path.isfile(filepath):
            logging.debug("{} found".format(filepath))
            return True
        else:
            logging.debug("{} not found".format(filepath))
            return False

    def load_filepath(self, filepath: str) -> None:
        '''Load settings from configuration in filepath.'''
        logging.debug("searching for {}".format(filepath))
        print('troubleshooting:', filepath)

        if self._check_filepath(filepath):
            self._filepaths.append(filepath)

    def __get_filepaths(self, filepath: str) -> None:
        self._filepaths.append(filepath)
        self.basepath, self.filename = self.split_filepath(filepath)
        if '.' in self.filename:
            self.filetype = self.get_filetype(self.filename)

    def load(self, filepath: str, filetype: Optional[str] = None) -> None:
        '''Load settings from configuration file.'''
        self.__get_filepaths(filepath=filepath)
        self._initialize_settings(self.load_config(self.head, filetype))

    def dump(self, filepath: str, filetype: Optional[str] = None) -> None:
        '''Save settings to configuraiton.'''
        self.dump_config(self.head, filetype, self.settings)

    def _set_env(self):
        '''Load environs from .env file.'''
        env_file = os.path.join(os.getcwd(), '.env')
        if self._check_filepath(env_file):
            with open(env_file) as env:
                for line in env:
                    k, v = line.partition("=")[::2]
                    os.environ[k.strip().upper()] = str(v)


class NestedConfigManager(ConfigManager):
    '''Manage settings from nested configurations.'''

    def __init__(self, application: str, **kwargs):
        '''Initialize nested settings management.'''
        super().__init__(application, **kwargs)

    def __get_filepaths(self, basepath: Optional[str] = None):
        '''Load configurations located in nested directory path.'''
        print('attempting', self.filename)
        for filepath in glob.iglob(
            "/**/{f}".format(f=self.filename), recursive=True
        ):
            print('attempting', self.filename)
            self.load_filepath(filepath)

    def load_configs(
        self, filepath: Optional[str] = None, filetype: Optional[str] = None
    ):
        '''Load settings from nested configuration.'''
        self.__get_filepaths()
        settings = []
        for filepath in self._filepaths:
            settings.append(
                {'filepath': filepath, **self.load_config(filepath)}
            )
        self._initialize_settings({'settings': settings})


class HierarchyConfigManager(ConfigManager):
    '''Manage settings from hierarchy configurations.'''

    def __init__(self, application: str, **kwargs):
        '''Initialize settings from hirarchy filepaths.

        Parameters
        ----------
        merge_sections: list, optional
            Include sections to be merged
        merge_strategy: list, optional
            Strategy to used when merging: overlay, parition, and last
              - overlay will replace exsisting entries
              - partition will keeps each seettings separate
              - last will only use the last loaded
        enable_system_filepaths: bool, optional
            Enable system filepath lookup for configurations.
        enable_user_filepaths: bool, optional
            Enable user filepath lookup for configurations.
        enable_local_filepaths: bool, optional
            Enable local filepath lookup for configurations.

        '''
        super().__init__(application, **kwargs)

        self.merge_strategy: Optional[str] = kwargs.get('merge_strategy', None)
        self.merge_sections: Set[str] = kwargs.get('merge_sections', set())

        self.enable_system_filepaths: Union[str, bool] = kwargs.get(
            'enable_system_filepaths', False
        )
        self.enable_user_filepaths: Union[str, bool] = kwargs.get(
            'enable_user_filepaths', False
        )
        self.enable_local_filepaths: Union[str, bool] = kwargs.get(
            'enable_local_filepaths', True
        )

    # TODO: Implement pathlib
    def __get_filepaths(self):
        r'''Load config paths based on priority.

        First(lowest) to last(highest):
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

        if self.enable_system_filepaths and os.name == 'posix':
            self.load_filepath(
                os.path.join(os.sep, 'etc', self.application, self.filename)
            )
        # TODO: Add windows/linux compliant service path config option

        if self.enable_user_filepaths:
            if platform.system() == 'Windows':
                __user_app_filepath = os.path.join('AppData', 'Local')

            if platform.system() == 'Darwin':
                __user_app_filepath = os.path.join(
                    'Library', 'Application Support'
                )

            if platform.system() == 'Linux':
                __user_app_filepath = '.config'

            self.load_filepath(
                os.path.join(
                    os.path.expanduser('~'),
                    __user_app_filepath,
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

        if self.enable_local_filepaths:
            self.load_filepath(os.path.join(os.getcwd(), self.filename))
            self.load_filepath(
                os.path.join(
                    os.getcwd(),
                    "{a}.{f}".format(a=self.application, f=self.filetype),
                )
            )

    def load_configs(self):
        '''Load settings from hierarchy filepaths.'''
        self.__get_filepaths()
        settings: Dict[Any, Any] = {}
        for filepath in self._filepaths:
            self.settings.merge(self.load_config(filepath))
        self._initialize_settings(settings)
