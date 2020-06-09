# -*- coding: utf-8 -*-
import errno
import sys
from ruamel.yaml import YAML
from . import ConfigBase, ConfigMixin
from ..utils import Logger


# TODO: Implement ruamel yaml
class YamlConfig(ConfigBase, ConfigMixin):
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info('Inializing YamlConfig')
        self.yaml = YAML(typ = 'safe')

    @staticmethod
    def filetypes():
        return ['yaml', 'yml']

    def load_config(self, filepath):
        self.__log.info(
            "YamlConfig loading configuration file {}".format(filepath)
        )
        with open(filepath, 'r') as yaml_file:
            self._configuration = self.yaml.load(yaml_file)
            self.__log.debug(self._configuration)
        yaml_file.close()

    def save_config(self, filepath):
        try:
            with open(filepath, 'w') as yaml_file:
                self.yaml.dump(
                    self._configuration,
                    yaml_file,
                    default_flow_style=False
                )
            yaml_file.close()
        except IOError as err:
            if err[0] == errno.EPERM:
                self.__log.error(
                    'Error: unable to write to file'
                )
                sys.exit(1)
