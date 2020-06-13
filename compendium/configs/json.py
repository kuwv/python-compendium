# -*- coding: utf-8 -*-
# import datetime
import errno
import json  # type: ignore
# import jsonschema  # type: ignore
import os
from . import ConfigBase
from ..utils import Logger


class JsonConfig(ConfigBase):
    def __init__(self):
        self.__log = Logger(__name__)
        self.__log.info('Inializing JsonConfig')
        self.encoder = str

    @staticmethod
    def filetypes():
        return ['json']

    def load_config(self, filepath):
        self.__log.info('JsonConfig: loading configuration file')
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                content = json.load(f)
            f.close()
        else:
            content = {}
        return content

    def save_config(self, content, filepath):
        try:
            with open(filepath, 'w') as f:
                json.dump(
                    content, f, indent=2, sort_keys=True, default=self.encoder
                )
            f.close()
        except IOError as err:
            if err.errno == errno.EACCES:
                self.__log.error(
                    'Error: You do not have permission to write to this file'
                )
                raise

    # def validate(self, content):
    #     try:
    #         jsonschema.validate(instance=content, schema=self.schema)
    #     except jsonschema.exceptions.ValidationError as err:
    #         # TODO handle validation error
    #         print(err[0])
    #         return False
    #     return True
