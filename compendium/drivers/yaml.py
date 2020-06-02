# -*- coding: utf-8 -*-
import sys
import yaml
from lunar.config import ConfigBase
from lunar.utils import Logger


class YamlConf(ConfigBase):
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info("Inializing YamlConf")

    def load_conf(self, filepath):
        self.__log.info("YamlConf loading configuration file {}".format(filepath))
        with open(filepath, "r") as yaml_file:
            self._configuration = yaml.load(yaml_file)
            self.__log.debug(self._configuration)
        yaml_file.close()

    def save_conf(self):
        try:
            with open(self.filepath, "w") as yaml_file:
                yaml.dump(self._configuration, yaml_file, default_flow_style=False)
        except IOError as err:
            if err[0] == errno.EPERM:
                self.__log.error(
                    "Error: You do not have permission to write to this file"
                )
                sys.exit(1)

    def update_conf(self, content):
        self._configuration.update(content)

    def get_conf(self):
        return self._configuration
