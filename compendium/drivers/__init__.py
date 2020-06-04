# -*- coding: utf-8 -*-
# import codecs
# import pkg_resources
from .config_base import ConfigBase  # noqa
from .ini import IniConfig  # noqa
from .json import JsonConfig  # noqa
from .toml import TomlConfig  # noqa
from .yaml import YamlConfig  # noqa
from .utils import ModuleLoader
from .utils import Logger


# TODO: Lookup driver filetypes
def discovery_loader(filetype):
    if filetype == "yaml" or filetype == "yml":
        return "compendium.drivers.YamlConfig"
    elif filetype == "json":
        return "compendium.drivers.JsonConfig"
    elif filetype == "cfg":
        return "compendium.drivers.IniConfig"


def discover(filename):
    self.__log.info("Loading configuration drivers")
    mod = ModuleLoader()
    # TODO: figure out which driver to load from files in paths
    config_class = mod.load_classpath(self.discovery_loader(filetype))
    self.__config_file = config_class()
    self.__log.info("Finished loading drivers")
