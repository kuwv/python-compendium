# -*- coding: utf-8 -*-
import errno
import sys
import yaml
from . import ConfigBase
from ..utils import Logger


# TODO: Implement ruamel yaml
class YamlConfig(ConfigBase):
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info('Inializing YamlConfig')

    @staticmethod
    def filetypes():
        return ['yaml', 'yml']

    def load_config(self, filepath):
        self.__log.info(
            "YamlConfig loading configuration file {}".format(filepath)
        )
        with open(filepath, 'r') as yaml_file:
            self._configuration = yaml.load(yaml_file)
            self.__log.debug(self._configuration)
        yaml_file.close()

    def save_config(self):
        try:
            with open(self.filepath, 'w') as yaml_file:
                yaml.dump(
                    self._configuration,
                    yaml_file,
                    default_flow_style=False
                )
        except IOError as err:
            if err[0] == errno.EPERM:
                self.__log.error(
                    'Error: unable to write to file'
                )
                sys.exit(1)

    def update_config(self, content):
        self._configuration.update(content)

    def get_config(self):
        return self._configuration
