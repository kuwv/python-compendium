# -*- coding: utf-8 -*-
import os
import sys
from collections import defaultdict
from configparser import ConfigParser, ExtendedInterpolation
from . import ConfigBase
from ..utils import Logger


class IniConfig(ConfigBase):
    __parser = None
    filepath = None
    service = None

    def __init__(self):
        self.__log = Logger(__name__)
        self.__parser = ConfigParser(dict_type=defaultdict)
        self.__parser._interpolation = ExtendedInterpolation()

    @propery
    def filetypes(self):
        return ['cfg', 'cnf', 'conf', 'config', 'ini']

    def load_config(self, filepath):
        self.__log.debug("INIConf loading file: {}".format(filepath))
        if os.path.isfile(filepath):
            self.__parser.read(filepath)
            # TODO: need to combine all dicts into one dict
            print(self.__parser.sections())
            for section in self.__parser.sections():
                for name, value in self.__parser.items(section):
                    print("  {} = {}".format(name, value))
            self.__configuration = self.__parser._sections
        else:
            self.__log.error("Error: file not in specified path")
            sys.exit("Error: file not in specified path")

    def save_config(self):
        try:
            with open(self.filepath, "w") as configfile:
                self.__parser.write(configfile)
        except IOError as err:
            if err[0] == errno.EPERM:
                self.__log.error(
                    "Error: unable to write to file"
                )
                sys.exit(1)

    def update_config(self, content):
        super()

    def get_config(self):
        return self.__configuration
