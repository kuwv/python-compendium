# -*- coding: utf-8 -*-
import codecs
import os
import pkg_resources
import sys
# TODO Use pathlib
from .drivers.config_base import ConfigBase
from .drivers.template import Template
from .utils import Logger


class Settings(object):

    __conf_file = None
    directory = None
    scenario = None
    provider = None

    def __getattr__(self, k):
        try:
            return self.data[k]
        except KeyError:
            raise AttributeError

    def __init__(self, **kwargs):
        '''
        First(lowest) to last(highest)
        - System configs:
            /etc/lunar/$SERVICE/$SERVICE.$FILETYPE
            $LUNA_CONF/$SERVICE/$SERVICE.$FILETYPE
        - User configs:
            $HOME/.lunar.d/$SERVICE/$SERVICE.$FILETYPE
            $PWD/lunar.cfg
        - Runtime configs:
            ENV_VAR
            CLI_VAR
        '''
        self.__log = Logger(__name__)

        filename = None
        filetype = None
        subdir = None
        self.settings = {}
        self.pathlist = []

        self.__log.info("Determing settings locations")
        # TODO: Skip all if already loaded unless 'reload' is passed
        # Determine service for directory layout
        if 'directory' in kwargs:
            self.directory = kwargs.get('directory')

        if 'conf_dir' in kwargs:
            self.conf_dir = kwargs.get('conf_dir')
        else:
            self.conf_dir = '/etc/lunar'

        if 'home_dir' in kwargs:
            self.home_dir = kwargs.get('home_dir')

        if 'lib_dir' in kwargs:
            self.lib_dir = kwargs.get('lib_dir')
        else:
            self.lib_dir = '/var/lib/lunar'

        if 'scenario' in kwargs:
            self.scenario = kwargs.get('scenario')
            subdir = '/scenarios/'
            self.__log.info("Controller settings {}".format(self.scenario))
        elif 'provider' in kwargs:
            self.provider = kwargs.get('provider')
            subdir = '/' + self.provider + '/'
            self.__log.info("Initiating service {}".format(self.provider))
        else:
            self.provider = 'lunar'
            subdir = '/'
            self.__log.info("Initiating Lunar CLI")

        # Figure out the configuration file
        if 'filename' in kwargs:
            # Get the config filename
            filename = kwargs.get('filename')
            # Get the config filetype
            if filetype is None:
                fileArr = filename.split('.')
                filetype = fileArr[-1]
        else:
            # TODO: Search for filetypes from files in path
            if 'filetype' in kwargs:
                filetype = kwargs.get('filetype')
            else:
                filetype = 'yml'
            # Get the config filename
            if self.scenario is not None:
                filename = self.scenario + '.' + filetype
            elif self.provider is not None:
                filename = self.provider + '.' + filetype

        self.__log.info("Loading configuration drivers")
        mod = ModuleLoader()
        # TODO: figure out which driver to load from files in paths
        conf_class = mod.load_classpath(self.discovery_loader(filetype))
        self.__conf_file = conf_class()
        self.__log.info("Finished loading drivers")

        # Load configurations
        self.__load_configpaths(subdir)
        self.load_configs(filename)

        # 5. Load from provided path
        #$LUNA_CONF
        if 'config' in kwargs:
            self.load_config(cfg_path=kwargs.get('config'))

    # TODO: Implement pathlib
    def __load_configpaths(self, subdir):
        '''Load config paths based on priority
        1. Load lunar.cfg from module read-only defaults
          - /usr/lib/python/site-packages/lunar
          - /usr/lib/python/site-packages/lunar-module
          - /usr/lib/lunar/conf/
        2. Load lunar.cfg from /etc/lunar
          - /etc/lunar/lunar.cfg
        3. Load user configs
          - $HOME/.lunar.d/lunar.cfg
          - $HOME/.lunar.d/$SERVICE/$SERVICE.$FILETYPE
        4. Load config in PWD
          - $HOME/.lunar.d/$SERVICE/$SERVICE.$FILETYPE
          - $PWD/lunar.cfg
        '''
        if self.directory is not None:
            self.pathlist.append(self.directory + '/')
        else:
            # TODO: Use pkg_resources to locate default configs
            #print("Path: ", pkg_resources.resource_filename('lunar', 'usr/share/lunar' + subdir))
            self.pathlist.append(subdir)

            self.pathlist.append('/etc/lunar' + subdir)

            self.pathlist.append(os.path.expanduser("~") + '/.lunar.d' + subdir)

            # TODO: Make directory if not exists

            self.pathlist.append(os.getcwd() + '/')

    def load_configs(self, filename):
        for path in self.pathlist:
             self.load_config(path + filename)

    def load_config(self, cfg_path):
        if (os.path.exists(cfg_path)):
            self.__log.info("Loading configuration: '{}'".format(cfg_path))
            self.__conf_file.load_conf(filepath=cfg_path)
            self.update_settings(self.__conf_file.get_conf())
            self.__log.info("Finished loading configuration: '{}'".format(cfg_path))
        else:
            self.__log.info("Skipping: No configuration found at: '{}'".format(cfg_path))

    def discovery_loader(self, filetype):
        if filetype == 'yaml' or filetype == 'yml':
            return 'compendium.drivers.yaml.YamlConf'
        elif filetype == 'json':
            return 'compendium.drivers.json.JsonConf'
        elif filetype == 'cfg':
            return 'compendium.drivers.ini.IniConf'

    def make_directory(self):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_configpaths(self):
        return self.pathlist

    def get_settings(self):
        return self.settings

    def update_settings(self, new_settings):
        self.__log.debug(new_settings)
        self.settings.update(new_settings)

    def get_provider_conf(self, sp):
        return self.__configuration[sp]
