# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control configuration files.'''

# from weakref import ref
import logging
import os
import pkg_resources
from collections import UserDict
from typing import Optional, Type

from compendium import exceptions
from compendium.filetypes_base import FiletypesBase
from compendium.filepaths import FilepathMixin
from compendium.filetypes.json import JsonConfig  # noqa
from compendium.filetypes.toml import TomlConfig  # noqa
from compendium.filetypes.yaml import YamlConfig  # noqa
if 'xmltodict' in {pkg.key for pkg in pkg_resources.working_set}:
    from compendium.filetypes.xml import XmlConfig  # noqa
from compendium.query import DpathMixin

log = logging.getLogger(__name__)


class ConfigFile(UserDict, DpathMixin, FilepathMixin):
    '''Manage settings loaded from confiugrations using dpath.'''

    def __init__(self, filepath: str = None, **kwargs):
        '''Initialize single configuration file.'''
        self.filepath: Optional[str] = filepath
        self.filename: str = kwargs.pop('filename', 'config.toml')
        self.filetype: str = kwargs.pop(
            'filetype', self.get_filetype(self.filename)
        )

        self.writable: bool = bool(kwargs.pop('writable', False))
        self.autosave: bool = bool(
            kwargs.pop('autosave', True if self.writable else False)
        )

        if 'separator' in kwargs:
            self.separator: str = kwargs.pop('separator')
        super().__init__(**kwargs)

    @staticmethod
    def modules():
        '''Lookup modules inheriting FiletypesBase.'''
        return [m for m in FiletypesBase.__subclasses__()]

    def __get_class(
        self, filetype: Optional[str] = 'toml'
    ) -> Optional[Type[FiletypesBase]]:
        '''Get class object from filetype module.'''
        for module in self.modules():
            if filetype in module.filetypes():  # type: ignore
                return module
        return None

    def load(self, filepath: Optional[str] = None) -> None:
        '''Load settings from configuration file.'''
        filepath = filepath or self.filepath
        if filepath:
            '''Use discovered module to load configuration.'''
            if os.path.exists(filepath):
                logging.info("Retrieving configuration: '{}'".format(filepath))
                Class = self.__get_class(self.get_filetype(filepath))
                if Class:
                    c = Class()
                    self.update(c.load_config(filepath=filepath))
                else:
                    raise exceptions.CompendiumDriverError(
                        "Error: No class found for: '{}'".format(filepath)
                    )
            else:
                raise exceptions.CompendiumConfigFileError(
                    "Skipping: No configuration found at: '{}'".format(filepath)
                )
        else:
            raise exceptions.CompendiumConfigFileError(
                'Error: no config file provided'
            )

    def dump(
        self, filepath: Optional[str] = None, writable: bool = False,
    ) -> None:
        '''Save settings to configuraiton.'''
        if writable or self.writable:
            filepath = filepath or self.filepath
            if filepath:
                # Use discovered module to save configuration
                logging.info("Saving configuration: '{}'".format(filepath))
                Class = self.__get_class(self.get_filetype(filepath))
                if Class:
                    # TODO: refactor to use respective dict from chainmap
                    c = Class()
                    c.dump_config(self.data, filepath)
                else:
                    raise exceptions.CompendiumDriverError(
                        "Skipping: No class found for: '{}'".format(filepath)
                    )
            else:
                raise exceptions.CompendiumConfigFileError(
                    'Error: no config file provided'
                )
        else:
            raise exceptions.CompendiumConfigFileError(
                'Error: file is not writable'
            )
