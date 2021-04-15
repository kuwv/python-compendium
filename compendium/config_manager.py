# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

import glob
import logging
import os
from typing import Any, Callable, Dict, List, Union
from mypy_extensions import KwArg, VarArg

from anytree import NodeMixin  # type: ignore

from compendium.loader import ConfigFile
from compendium.filepaths import ConfigPaths
# from compendium.query import DpathMixin
from compendium.settings import EnvironsMixin, SettingsMap

log = logging.getLogger(__name__)


class ConfigManager(EnvironsMixin):
    def __init__(self, *args: str, **kwargs: Any) -> None:
        '''Initialize single settings management.

        merge_sections: []
        merge_strategy:
          - overlay
          - partition
          - last

        '''
        # Setup logging
        if 'log_level' in kwargs:
            log.setLevel(getattr(logging, kwargs.pop('log_level').upper()))
        if 'log_handler' in kwargs:
            log_handler = kwargs.pop('log_handler')
            log.addHandler(logging.StreamHandler(log_handler))  # type: ignore

        # Setup filepaths
        # TODO: args should be filepaths
        self._filepaths: List[str] = list(args)
        self.config_files: List[Dict[str, Union[str, ConfigFile]]] = []

        # Load environs
        if 'prefix' in kwargs:
            self.prefix = kwargs.pop('prefix')
        if 'separator' in kwargs:
            self.separator = kwargs.pop('separator')
        if kwargs.pop('load_dotenv', False):
            self.load_dotenv()
        if kwargs.pop('load_environs', True):
            self.environs = self.load_environs()
        # if kwargs.pop('load_startup_args', True):
        #     self.environs.update(kwargs.pop('load_startup_args', {}))

        # Load defaults
        defaults = kwargs.pop('defaults', {})

        # Populate settings
        if 'data' in kwargs:
            self.data = SettingsMap(*kwargs.pop('data'))
            if defaults != {}:
                self.defaults.update(defaults)
        else:
            self.data = SettingsMap(defaults)

    def __getattr__(
        self, attr: str
    ) -> Callable[[VarArg(Any), KwArg(Any)], Any]:
        '''Proxy calls to settings store.'''
        if hasattr(self.__dict__.get('data'), attr):
            def wrapper(*args, **kwargs):
                return getattr(self.data, attr)(*args, **kwargs)
            return wrapper
        raise AttributeError(attr)

    def __repr__(self) -> str:
        '''Get string representation of data.'''
        return repr(self.data)

    @property
    def defaults(self):  # type: ignore
        '''Get configuration defaults.'''
        return self.data.maps[0]

    @property
    def settings(self) -> SettingsMap:
        '''Create settings to prototype idea.'''
        # TODO: maybe returing maps would be better
        if self.environs != {}:
            return SettingsMap(self.environs, *self.data.maps)
        else:
            return self.data

    @property
    def filepaths(self) -> List[str]:  # remove
        '''Retrieve filepaths.'''
        return self._filepaths

    def add_filepath(self, filepath: str) -> None:
        '''Load settings from configuration in filepath.'''
        logging.debug("searching for {}".format(filepath))
        self._filepaths.append(filepath)

    def load_config(self, filepath: str) -> None:
        '''Load settings from nested configuration.'''
        if os.path.exists(filepath):
            config_file = ConfigFile(filepath=filepath)
            config_file.load()
            self.data.push(config_file)

    def load_configs(self) -> None:
        '''Load configuration files from filepaths.'''
        for filepath in self._filepaths:
            self.load_config(filepath)


