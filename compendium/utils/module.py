# -*- coding: utf-8 -*-
import importlib
import importlib.machinery
import pkg_resources
import pkgutil
from .logger import Logger

SUFFIXES = [
    ('Source:', importlib.machinery.SOURCE_SUFFIXES),
    ('Debug:', importlib.machinery.DEBUG_BYTECODE_SUFFIXES),
    ('Optimized:', importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES),
    ('Bytecode:', importlib.machinery.BYTECODE_SUFFIXES),
    ('Extension:', importlib.machinery.EXTENSION_SUFFIXES),
]


def discover_plugins(self, module_prefix='lunar_'):
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith(module_prefix)
    }


def discover_entry_points(self, entry):
    return {
        entry_point.name: entry_point.load()
        for entry_point
        in pkg_resources.iter_entry_points(entry)
    }


# TODO: should load scenarios from pkgutil
# https://packaging.python.org/guides/creating-and-discovering-plugins/
# pluginbase +1
# stevedore -1 only 2.7 and 3.5 ?!?
# importlib +1
class ModuleLoader(object):

    __modulePath = None
    __loader = None

    def __init__(self, modulePath=None):
        self.__log = Logger(__name__)
        if modulePath is not None:
            self.__modulePath = modulePath

    """
    def find_loader(self, loaderName):
        self.__loader = importlib.find_loader(loaderName)

    def load_package_module(self, loaderName, moduleName):
        pkg_loader = self.find_loader(loaderName)
        pkg = pkg_loader.load_module()
        self.__loader = importlib.find_loader(moduleName, pkg.__path__)

    def reload_module(self, moduleName):
        try:
            module = importlib.reload(moduleName)
        except ImportError:
            self.__log.error("Failed to reload {m}".format(m=moduleName))
        return module
    """

    def load_module(self, moduleName):
        try:
            module = importlib.import_module(moduleName)
        except ImportError:
            self.__log.error("Failed to load {m}".format(m=moduleName))
        return module

    def load_classpath(self, fullClassPath):
        self.__log.info("Loading class {c}".format(c=fullClassPath))
        try:
            classData = fullClassPath.split('.')
            modulePath = '.'.join(classData[:-1])
            className = classData[-1]
            self.__log.info(
                "Module: {m} Class: {c}".format(m=modulePath, c=className)
            )
            module = self.load_module(modulePath)
        except ImportError:
            self.__log.error("Failed to load {c}".format(c=className))
        return getattr(module, className)


class ModuleInstaller(object):
    pass
