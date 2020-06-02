# -*- coding: utf-8 -*-
import json
import sys
from lunar.config import ConfigBase
from lunar.utils import Logger


class JsonConf(ConfigBase):
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info("Inializing JsonConf")

    # def __update_key_delimter(self, json, old, new)
    #     content = { key.replace(old, new): content[key] for key in file.keys() }

    def load_conf(self, filepath):
        self.__log.info("JsonConf: loading configuration file")
        with open(filepath, "r") as json_file:
            self._configuration = json.load(json_file)
        json_file.close()

    def save_conf(self):
        try:
            with open(self.filepath, "w") as json_path:
                json.dump(self._configuration, json_path, indent=2, sort_keys=True)
        except IOError as err:
            if err[0] == errno.EPERM:
                print("Error: You do not have permission to write to this file")
                sys.exit(1)

    def update_conf(self, content):
        content.pop("func", None)
        self._configuration.update(content)

    def get_conf(self):
        return self._configuration
