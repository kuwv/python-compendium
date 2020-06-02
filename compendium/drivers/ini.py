# -*- coding: utf-8 -*-
import os
import sys
from lunar.config import ConfigBase
from lunar.utils import Logger
from collections import defaultdict
from configparser import ConfigParser, ExtendedInterpolation


class IniConf(ConfigBase):
    __parser = None
    filepath = None
    service = None

    def __init__(self):
        self.__log = Logger(__name__)
        self.__parser = ConfigParser(dict_type=defaultdict)
        self.__parser._interpolation = ExtendedInterpolation()

    def load_conf(self, filepath):
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
            self.__log.error("Unable to locate file in specified path")
            sys.exit("Error: Unable to locate file in specified path")

    def save_conf(self):
        try:
            with open(self.filepath, "w") as configfile:
                self.__parser.write(configfile)
        except IOError as err:
            if err[0] == errno.EPERM:
                self.__log.error(
                    "Error: You do not have permission to write to this file"
                )
                sys.exit(1)

    def update_conf(self, content):
        super()

    def get_conf(self):
        return self.__configuration

    """
    def list_conf(self):
        for section in self.__parser.sections():
            print('Section:', section)
            print('Options:', self.__parser.options(section))
            for name, value in self.__parser.items(section):
                print('  %s = %s' % (name, value))
            print()

    def get_conf(self):
        d = dict(self.__parser._sections)
        for k in d:
            d[k] = dict(self.__parser._defaults, **d[k])
            d[k].pop('__name__', None)
        setattr(Settings, self.service, d)
        return d

    def get_value(self, section, key):
        return self.__parser.get(section, key)

    def update_value(self, section, key, value):
        self.__parser.set(section, key, value);

    def add_section(self, section):
        self.__parser.add_section(section)

    def get_section(self, section):
        return self.__parser._sections[section]

    def get_list(self, section, key):
        #return self.get_value(section, key).split('\n')
        #return json.loads(self.get_value(section, key).split('\n'))
        result = self.get_value(section, key).split('\n [ ]')
        print(result)
        return result

    #def get_list_item(self, section, key):
    #    value = self.__parser.get(section, key)
    #    return list(filter(None, (x.strip() for x in value.splitlines())))

    #def get_list(self, section, key):
    #    return [x for x in self.get_list_item(section, key)]

    def update_section(self, section, args):
        for key,value in args:
            self.__parser.set(section, key, value)
    """
