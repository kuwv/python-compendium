# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Control configuration files."""

# from weakref import ref
import logging
import os
from typing import Any, Dict, Optional, Tuple, Type

import pkg_resources  # type: ignore

from compendium import exceptions
from compendium.filetypes import FiletypesBase
from compendium.filetypes.ini import IniConfig  # noqa
from compendium.filetypes.json import JsonConfig  # noqa
from compendium.filetypes.toml import TomlConfig  # noqa
from compendium.filetypes.yaml import YamlConfig  # noqa
from compendium.settings import Settings

# TODO: use importlib instead
if 'xmltodict' in {pkg.key for pkg in pkg_resources.working_set}:
    from compendium.filetypes.xml import XmlConfig  # noqa

log = logging.getLogger(__name__)


class ConfigFile:
    """Manage settings loaded from confiugrations using dpath."""

    # TODO: switch to dependency injection for filetypes
    def __init__(self, filepath: Optional[str] = None, **kwargs: Any) -> None:
        """Initialize single configuration file."""
        self.filepath: Optional[str] = filepath
        self.filename: str = kwargs.pop('filename', 'config.toml')
        self.filetype: str = kwargs.pop(
            'filetype', self.get_filetype(self.filename)
        )

        self.writable: bool = bool(kwargs.pop('writable', False))
        self.autosave: bool = bool(
            kwargs.pop('autosave', True if self.writable else False)
        )
        self.factory: Optional[dict] = kwargs.pop('factory', Settings)
        self.__loader = None

    def __get_class(
        self, filetype: Optional[str] = 'toml'
    ) -> Optional[Type[FiletypesBase]]:
        """Get class object from filetype module."""
        for module in [m for m in FiletypesBase.__subclasses__()]:
            if filetype in module.extensions():
                return module
        return None

    # def loader(self) -> Optional[FiletypesBase]:
    #     if not self.__loader:
    #         Class = self.__get_class(
    #             self.get_filetype(filepath) or self.filetype
    #         )
    #         self.__loader = Class() if Class else None
    #     return self.__loader

    @staticmethod
    def get_filetype(filepath: str) -> Optional[str]:
        """Get filetype from filepath."""
        if '.' in filepath:
            return os.path.splitext(filepath)[1].strip('.')
        else:
            return None

    def load(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Load settings from configuration file."""
        filepath = filepath or self.filepath
        if filepath:
            # Use discovered module to load configuration.
            if os.path.exists(filepath):
                logging.info(f"Retrieving configuration: '{filepath}'")
                Class = self.__get_class(
                    self.get_filetype(filepath) or self.filetype
                )
                if Class:
                    c = Class()
                    # TODO: combine factory and load_config
                    data = c.load_config(filepath=filepath)
                    return self.factory(data) 
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
            filepath = filepath or self.filepath
            if filepath:
                # Use discovered module to save configuration
                logging.info(f"Saving configuration: '{filepath}'")
                Class = self.__get_class(
                    self.get_filetype(filepath) or self.filetype
                )
                if Class:
                    # TODO: refactor to use respective dict from chainmap
                    c = Class()
                    c.dump_config(data, filepath)
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
