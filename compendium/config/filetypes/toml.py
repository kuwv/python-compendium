# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control toml module.'''

import errno
import os
import logging

import tomlkit  # type: ignore

from .. import ConfigBase


class TomlConfig(ConfigBase):
    '''Manage toml configurations.'''

    def __init__(self, **kwargs):
        '''Initialize toml module.'''
        logging.info('Inializing TomlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')

    @staticmethod
    def filetypes():
        '''Return supported filetypes.'''
        return [
            'cfg', 'conf', 'config', 'cnf', 'ini', 'toml', 'tml'
        ]

    def load_config(self, filepath):
        '''Load settings from toml configuration.'''
        logging.info('loading TOML configuration file')
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding=self.encoding) as f:
                content = tomlkit.parse(f.read())
        else:
            content = {}
        return content

    def dump_config(self, content, filepath):
        '''Save settings to toml configuration.'''
        logging.info('TomlConfig: saving configuration file')
        try:
            with open(filepath, 'w') as f:
                f.write(tomlkit.dumps(content))
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise
