# -*- coding: utf-8 -*-
import errno
import os
import logging

import tomlkit  # type: ignore

from .. import ConfigBase


class TomlConfig(ConfigBase):
    def __init__(self, **kwargs):
        logging.info('Inializing TomlConfig')
        self.encoding = kwargs.get('encoding', 'utf-8')

    @staticmethod
    def filetypes():
        return [
            'cfg', 'conf', 'config', 'cnf', 'ini', 'toml', 'tml'
        ]

    def load_config(self, filepath):
        logging.info('TomlConfig: loading configuration file')
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding=self.encoding) as f:
                content = tomlkit.parse(f.read())
        else:
            content = {}
        return content

    def save_config(self, content, filepath):
        logging.info('TomlConfig: saving configuration file')
        try:
            with open(filepath, 'w') as f:
                f.write(tomlkit.dumps(content))
        except IOError as err:
            if err.errno == errno.EACCES:
                logging.error(
                    'Error: You do not have permission to write to this file'
                )
                raise
