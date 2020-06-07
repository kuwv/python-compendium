# -*- coding: utf-8 -*-
import errno
import json
import jsonschema
import sys
from . import ConfigBase
from ..utils import Logger


class JsonConfig(ConfigBase):
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info('Inializing JsonConfig')

    # def __update_key_delimter(self, json, old, new)
    #     content = {
    #         key.replace(old, new): content[key] for key in file.keys()
    #     }

    @staticmethod
    def filetypes():
        return ['json']

    def load_config(self, filepath):
        self.__log.info('JsonConfig: loading configuration file')
        with open(filepath, 'r') as json_file:
            self._configuration = json.load(json_file)
        json_file.close()

    def save_config(self):
        try:
            with open(self.filepath, 'w') as json_path:
                json.dump(
                    self._configuration, json_path, indent=2, sort_keys=True
                )
        except IOError as err:
            if err[0] == errno.EPERM:
                print(
                    'Error: You do not have permission to write to this file'
                )
                sys.exit(1)

    def update_config(self, content):
        content.pop('func', None)
        self._configuration.update(content)

    def get_config(self):
        return self._configuration

    def validate(self, content):
        try:
            jsonschema.validate(instance=content, schema=self.schema)
        except jsonschema.exceptions.ValidationError as err:
            # TODO handle validation error
            print(err[0])
            return False
        return True
