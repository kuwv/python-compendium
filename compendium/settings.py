# -*- coding: utf-8 -*-
# import codecs
import os

# import pkg_resources
# import sys
# TODO Use pathlib
from .utils import ModuleLoader
from .utils import Logger
import .driver

class Settings(object):

    __config_file = None
    directory = None
    scenario = None
    provider = None

    def __getattr__(self, k):
        try:
            return self.data[k]
        except KeyError:
            raise AttributeError

    def __init__(self, **kwargs):
        """Load config paths based on priority
        First(lowest) to last(highest)
        1. Load settings.<FILETYPE> from module read-only defaults
          - /usr/lib/<APP>/conf/
        2. Load settings.<FILETYPE> from /etc/<APP>
          - /etc/<APP>/settings.<FILETYPE>
          - /etc/<APP>/<CONFIG>.<FILETYPE>
          - /etc/<APP>/<SUBDIR>/<CONFIG>.<FILETYPE>
        3. Load user configs
          - ~/.<APP>.d/settings.<FILETYPE>
          - ~/.<APP>.d/<CONFIG>.<FILETYPE>
          - ~/.<APP>.d/<SUBDIR>/<CONFIG>.<FILETYPE>
        4. Load config in PWD
          - ./settings.<FILETYPE>
          - ./<CONFIG>.<FILETYPE>
        5. Runtime configs:
          - /etc/sysconfig/<APP>
          - .env
          - <CLI>
        """
        self.__log = Logger(__name__)

        filename = None
        filetype = None
        subdir = None
        self.settings = {}
        self.pathlist = []

        self.__log.info("Determing settings locations")
        # TODO: Skip all if already loaded unless 'reload' is passed
        # Determine service for directory layout
        if "directory" in kwargs:
            self.directory = kwargs.get("directory")

        if "config_dir" in kwargs:
            self.config_dir = kwargs.get("config_dir")
        else:
            self.config_dir = "/etc/compendium"

        if "home_dir" in kwargs:
            self.home_dir = kwargs.get("home_dir")

        if "scenario" in kwargs:
            self.scenario = kwargs.get("scenario")
            subdir = "/scenarios/"
            self.__log.info("Controller settings {}".format(self.scenario))
        else:
            self.provider = "compendium"
            subdir = "/"
            self.__log.info("initiating compendium CLI")

        # Figure out the configuration file
        if "filename" in kwargs:
            # Get the config filename
            filename = kwargs.get("filename")

            # Get the config filetype
            if filetype is None:
                filetype = filename.split(".")[-1]
        else:
            # TODO: Search for filetypes from files in path
            if "filetype" in kwargs:
                filetype = kwargs.get("filetype")
            else:
                filetype = "yml"

            # Get the config filename
            if self.scenario is not None:
                filename = self.scenario + "." + filetype

        self.__log.info("Loading configuration drivers")
        mod = ModuleLoader()
        # TODO: figure out which driver to load from files in paths
        config_class = mod.load_classpath(self.discovery_loader(filetype))
        self.__config_file = config_class()
        self.__log.info("Finished loading drivers")

        # Load configurations
        self.__load_configpaths(subdir)
        self.load_configs(filename)

        # 5. Load from provided path
        # <APP>_CONFIG
        if "config" in kwargs:
            self.load_config(config_path=kwargs.get("config"))

    # TODO: Implement pathlib
    def __load_configpaths(self, subdir):
        """
        First(lowest) to last(highest)
        - System configs
        - User configs
        - Local configs
        - Runtime configs
        """
        if self.directory is not None:
            self.pathlist.append(self.directory + "/")
        else:
            # TODO: Use pkg_resources to locate default configs
            # print(
            #     "Path: ",
            #     pkg_resources.resource_filename(
            #         'compendium',
            #         'usr/share/compendium' + subdir
            #     )
            # )
            self.pathlist.append(subdir)

            self.pathlist.append("/etc/compendium" + subdir)

            self.pathlist.append(os.path.expanduser("~") + "/.compendium.d" + subdir)

            # TODO: Make directory if not exists

            self.pathlist.append(os.getcwd() + "/")

    def load_configs(self, filename):
        for path in self.pathlist:
            self.load_config(path + filename)

    def load_config(self, config_path):
        if os.path.exists(config_path):
            self.__log.info("Loading configuration: '{}'".format(config_path))
            self.__config_file.load_config(filepath=config_path)
            self.update_settings(self.__config_file.get_config())
            self.__log.info("Finished loading configuration: '{}'".format(config_path))
        else:
            self.__log.info(
                "Skipping: No configuration found at: '{}'".format(config_path)
            )

    # TODO: Lookup driver filetypes
    def discovery_loader(self, filetype):
        if filetype == "yaml" or filetype == "yml":
            return "compendium.drivers.YamlConfig"
        elif filetype == "json":
            return "compendium.drivers.JsonConfig"
        elif filetype == "cfg":
            return "compendium.drivers.IniConfig"

    def make_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def get_configpaths(self):
        return self.pathlist

    def get_settings(self):
        return self.settings

    def update_settings(self, new_settings):
        self.__log.debug(new_settings)
        self.settings.update(new_settings)
