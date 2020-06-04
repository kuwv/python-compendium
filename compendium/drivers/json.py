# -*- coding: utf-8 -*-
import errno
import json
import sys
from . import ConfigBase
from ..utils import Logger


class JsonConfig(ConfigBase):
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info("Inializing JsonConfig")

    # def __update_key_delimter(self, json, old, new)
    #     content = {
    #         key.replace(old, new): content[key] for key in file.keys()
    #     }

    @property
    def filetypes(self):
        return ['json']

    def load_config(self, filepath):
        self.__log.info("JsonConfig: loading configuration file")
        with open(filepath, "r") as json_file:
            self._configuration = json.load(json_file)
        json_file.close()

    def save_config(self):
        try:
            with open(self.filepath, "w") as json_path:
                json.dump(
                    self._configuration, json_path, indent=2, sort_keys=True
                )
        except IOError as err:
            if err[0] == errno.EPERM:
                print(
                    "Error: You do not have permission to write to this file"
                )
                sys.exit(1)

    def update_config(self, content):
        content.pop("func", None)
        self._configuration.update(content)

    def get_config(self):
        return self._configuration
