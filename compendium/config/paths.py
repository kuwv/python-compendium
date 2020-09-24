# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide configuration filepaths.'''

import logging
from typing import List, Optional, Union

from . import ConfigFile


class ConfigPaths(ConfigFile):
    '''Manage configuration paths.'''

    # TODO: Skip all if already loaded unless 'reload' is passed
    def __init__(self, **kwargs: str):
        '''Initialize configuration path topology.'''
        super().__init__()

        # TODO: writable / readonly
        self._filepaths: List[str] = []
        self.base_path: Optional[str] = None

        if 'path' in kwargs:
            self._filepaths.append(kwargs['path'])
            self.base_path, self.filename = self.split_filepath(
                self._filepaths[0]
            )
            self.filetype = self.get_filetype(self.filename)
        elif 'filename' in kwargs:
            self.filename = kwargs['filename']
            self.filetype = self.get_filetype(self.filename)
        else:
            self.filename = 'settings.toml'
            self.filetype = 'toml'

    @property
    def filepaths(self):
        '''Retrieve filepaths.'''
        return self._filepaths

    @property
    def head(self):
        '''Retrieve head filepath.'''
        return self._filepaths[-1]

    # @property
    # def tail(self):
    #     '''Retrieve beggining filepath.'''
    #     return self._filepaths[0]

    def load_filepath(self, filepath: str):
        '''Load settings from configuration in filepath.'''
        logging.debug("searching for {}".format(filepath))

        if self._check_path(filepath):
            self._filepaths.append(filepath)
