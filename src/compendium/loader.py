# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control configuration files."""

# from weakref import ref
import importlib
import logging
import os
from typing import Any, Dict, Optional, Type

from compendium import exceptions
from compendium.filetypes import FiletypesBase
from compendium.filetypes.ini import IniConfig  # noqa
from compendium.filetypes.json import JsonConfig  # noqa
from compendium.filetypes.toml import TomlConfig  # noqa
from compendium.filetypes.yaml import YamlConfig  # noqa
from compendium.settings import Settings

if importlib.util.find_spec('xmltodict'):  # type: ignore
    from compendium.filetypes.xml import XmlConfig  # noqa

log = logging.getLogger(__name__)


class ConfigFile:
    """Manage settings loaded from confiugrations using dpath."""

    # TODO: switch to dependency injection for filetypes
    def __init__(self, filepath: Optional[str] = None, **kwargs: Any) -> None:
        """Initialize single configuration file."""
        self.default_filetype = kwargs.pop('default_filetype', 'toml')
        self.default_filename = kwargs.pop(
            'default_filename', f"config.{self.default_filetype}"
        )
        if filepath:
            self.filepath = filepath
        self.writable = bool(kwargs.pop('writable', False))
        self.autosave = bool(
            kwargs.pop('autosave', True if self.writable else False)
        )
        self.factory: dict = kwargs.pop('factory', Settings)
        self.factory_kwargs: Dict[str, Any] = kwargs.pop('factory_kwargs', {})

    def __repr__(self) -> str:
        """Get filepath."""
        return repr(self.filepath)

    def __str__(self) -> str:
        """Return filepath."""
        return self.filepath

    def __eq__(self, other: Any) -> bool:
        """Check if path is equal to config file path."""
        if type(other) == str:
            return self.filepath == other
        if type(other) == type(self):
            return self == other
        return False

    def __get_class(
        self, filetype: Optional[str] = 'toml'
    ) -> Optional[Type[FiletypesBase]]:
        """Get class object from filetype module."""
        for module in [m for m in FiletypesBase.__subclasses__()]:
            if filetype in module.extensions():
                return module
        return None

    @property
    def filename(self) -> str:
        """Get filename from filepath."""
        filename = os.path.basename(self.filepath)
        return filename if filename != '' else self.default_filename

    @property
    def filetype(self) -> str:
        """Get filetype from filename."""
        if '.' in self.filename and not self.filename.startswith('.'):
            return os.path.splitext(self.filename)[1].strip('.')
        return self.default_filetype

    @property
    def strategy(self) -> Optional[FiletypesBase]:
        """Get loader strategy from filetype."""
        return self._strategy.get(self.filepath)

    @property
    def filepath(self) -> str:
        """Get filepath."""
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: str) -> None:
        """Set filepath."""
        self._filepath = filepath
        if not hasattr(self, '_strategy'):
            self._strategy: Dict[str, FiletypesBase] = {}
        if filepath not in self._strategy.keys():
            Class = self.__get_class(self.filetype)
            if Class:
                self._strategy[filepath] = Class()

    def load(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Load settings from configuration file."""
        self.filepath = filepath or self.filepath
        if self.filepath:
            # Use discovered module to load configuration.
            if os.path.exists(self.filepath):
                logging.info(f"Retrieving configuration: '{filepath}'")
                if self.strategy:
                    # TODO: combine factory and load_config
                    data = self.strategy.load_config(filepath=self.filepath)
                    return self.factory(
                        data, **self.factory_kwargs
                    )  # type: ignore
                else:
                    raise exceptions.DriverError(
                        f"Error: No class found for: '{filepath}'"
                    )
            else:
                raise exceptions.ConfigFileError(
                    f"Skipping: No configuration found at: '{filepath}'"
                )
        else:
            raise exceptions.ConfigFileError('Error: no config file provided')

    def dump(
        self,
        data: Dict[str, Any],
        filepath: Optional[str] = None
    ) -> None:
        """Save settings to configuraiton."""
        if self.writable:
            self.filepath = filepath or self.filepath
            if self.filepath:
                # Use discovered module to save configuration
                logging.info(f"Saving configuration: '{filepath}'")
                if self.strategy:
                    # TODO: refactor to use respective dict from chainmap
                    self.strategy.dump_config(data, self.filepath)
                else:
                    raise exceptions.DriverError(
                        f"Skipping: No class found for: '{filepath}'"
                    )
            else:
                raise exceptions.ConfigFileError(
                    'Error: no config file provided'
                )
        else:
            raise exceptions.ConfigFileError('Error: file is not writable')
