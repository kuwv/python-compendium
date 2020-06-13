# -*- coding: utf-8 -*-
import errno
import os
import tomlkit  # type: ignore
from . import ConfigBase
from ..utils import Logger


class TomlConfig(ConfigBase):
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info('Inializing TomlConfig')

    @staticmethod
    def filetypes():
        return [
            'cfg', 'cnf', 'conf', 'config', 'ini', 'toml', 'tml'
        ]

    def load_config(self, filepath):
        self.__log.info('TomlConfig: loading configuration file')
        if os.path.isfile(filepath):
            with open(filepath, encoding='utf-8') as f:
                content = tomlkit.loads(f.read())
        else:
            content = {}
        return content

    def save_config(self, content, filepath):
        self.__log.info('TomlConfig: saving configuration file')
        try:
            with open(filepath, 'w') as f:
                f.write(tomlkit.dumps(content))
        except IOError as err:
            if err.errno == errno.EACCES:
                self.__log.error(
                    'Error: You do not have permission to write to this file'
                )
                raise
