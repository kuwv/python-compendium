# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Control YAML configuration module.'''

import errno
import logging
import os

from ruamel.yaml import YAML  # type: ignore

from .. import ConfigBase


class YamlConfig(ConfigBase):
    '''Manage YAML configuration files.'''

    def __init__(self, **kwargs):
        '''Initialize YAML configuration module.'''
        logging.info('Inializing YamlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.yaml = YAML(typ='safe')

    @staticmethod
    def filetypes():
        '''Return support YAML filetypes.'''
        return ['yaml', 'yml']

    def load_config(self, filepath):
        '''Load settings from YAML configuration.'''
        logging.info(
            "loading YAML configuration file {}".format(filepath)
        )
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding=self.encoding) as f:
                content = self.yaml.load(f)
        else:
            content = {}
        return content

    def dump_config(self, content, filepath):
        '''Save settings to YAML configuration.'''
        try:
            with open(filepath, 'w') as f:
                self.yaml.dump(content, f)
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'You do not have permission to write to this file'
                )
                raise
