# -*- coding: utf-8 -*-
import os
import sys
import pluginbase
from lunar.utils.logger import Logger


class PluginLoader(object):
    """
    1. Identify module part (exp: logging formatter)
    2. Implement plugin scafolding
    3. load plugin
    """

    __pluginPath = None
    __loader = None

    def __init__(self, pluginPath=None):
        self.__log = Logger(__name__)
        if pluginPath is not None:
            self.__pluginPath = pluginPath


class PluginInstaller(object):
    pass
