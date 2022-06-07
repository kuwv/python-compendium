# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Provide settings modules."""

import glob
import logging
import os
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple

from anytree import NodeMixin, Resolver

from compendium import exceptions
from compendium.filepaths import ConfigPaths
from compendium.loader import ConfigFile
from compendium.settings import EnvironSettings

if TYPE_CHECKING:
    from collections.abc import MutableMapping
    from mypy_extensions import KwArg, VarArg

__all__: List[str] = [
     'ConfigManager',
     'HierarchyConfigManager',
     'TreeConfigManager',
]

log = logging.getLogger(__name__)


class ConfigManager(EnvironSettings):
    """Provide config management representation."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize single settings management."""
        # Setup logging
        if 'log_level' in kwargs:
            log.setLevel(getattr(logging, kwargs.pop('log_level').upper()))
        if 'log_handler' in kwargs:
            log_handler = kwargs.pop('log_handler')
            log.addHandler(logging.StreamHandler(log_handler))

        # Setup filepaths
        self.name = kwargs.pop('name', 'compendium')
        self._filepaths: List[ConfigFile] = [
            (ConfigFile(f, factory_kwargs=kwargs) if type(f) == str else f)
            for f in kwargs.pop('filepaths', [])
        ]

        # Load defaults
        defaults = kwargs.pop('defaults', {})

        # Populate settings
        # if 'data' in kwargs:
        # if args != ():
        #     # self.data = SettingsMap(*kwargs.pop('data'))
        #     self.data = SettingsMap(*args, **kwargs)
        # elif 'settings' in kwargs:
        #     self.data = kwargs.pop('settings')
        # else:
        #     self.data = SettingsMap(defaults, **kwargs)
        super().__init__(*args, **kwargs)

        # Update defaults
        if defaults != {}:
            self.defaults.update(defaults)

        if kwargs.pop('load_configs', True):
            self.load_configs(**kwargs)

    def __getattr__(
        self, attr: str
    ) -> 'Callable[[VarArg(Any), KwArg(Any)], Any]':
        """Proxy calls to settings store."""
        if hasattr(self.__dict__.get('data'), attr):
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                """Call query for data store."""
                return getattr(self.data, attr)(*args, **kwargs)
            return wrapper
        raise AttributeError(attr)

    @property
    def defaults(self) -> Any:
        """Get configuration defaults."""
        return self.data.maps[-1]

    @property
    def filepaths(self) -> Tuple[ConfigFile, ...]:
        """Retrieve filepaths."""
        return tuple(self._filepaths)

    def add_filepath(self, filepath: str) -> None:
        """Load settings from configuration in filepath."""
        logging.debug(f"searching for {filepath}")
        self._filepaths.append(ConfigFile(filepath))

    # def dump_config(self, config_file: ConfigFile) -> None:
    #     """Dump settings to configuration."""
    #     if os.path.exists(config_file.filepath):
    #         config_file.dump(self.data)
    #         if update:
    #             self.data.push(config_file)

    def load_config(
        self,
        config_file: ConfigFile,
        update: bool = True,
        *args: str,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """Load settings from configuration."""
        if os.path.exists(config_file.filepath):
            # config_file = ConfigFile(filepath=filepath, **kwargs)
            settings = config_file.load()
            if update:
                self.push(settings)
            return settings
        return None

    def load_configs(self, **kwargs: Any) -> None:
        """Load configuration files from filepaths."""
        for filepath in self._filepaths:
            self.load_config(filepath, **kwargs)


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

        # XXX: need to workout config loading
        if load_children:
            kwargs['load_configs'] = False
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
        return tuple([self.get_namepath(x.filepath) for x in self.filepaths])

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
        for config in self.filepaths:
            if name == self.get_namepath(config.filepath):
                return config.filepath
        return None

    def get_config(self, namepath: str) -> Dict[str, Any]:
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
        self,
        config_file: ConfigFile,
        update: bool = False,
        *args: str,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """Load config."""
        # TODO: need to separate chainmap of defaults from namespace config
        settings = super().load_config(config_file, update)
        return self.new_child(
            settings, name=self.get_name(config_file.filepath), *args, **kwargs
        )

    def load_configs(self, **kwargs: Any) -> None:
        """Load configuration files from filepaths."""

        def get_child_paths(namepath: str) -> List[ConfigFile]:
            """Get relative child paths of namepath."""
            child_paths = []
            for config in self.filepaths[1:]:
                child_path = os.path.dirname(
                    os.path.relpath(config.filepath, self.basedir)
                )
                if (
                    len(child_path.split(os.sep)) > 1
                    and child_path.startswith(namepath)
                ):
                    child_paths.append(config)
            return child_paths

        if self.children == ():
            # get children filepaths of parent
            filepaths = self.filepaths if self.parent else self.filepaths[1:]
            for config in filepaths:
                # get child namepath from filepath
                namepath = os.path.dirname(
                    os.path.relpath(config.filepath, self.basedir)
                )
                # print('---', self.name, namepath, self.parent)
                # populate only direct children
                if len(namepath.split(os.sep)) == 1:
                    child_paths = get_child_paths(namepath)
                    children = list(self.children)
                    children.append(
                        self.load_config(
                            config,
                            update=False,
                            filepaths=child_paths,
                            basedir=f"{self.basedir}{os.sep}{namepath}",
                            **kwargs
                        )
                    )
                    self.children = children
        else:
            raise exceptions.ConfigManagerError(
                'children configurations already loaded'
            )
