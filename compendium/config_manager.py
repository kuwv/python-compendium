# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide settings modules.'''

import glob
import logging
import os
from typing import Any, Callable, List, Optional

from anytree import NodeMixin, Resolver  # type: ignore
from mypy_extensions import KwArg, VarArg

from compendium.filepaths import ConfigPaths
from compendium.loader import ConfigFile
from compendium.settings import EnvironsMixin, SettingsMap

log = logging.getLogger(__name__)


class ConfigManager(EnvironsMixin):
    def __init__(self, name: str, *args: str, **kwargs: Any) -> None:
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
        self.name = name
        # TODO: args should be filepaths
        self._filepaths: List[str] = list(args)
        # self.config_files: List[Dict[str, Union[str, ConfigFile]]] = []

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
        # print('- data', self.data)

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

    def load_config(
        self, filepath: str, update: bool = True, *args: str
    ) -> Optional[ConfigFile]:
        '''Load settings from configuration.'''
        if os.path.exists(filepath):
            config_file = ConfigFile(filepath=filepath)
            config_file.load()
            if update:
                self.data.push(config_file)
            return config_file
        return None

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
        super().__init__(name, *args, **kwargs)
        self._prep_filepaths()
        # self.children: List[Dict[str, Union[str, ConfigFile]]] = []

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
        self.parent = kwargs.pop('parent', None)
        if 'children' in kwargs:
            self.children = kwargs.pop('children')
        load_root = kwargs.pop('load_root', False)
        load_children = kwargs.pop('load_children', False)

        self.filename = kwargs.pop('filename', 'config.toml')
        self.basedir = kwargs.pop('basedir', os.getcwd())

        super().__init__(name, *args, **kwargs)

        if args == ():
            self._prep_filepaths()
        else:
            self._filepaths == list(args)

        if load_root:
            super().load_config(self.filepaths[0])
        if load_children:
            self.load_configs()

    @property
    def namepaths(self) -> List[str]:
        return [self.get_namepath(x) for x in self.filepaths]

    # def __iter__(self) -> 'TreeConfigManager':
    #     '''Return hand itself as iterator.'''
    #     self.__count = 0
    #     return self
    #
    # def __next__(self) -> ConfigFile:
    #     '''Get next card instance.'''
    #     if self.__count < len(self._filepaths):
    #         filepath = self._filepaths[self.__count]
    #         name = self.get_name(filepath)
    #         print(
    #             '--- parent_name',
    #             name.rsplit(self.separator, 1)[0],
    #             'child_name',
    #             name
    #         )
    #         # Check if already loaded in data store
    #         parent_file = self.get_config(name.rsplit(self.separator, 1)[0])
    #         config_file = self.get_config(filepath)
    #         print('--- parent', parent_file, 'child', config_file)
    #         # Load the file if not loaded
    #         if config_file is None:
    #             config_file = ConfigFile(filepath=filepath)
    #             config_file.load()
    #         self.__count += 1
    #         return self.new_child(
    #             self.get_name(filepath),
    #             parent=parent_file or self,
    #             data=config_file,
    #         )
    #     else:
    #         raise StopIteration()

    def get_name(self, filepath: str) -> str:
        '''Get name from tree path.'''
        name = os.path.dirname(os.path.relpath(filepath, self.basedir)).split(
            os.sep
        )[-1]
        if name != '':
            return name
        else:
            return self.name

    def get_namepath(self, filepath: str) -> str:
        '''Get name from tree path.'''
        name = os.path.dirname(os.path.relpath(filepath, self.basedir)).replace(
            os.sep, self.separator
        )
        if name != '':
            return f"{self.separator}{self.name}{self.separator}{name}"
        else:
            return f"{self.separator}{self.name}"

    def get_filepath(self, name: str) -> Optional[str]:
        '''Get filepath from namepath.'''
        for x in self.filepaths:
            if name == self.get_namepath(x):
                return x
        return None

    def get_config(self, namepath):
        '''Get config from store by attribute.'''
        r = Resolver('name')
        results = r.get(self, namepath)
        return results

    def new_child(
        self, name: str, *args: str, **kwargs: Any
    ) -> 'TreeConfigManager':
        '''Get child config node.'''
        if 'basedir' not in kwargs:
            kwargs['basedir'] = self.basedir
        if 'filename' not in kwargs:
            kwargs['filename'] = self.filename
        kwargs['parent'] = self
        # (
        #     self.get_config(
        #         self.get_namepath(filepath).rsplit(self.separator, 1)[0]
        #     )
        # )

        data = self.data.maps
        # filepath = (
        #     kwargs.pop('filepath', None)
        #     or self.get_filepath(
        #         f"{self.separator}{self.name}{self.separator}{name}"
        #     )
        # )
        # if filepath is not None:
        #     config_file = self.load_config(filepath)
        #     if config_file is not None:
        #         data = [config_file] + data  # type: ignore
        if 'data' in kwargs and kwargs['data'] not in self.data.maps:
            data = [kwargs.pop('data')] + data
        kwargs['data'] = data
        kwargs['load_children'] = True
        return self.__class__(name, *args, **kwargs)

    def _prep_filepaths(self) -> None:
        '''Load config_files located in nested directory path.'''
        for filepath in glob.iglob(
            os.path.join(self.basedir, '**', self.filename), recursive=True
        ):
            self.add_filepath(filepath)

    def load_config(
        self, filepath: str, update: bool = False, *args: str, **kwargs: Any
    ) -> Optional[ConfigFile]:
        '''Load config.'''
        config_file = super().load_config(filepath, update)
        return self.new_child(
            self.get_name(filepath), data=config_file, *args, **kwargs
        )

    def load_configs(self) -> None:
        '''Load configuration files from filepaths.'''
        for x in self.filepaths[1:]:
            namepath = os.path.dirname(os.path.relpath(x, self.basedir))
            # print('---', self.name, namepath, self.parent)
            if len(namepath.split(os.sep)) == 1:
                child_paths = []
                for c in self.filepaths[1:]:
                    child_path = os.path.dirname(
                        os.path.relpath(c, self.basedir)
                    )
                    # print('child_path', child_path)
                    if namepath != child_path and namepath in child_path:
                        child_paths.append(c)
                children = list(self.children)
                children.append(
                    self.load_config(
                        x,
                        False,
                        *child_paths,
                        basedir=f"{self.basedir}{os.sep}{namepath}",
                    )
                )
                self.children = children
