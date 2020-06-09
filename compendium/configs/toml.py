# -*- coding: utf-8 -*-
import errno
import os
import sys
import tomlkit
from . import ConfigBase, ConfigMixin
from ..utils import Logger


class TomlConfig(ConfigBase, ConfigMixin):
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
                self._configuration = tomlkit.loads(f.read())
            f.close()
        else:
            # TODO: Load template if configured
            self._configuration = {}
        return self._configuration

    def save_config(self, filepath):
        self.__log.info('TomlConfig: saving configuration file')
        try:
            with open(filepath, 'w') as f:
                f.write(tomlkit.dumps(self._configuration))
            f.close()
        except IOError as err:
            if err[0] == errno.EPERM:
                print('Error: unable to write to file')
                sys.exit(1)
