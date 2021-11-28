# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide settings modules."""

import glob
import logging
import os
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple

from anytree import NodeMixin, Resolver  # type: ignore

from compendium import exceptions
from compendium.filepaths import ConfigPaths
from compendium.loader import ConfigFile
from compendium.settings import EnvironsMixin, SettingsMap

if TYPE_CHECKING:
    from mypy_extensions import KwArg, VarArg

log = logging.getLogger(__name__)


class ConfigManager(EnvironsMixin):
    """Provide config management representation."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize single settings management.

        merge_sections: []
        merge_strategy:
          - overlay
          - partition
          - last

        """
        # Setup logging
        if 'log_level' in kwargs:
            log.setLevel(getattr(logging, kwargs.pop('log_level').upper()))
        if 'log_handler' in kwargs:
            log_handler = kwargs.pop('log_handler')
            log.addHandler(logging.StreamHandler(log_handler))  # type: ignore

        # Setup filepaths
        self.name = kwargs.pop('name', 'compendium')
        # self._filepaths: List[str] = list(args)
        self._filepaths: List[str] = kwargs.pop('filepaths', [])

        # TODO: determine if multiple config files
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

        # Load defaults
        defaults = kwargs.pop('defaults', {})

        # Populate settings
        # if 'data' in kwargs:
        if args != ():
            # self.data = SettingsMap(*kwargs.pop('data'))
            self.data = SettingsMap(*args)
            if defaults != {}:
                self.defaults.update(defaults)
        elif 'settings' in kwargs:
            self.data = kwargs.pop('settings')
        else:
            self.data = SettingsMap(defaults)
        # print('- data', self.data)

    def __getattr__(
        self, attr: str
    ) -> 'Callable[[VarArg(Any), KwArg(Any)], Any]':
        """Proxy calls to settings store."""
        if hasattr(self.__dict__.get('data'), attr):

            def wrapper(*args, **kwargs):
                """Call query for data store."""
                return getattr(self.data, attr)(*args, **kwargs)

            return wrapper
        raise AttributeError(attr)

    def __repr__(self) -> str:
        """Get string representation of data."""
        return repr(self.data)

    @property
    def defaults(self):  # type: ignore
        """Get configuration defaults."""
        return self.data.maps[0]

    @property
    def settings(self) -> SettingsMap:
        """Create settings to prototype idea."""
        # TODO: maybe returing maps would be better
        if self.environs != {}:
            return SettingsMap(self.environs, *self.data.maps)
        else:
            return self.data

    @property
    def filepaths(self) -> Tuple[str, ...]:
        """Retrieve filepaths."""
        # TODO: should this be removed
        return tuple(self._filepaths)

    def add_filepath(self, filepath: str) -> None:
        """Load settings from configuration in filepath."""
        logging.debug("searching for {}".format(filepath))
        self._filepaths.append(filepath)

    # def dump_config(self, filepath: str, *args: str) -> None:
    #     """Dump settings to configuration."""
    #     if os.path.exists(filepath):
    #         config_file = ConfigFile(filepath=filepath)
    #         config_file.dump()
    #         if update:
    #             self.data.push(config_file)

    def load_config(
        self, filepath: str, update: bool = True
    ) -> Optional[ConfigFile]:
        """Load settings from configuration."""
        if os.path.exists(filepath):
            config_file = ConfigFile(filepath=filepath)
            config_file.load()
            if update:
                self.data.push(config_file)  # type: ignore
            return config_file
        return None

    def load_configs(self) -> None:
        """Load configuration files from filepaths."""
        for filepath in self._filepaths:
            self.load_config(filepath)


