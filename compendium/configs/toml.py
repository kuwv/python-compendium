# -*- coding: utf-8 -*-
import errno
import os
import sys
import tomlkit
from . import ConfigBase
from ..utils import Logger


class TomlConfig(ConfigBase):
    # TODO: Add default template
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info("Inializing TomlConfig")

    # def __update_key_delimter(self, toml, old, new)
    #     content = {
    #         key.replace(old, new): content[key] for key in file.keys()
    #     }

    @staticmethod
    def filetypes():
        return ['toml', 'tml']

    def load_config(self, filepath):
        self.__log.info("TomlConfig: loading configuration file")
        if os.path.isfile(filepath):
            with open(filepath, encoding='utf-8') as f:
                self._configuration = tomlkit.loads(f.read())
            f.close()
        else:
            # TODO: Load template if configured
            self._configuration = {}
        return self._configuration

    def save_config(self):
        self.__log.info("TomlConfig: saving configuration file")
        try:
            with open(self.filepath, "w") as f:
                f.write(tomlkit.dumps(self._configuration))
            f.close()
        except IOError as err:
            if err[0] == errno.EPERM:
                print("Error: unable to write to file")
                sys.exit(1)

    def update_config(self, content):
        content.pop("func", None)
        self._configuration.update(content)

    def get_config(self):
        return self._configuration