# TODO: refactor to consume multiple configfile objects
# TODO: refactor for lazyloading
class HierarchyConfigManager(ConfigManager):
    '''Manage settings from hierarchy config_files.'''

    def __init__(self, name: str, *args: str, **kwargs: Any) -> None:
        '''Initialize settings from hirarchy filepaths.

        Parameters
        ----------
        name: str
            Name of name.
        merge_sections: list, optional
            Include sections to be merged
        merge_strategy: list, optional
            Strategy to used when merging: overlay, parition, and last
              - overlay will replace exsisting entries
              - partition will keeps each seettings separate
              - last will only use the last loaded
        enable_system_filepaths: bool, optional
            Enable system filepath lookup for config_files.
        enable_global_filepaths: bool, optional
            Enable user filepath lookup for config_files.
        enable_local_filepaths: bool, optional
            Enable local filepath lookup for config_files.

        '''
        self.basedir = kwargs.pop('basedir', os.sep)
        self.filename = kwargs.pop('filename', 'config.toml')
        self.enable_system_filepaths = bool(
            kwargs.get('enable_system_filepaths', False)
        )
        self.enable_global_filepaths = bool(
            kwargs.get('enable_global_filepaths', False)
        )
        self.enable_local_filepaths = bool(
            kwargs.get('enable_local_filepaths', True)
        )
        super().__init__(*args, **kwargs)
        self.name = name
        self._prep_filepaths()

    def _prep_filepaths(self) -> None:
        '''Load config_files located in nested directory path.'''
        config_filepaths = ConfigPaths(
            name=self.name,
            filename=self.filename,
            basedir=self.basedir,
            enable_system_filepaths=self.enable_system_filepaths,
            enable_global_filepaths=self.enable_global_filepaths,
            enable_local_filepaths=self.enable_local_filepaths,
        )
        for filepath in config_filepaths.filepaths:
            self.add_filepath(filepath)


# TODO: refactor to consume multiple configfile objects
class TreeConfigManager(ConfigManager, NodeMixin):
    '''Manage settings from nested tree config_files.'''

    def __init__(self, name: str, *args: str, **kwargs: Any) -> None:
        '''Initialize nested settings management.'''
        self.basedir = kwargs.pop('basedir', os.getcwd())
        self.filename = kwargs.pop('filename', 'config.toml')

        self.parent = kwargs.pop('parent', None)
        if 'children' in kwargs:
            self.children = kwargs.pop('children')

        load_root = kwargs.pop('load_root', False)
        load_all = kwargs.pop('load_all', False)

        super().__init__(*args, **kwargs)
        self.name = name

        self._prep_filepaths()
        if load_root:
            self.load_config(self.filepaths[0])
        if load_all:
            self.load_configs()

    def __iter__(self) -> 'TreeConfigManager':
        '''Return hand itself as iterator.'''
        self.__count = 0
        return self

    def __next__(self) -> ConfigFile:
        '''Get next card instance.'''
        print('maps', self.data == {})
        if self.__count < len(self._filepaths):
            filepath = self._filepaths[self.__count]
            if os.path.exists(filepath):
                config_file = ConfigFile(filepath=filepath)
                config_file.load()
                if config_file.filepath:
                    print(self.get_name(config_file.filepath))
                    print('filepath', config_file.filepath)
            else:
                config_file = ConfigFile(filepath)
            self.__count += 1
            return self.new_child(
                self.get_name(filepath),
                data=config_file,
            )
        else:
            raise StopIteration()

    def new_child(
        self,
        name: str,
        *args: str,
        **kwargs: Any
    ) -> 'TreeConfigManager':
        '''Create config file tree node.'''
        # TODO: get relative filepaths as *args
        if 'data' in kwargs and kwargs['data'] not in self.data.maps:
            new_data = kwargs.pop('data')
            data = [new_data] + self.data.maps
        else:
            data = self.data.maps
        kwargs['data'] = data
        return self.__class__(name, *args, parent=self, **kwargs)

    def get_name(self, filepath: str) -> str:
        '''Get name from tree path.'''
        return os.path.dirname(
            os.path.relpath(filepath, self.basedir)
        ).replace(os.sep, self.separator)

    # @property
    # def settings(self) -> SettingsMap:
    #     '''Create settings to prototype idea.'''
    #     settings = SettingsMap()
    #     for cfg in self.config_files:
    #         # TODO: if config_file has name else
    #         name = self.get_name(cfg['filepath'])
    #         if name == '':
    #             # TODO: should create list for child configs
    #             settings.push(cfg['config_file'])
    #         else:
    #             # TODO: should append to list
    #             settings.create(name, cfg['config_file'])
    #     return settings

    def _prep_filepaths(self) -> None:
        '''Load config_files located in nested directory path.'''
        for filepath in glob.iglob(
            os.path.join(self.basedir, '**', self.filename), recursive=True
        ):
            self.add_filepath(filepath)