# TODO: refactor to consume multiple configfile objects
# TODO: refactor for lazyloading
class HierarchyConfigManager(ConfigManager):
    """Manage settings from hierarchy config_files."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize settings from hirarchy filepaths.

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

        """
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
        self._prep_filepaths()

    def _prep_filepaths(self) -> None:
        """Load config_files located in nested directory path."""
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
    """Manage settings from nested tree config_files."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize nested settings management."""
        self.parent = kwargs.pop('parent', None)
        if 'children' in kwargs:
            self.children = kwargs.pop('children')
        load_root = kwargs.pop('load_root', False)
        load_children = kwargs.pop('load_children', False)

        self.filename = kwargs.pop('filename', 'config.toml')
        self.basedir = kwargs.pop('basedir', os.getcwd())

        super().__init__(*args, **kwargs)

        if not self.parent and 'filepaths' not in kwargs:
            self._prep_filepaths()

        if load_root:
            super().load_config(self.filepaths[0])
        if load_children:
            self.load_configs()

    @property
    def namepaths(self) -> Tuple[str, ...]:
        """Return list of namepaths."""
        return tuple([self.get_namepath(x) for x in self.filepaths])

    def get_name(self, filepath: str) -> str:
        """Get name from tree path."""
        name = os.path.dirname(os.path.relpath(filepath, self.basedir),).split(
            os.sep
        )[-1]
        if name != '':
            return name
        else:
            return self.name

    def get_namepath(self, filepath: str) -> str:
        """Get name from tree path."""
        name = os.path.dirname(
            os.path.relpath(filepath, self.basedir),
        ).replace(os.sep, self.separator)
        if name != '':
            return f"{self.separator}{self.name}{self.separator}{name}"
        else:
            return f"{self.separator}{self.name}"

    def get_filepath(self, name: str) -> Optional[str]:
        """Get filepath from namepath."""
        for x in self.filepaths:
            if name == self.get_namepath(x):
                return x
        return None

    def get_config(self, namepath):
        """Get config from store by attribute."""
        r = Resolver('name')
        results = r.get(self, namepath)
        return results

    def new_child(self, *args: Any, **kwargs: Any) -> 'TreeConfigManager':
        """Get child config node."""
        if 'name' not in kwargs:
            kwargs['name'] = self.name
        if 'basedir' not in kwargs:
            kwargs['basedir'] = self.basedir
        if 'filename' not in kwargs:
            kwargs['filename'] = self.filename
        kwargs['parent'] = self
        kwargs['load_children'] = kwargs.get('load_children', True)
        data = (*args, self.data)
        return self.__class__(*data, **kwargs)

    def _prep_filepaths(self) -> None:
        """Load config_files located in nested directory path."""
        for filepath in glob.iglob(
            os.path.join(self.basedir, '**', self.filename), recursive=True
        ):
            if filepath not in self.filepaths:
                self.add_filepath(filepath)

    def load_config(
        self, filepath: str, update: bool = False, *args: str, **kwargs: Any
    ) -> Optional[ConfigFile]:
        """Load config."""
        # TODO: need to separate chainmap of defaults from namespace config
        config_file = super().load_config(filepath, update)
        return self.new_child(
            config_file, name=self.get_name(filepath), *args, **kwargs
        )

    def load_configs(self) -> None:
        """Load configuration files from filepaths."""

        def get_child_paths(namepath: str):
            """Get relative child paths of namepath."""
            child_paths = []
            for path in self.filepaths[1:]:
                child_path = os.path.dirname(
                    os.path.relpath(path, self.basedir)
                )
                if len(child_path.split(os.sep)) > 1 and child_path.startswith(
                    namepath
                ):
                    child_paths.append(path)
            return child_paths

        if self.children == ():
            # get children filepaths of parent
            filepaths = self.filepaths if self.parent else self.filepaths[1:]
            for x in filepaths:
                # get child namepath from filepath
                namepath = os.path.dirname(os.path.relpath(x, self.basedir))
                # print('---', self.name, namepath, self.parent)
                # populate only direct children
                if len(namepath.split(os.sep)) == 1:
                    child_paths = get_child_paths(namepath)
                    children = list(self.children)
                    children.append(
                        self.load_config(
                            x,
                            update=False,
                            filepaths=child_paths,
                            basedir=f"{self.basedir}{os.sep}{namepath}",
                        )
                    )
                    self.children = children
        else:
            raise exceptions.CompendiumConfigManagerError(
                'children configurations already loaded'
            )
