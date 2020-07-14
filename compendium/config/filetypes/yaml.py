'''Control YAML configuration module.'''
# -*- coding: utf-8 -*-
import errno
import logging
import os

from ruamel.yaml import YAML  # type: ignore

from .. import ConfigBase


# TODO: Implement ruamel yaml
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
            "YamlConfig loading configuration file {}".format(filepath)
        )
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding=self.encoding) as f:
                content = self.yaml.load(f)
        else:
            content = {}
        return content

    def save_config(self, content, filepath):
        '''Save settings to YAML configuration.'''
        try:
            with open(filepath, 'w') as f:
                self.yaml.dump(content, f)
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'Error: You do not have permission to write to this file'
                )
                raise
